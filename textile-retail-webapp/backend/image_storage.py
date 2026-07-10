"""
image_storage.py — Modular image storage abstraction for ASAA Fashion & Beauty House.

The active storage backend is selected by the IMAGE_STORAGE environment variable:

    IMAGE_STORAGE=github     (default) — commits image to GitHub repo, returns raw URL.
                                          Requires: GITHUB_TOKEN, GITHUB_REPO, GITHUB_BRANCH.
    IMAGE_STORAGE=cloudinary            — uploads to Cloudinary CDN (add later).
                                          Requires: CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY,
                                                    CLOUDINARY_API_SECRET.
    IMAGE_STORAGE=local                 — saves file to frontend/images/ on disk.
                                          WARNING: ephemeral on Render free tier.
    IMAGE_STORAGE=url_only              — no upload; caller must provide a URL directly.

To switch storage backends, only change the IMAGE_STORAGE env var.
No other code needs to change.

Google Drive links (paste fallback):
    If an admin pastes a Google Drive share URL anywhere, call
    `convert_gdrive_url(url)` to turn it into a direct-view URL.
    This is a client-side convenience, not a storage backend.
"""

import os
import re
import uuid
import base64
import asyncio
from pathlib import Path
from typing import Optional

from .config import load_app_env

load_app_env()


# ---------------------------------------------------------------------------
# Base interface — all storage backends implement these two methods
# ---------------------------------------------------------------------------

class ImageStorage:
    """Abstract image storage interface. Swap by implementing a subclass."""

    async def upload(self, filename: str, content: bytes, content_type: str = "image/jpeg") -> str:
        """Upload an image and return its public URL."""
        raise NotImplementedError

    async def delete(self, url: str) -> bool:
        """Delete an image by its URL. Returns True if deleted."""
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self.__class__.__name__


# ---------------------------------------------------------------------------
# GitHub storage (primary) — commits image to the repo as a static file
# ---------------------------------------------------------------------------

class GitHubImageStorage(ImageStorage):
    """
    Uploads images by committing them to the GitHub repository under
    frontend/images/.  The image is then served as a static file from the
    deployed site *and* from GitHub's raw CDN.

    Required env vars:
        GITHUB_TOKEN  — personal access token with `repo` (read/write) scope
        GITHUB_REPO   — e.g. "scod-code/textile_retail"
        GITHUB_BRANCH — defaults to "main"
    """

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN", "")
        self.repo = os.getenv("GITHUB_REPO", "scod-code/textile_retail")
        self.branch = os.getenv("GITHUB_BRANCH", "main")
        self._base_url = "https://api.github.com"

    def _is_configured(self) -> bool:
        return bool(self.token and self.repo)

    def _raw_url(self, path_in_repo: str) -> str:
        return f"https://raw.githubusercontent.com/{self.repo}/{self.branch}/{path_in_repo}"

    async def upload(self, filename: str, content: bytes, content_type: str = "image/jpeg") -> str:
        if not self._is_configured():
            raise RuntimeError(
                "GitHub storage is not configured. Set GITHUB_TOKEN and GITHUB_REPO "
                "in backend/.env, or change IMAGE_STORAGE to 'local' or 'url_only'."
            )

        import urllib.request, json as _json

        # Sanitise filename and give it a unique prefix to avoid collisions
        safe_name = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)
        uid = uuid.uuid4().hex[:8]
        repo_path = f"frontend/images/{uid}_{safe_name}"

        payload = {
            "message": f"Add product image {uid}_{safe_name}",
            "branch": self.branch,
            "content": base64.b64encode(content).decode("utf-8"),
        }

        api_url = f"{self._base_url}/repos/{self.repo}/contents/{repo_path}"
        body = _json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(
            api_url,
            data=body,
            headers={
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json",
                "User-Agent": "ASAA-Fashion-App",
            },
            method="PUT",
        )

        def _do_request():
            try:
                with urllib.request.urlopen(req, timeout=15) as resp:
                    return resp.status, resp.read()
            except urllib.error.HTTPError as e:
                return e.code, e.read()

        status, body_bytes = await asyncio.to_thread(_do_request)

        if status not in (200, 201):
            err = body_bytes.decode("utf-8", errors="replace")
            raise RuntimeError(f"GitHub API error {status}: {err}")

        return self._raw_url(repo_path)

    async def delete(self, url: str) -> bool:
        # Deletion via GitHub API requires the file's SHA — skip for now.
        # Images in the repo remain as static assets (cheap storage, good history).
        return False


# ---------------------------------------------------------------------------
# Cloudinary storage (future / plug-in-when-ready)
# ---------------------------------------------------------------------------

class CloudinaryImageStorage(ImageStorage):
    """
    Upload images to Cloudinary CDN.

    Required env vars:
        CLOUDINARY_CLOUD_NAME
        CLOUDINARY_API_KEY
        CLOUDINARY_API_SECRET

    Install: pip install cloudinary
    """

    async def upload(self, filename: str, content: bytes, content_type: str = "image/jpeg") -> str:
        try:
            import cloudinary
            import cloudinary.uploader
        except ImportError:
            raise RuntimeError("Install the 'cloudinary' package to use Cloudinary storage.")

        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
            secure=True,
        )
        uid = uuid.uuid4().hex[:8]
        safe_name = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)
        public_id = f"asaa-products/{uid}_{Path(safe_name).stem}"

        def _upload():
            return cloudinary.uploader.upload(
                content,
                public_id=public_id,
                resource_type="image",
                overwrite=False,
            )

        result = await asyncio.to_thread(_upload)
        return result["secure_url"]

    async def delete(self, url: str) -> bool:
        try:
            import cloudinary.uploader
            public_id = url.split("/upload/")[-1].rsplit(".", 1)[0]
            await asyncio.to_thread(cloudinary.uploader.destroy, public_id)
            return True
        except Exception:
            return False


# ---------------------------------------------------------------------------
# Local disk storage (development only — NOT persistent on Render free tier)
# ---------------------------------------------------------------------------

class LocalImageStorage(ImageStorage):
    """
    Saves images to frontend/images/ on the local filesystem.
    Files are served by FastAPI's StaticFiles mount.
    WARNING: This directory is wiped on every Render deploy restart.
    Use GitHub or Cloudinary storage in production.
    """

    def __init__(self):
        self.images_dir = Path(__file__).resolve().parent.parent / "frontend" / "images"
        self.images_dir.mkdir(parents=True, exist_ok=True)

    async def upload(self, filename: str, content: bytes, content_type: str = "image/jpeg") -> str:
        safe_name = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)
        uid = uuid.uuid4().hex[:8]
        dest = self.images_dir / f"{uid}_{safe_name}"

        def _write():
            dest.write_bytes(content)

        await asyncio.to_thread(_write)
        return f"/images/{uid}_{safe_name}"

    async def delete(self, url: str) -> bool:
        fname = url.lstrip("/images/")
        target = self.images_dir / fname
        if target.exists():
            target.unlink()
            return True
        return False


# ---------------------------------------------------------------------------
# URL-only (no upload — admin pastes a public image URL)
# ---------------------------------------------------------------------------

class URLPassthroughStorage(ImageStorage):
    """No upload at all — the caller provides a public URL directly."""

    async def upload(self, filename: str, content: bytes, content_type: str = "image/jpeg") -> str:
        raise RuntimeError("URL-only storage cannot accept file uploads. Paste a URL instead.")

    async def delete(self, url: str) -> bool:
        return False  # Nothing to delete


# ---------------------------------------------------------------------------
# Factory — returns the active backend based on IMAGE_STORAGE env var
# ---------------------------------------------------------------------------

_storage_instance: Optional[ImageStorage] = None


def get_image_storage() -> ImageStorage:
    """
    Returns the configured ImageStorage backend.
    Cached after the first call.

    Switch backends by setting IMAGE_STORAGE in backend/.env:
        github      (default)
        cloudinary
        local
        url_only
    """
    global _storage_instance
    if _storage_instance is not None:
        return _storage_instance

    backend = os.getenv("IMAGE_STORAGE", "github").lower().strip()

    if backend == "github":
        _storage_instance = GitHubImageStorage()
    elif backend == "cloudinary":
        _storage_instance = CloudinaryImageStorage()
    elif backend == "local":
        _storage_instance = LocalImageStorage()
    elif backend == "url_only":
        _storage_instance = URLPassthroughStorage()
    else:
        print(f"[image_storage] Unknown IMAGE_STORAGE='{backend}', defaulting to GitHub.")
        _storage_instance = GitHubImageStorage()

    print(f"[image_storage] Using backend: {_storage_instance.name}")
    return _storage_instance


# ---------------------------------------------------------------------------
# Google Drive URL conversion helper (client-side paste convenience)
# ---------------------------------------------------------------------------

def convert_gdrive_url(url: str) -> Optional[str]:
    """
    Convert a Google Drive share URL into a direct image URL.

    Handles these formats:
        https://drive.google.com/file/d/FILE_ID/view?usp=sharing
        https://drive.google.com/open?id=FILE_ID
        https://drive.google.com/uc?id=FILE_ID

    Returns the direct-view URL, or None if the URL is not a Google Drive link.
    """
    if not url or "drive.google.com" not in url:
        return None

    # Extract file ID
    patterns = [
        r"drive\.google\.com/file/d/([a-zA-Z0-9_-]+)",
        r"drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)",
        r"drive\.google\.com/uc\?.*?id=([a-zA-Z0-9_-]+)",
    ]
    for pattern in patterns:
        m = re.search(pattern, url)
        if m:
            file_id = m.group(1)
            return f"https://drive.google.com/uc?export=view&id={file_id}"

    return None
