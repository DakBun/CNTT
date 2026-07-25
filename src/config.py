"""Central configuration for paths and constants."""

from pathlib import Path

# Base directory of the repository
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
EXTERNAL_DIR = BASE_DIR / "data" / "external"

# Output directories
FIGURES_DIR = BASE_DIR / "figures"

# Ensure directories exist (non-destructive)
for _dir in (RAW_DIR, PROCESSED_DIR, EXTERNAL_DIR, FIGURES_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

SURVEY_YEARS = {
    2019: RAW_DIR / "2019" / "survey_results_public.csv",
    2022: RAW_DIR / "2022" / "survey_results_public.csv",
    2025: RAW_DIR / "2025" / "survey_results_public.csv",
}

COLUMN_MAPPING = {
    # Lương
    "ConvertedComp": "salary_usd",
    "ConvertedCompYearly": "salary_usd",
    # Ngôn ngữ / Database / Webframe đã dùng
    "LanguageWorkedWith": "languages_used",
    "LanguageHaveWorkedWith": "languages_used",
    "DatabaseWorkedWith": "databases_used",
    "DatabaseHaveWorkedWith": "databases_used",
    "WebframeWorkedWith": "webframes_used",
    "WebframeHaveWorkedWith": "webframes_used",
    # 13 cột tên giống nhau ở cả 3 năm — giữ nguyên tên
    "Age": "Age",
    "CompTotal": "CompTotal",
    "Country": "Country",
    "DevType": "DevType",
    "EdLevel": "EdLevel",
    "Employment": "Employment",
    "MainBranch": "MainBranch",
    "OrgSize": "OrgSize",
    "SOAccount": "SOAccount",
    "SOComm": "SOComm",
    "SOPartFreq": "SOPartFreq",
    "SOVisitFreq": "SOVisitFreq",
    "YearsCode": "YearsCode",
}
