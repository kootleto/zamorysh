import os
import pickle
from pathlib import Path
from sys import platform

from tools.logger import log


def _resolve_path(path: str) -> Path:
    is_android = "ANDROID_ARGUMENT" in os.environ or platform == "android"

    if is_android:
        base_str = (
            os.environ.get("ANDROID_PRIVATE")
            or os.environ.get("ANDROID_APP_PATH")
            or "."
        )
        base_dir = Path(base_str)
    else:
        base_dir = Path(__file__).resolve().parent.parent

    clean_relative = Path(path)
    if clean_relative.is_absolute() or path.startswith((".", "/", "\\")):
        clean_parts = [p for p in clean_relative.parts if p not in (".", "/", "\\")]
        return base_dir.joinpath(*clean_parts)

    return base_dir / clean_relative


def write_data(path: str, data) -> None:
    abs_path = _resolve_path(path)
    try:
        abs_path.parent.mkdir(parents=True, exist_ok=True)

        with open(abs_path, "wb") as f:
            pickle.dump(data, f)
        log(f"File {abs_path} saved successfully.", log_type="storage")

    except Exception as e:
        log(f"Failed to save {abs_path}: {e}.", log_type="storage")


def read_data(path: str) -> dict | None:
    abs_path = _resolve_path(path)
    if not abs_path.exists():
        log(f"No data found at {path}.", log_type="storage")
        return None

    try:
        with open(abs_path, "rb") as f:
            data = pickle.load(f)
            log(f"File {abs_path} loaded successfully.", log_type="storage")
            return data

    except Exception as e:
        log(f"Failed to load {abs_path}: {e}.", log_type="storage")
        return None
