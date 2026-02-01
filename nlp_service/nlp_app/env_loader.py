# FILE: nlp_service/app/env_loader.py
import os
import pathlib
from dotenv import load_dotenv

def load_env() -> None:
    """Load .env.<env>(.local) automatically unless DOTENV_CONFIG_PATH is set."""

    # 1) explicit override
    explicit = os.getenv("DOTENV_CONFIG_PATH")
    if explicit and pathlib.Path(explicit).exists():
        load_dotenv(explicit, override=True)
        print(f"[env] loaded explicit {explicit}")
        return

    # 2) based on ENV/NODE_ENV (default = development)
    env = (os.getenv("ENV") or os.getenv("NODE_ENV") or "development").strip().lower()
    root = pathlib.Path(__file__).resolve().parents[1]  # → project/nlp_service

    for candidate in (
        root / f".env.{env}.local",  # highest priority
        root / f".env.{env}",        # fallback for this env
        root / ".env",               # global fallback
    ):
        if candidate.exists():
            load_dotenv(candidate.as_posix(), override=True)
            print(f"[env] loaded {candidate.name}")
            return

    print("[env] no .env file found; relying on process env")
