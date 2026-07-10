"""
Top-level entry so a process that runs `uvicorn main:app` will find
the FastAPI `app` defined in `backend/main.py`.

Render's default start command from the guide used `uvicorn main:app`.
This file simply imports the app and exposes it at top level.
"""
from backend.main import app  # re-export the application


if __name__ == "__main__":
    # Local convenience: run the app directly for quick testing
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
