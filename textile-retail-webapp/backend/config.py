from pathlib import Path
from dotenv import load_dotenv


ENV_PATH = Path(__file__).resolve().parent / ".env"


def load_app_env():
    load_dotenv(ENV_PATH, override=False)
