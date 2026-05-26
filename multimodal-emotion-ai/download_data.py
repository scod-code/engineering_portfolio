import subprocess
import sys
import os
import urllib.request
import zipfile
from pathlib import Path


def download_ravdess(output_dir="ravdess_data"):
    if Path(output_dir).exists() and any(Path(output_dir).rglob("*.wav")):
        print(f"RAVDESS already present in {output_dir}/. Skipping.")
        return
    Path(output_dir).mkdir(exist_ok=True)
    print("Downloading RAVDESS audio (~215 MB)...")
    subprocess.run([
        sys.executable, "-m", "zenodo_get",
        "https://zenodo.org/records/1188976",
        "-o", output_dir
    ], check=True)
    print("RAVDESS download complete.")


def download_felt(output_dir="felt_data"):
    if Path(output_dir).exists() and any(Path(output_dir).rglob("*.csv")):
        print(f"FELT already present in {output_dir}/. Skipping.")
        return
    Path(output_dir).mkdir(exist_ok=True)
    zip_path = "smoothed_motion_speech.zip"
    url = "https://zenodo.org/records/13243600/files/smoothed_motion_speech.zip?download=1"

    print("Downloading FELT smoothed speech CSVs (~945 MB)...")
    print("This will take several minutes depending on your connection.")

    def progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        pct = min(downloaded / total_size * 100, 100)
        print(f"\r  {pct:.1f}% ({downloaded // 1_000_000} MB / {total_size // 1_000_000} MB)", end="")

    urllib.request.urlretrieve(url, zip_path, reporthook=progress)
    print("\nExtracting...")

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(output_dir)

    os.remove(zip_path)
    csv_count = len(list(Path(output_dir).rglob("*.csv")))
    print(f"Done. {csv_count} CSV files extracted to {output_dir}/")


if __name__ == "__main__":
    download_ravdess()
    download_felt()
