from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
EXTERNAL_DIR = BASE_DIR / "data" / "external"
FIGURES_DIR = BASE_DIR / "figures"

for _dir in (RAW_DIR, PROCESSED_DIR, EXTERNAL_DIR, FIGURES_DIR):
    _dir.mkdir(parents=True, exist_ok=True)
