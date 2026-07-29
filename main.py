"""Pipeline chính: chạy toàn bộ quy trình phân tích dữ liệu từ đầu đến cuối."""

import sys

from pathlib import Path

# Đảm bảo project root có thể import các module trong src/
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.ingestion.survey_loader import load_all_years
from src.processing.cleaner import (
    clean_missing,
    explode_multiselect,
    filter_salary_outliers,
    normalize_edlevel,
    normalize_remote_work,
)
from src.analysis.analyzer import analyze_salary_by_group, analyze_tech_demand, compute_summary
from src.visualization.charts import (
    plot_education_distribution,
    plot_salary_boxplot,
    plot_salary_trend,
    plot_tech_popularity,
    plot_remote_work_distribution,
)
from src.config import FIGURES_DIR


def main() -> None:
    # Bước 1 - Đọc dữ liệu
    print("[1/5] Đang đọc dữ liệu 3 năm...")
    df = load_all_years([2019, 2022, 2025])
    print(f"Shape sau khi đọc: {df.shape}")

    # Bước 2 - Làm sạch
    print("[2/5] Đang làm sạch...")
    df = clean_missing(df)
    df = normalize_remote_work(df)
    df = normalize_edlevel(df)
    df = filter_salary_outliers(df)
    print(f"Shape sau khi lọc: {df.shape}")

    # Bước 3 - Thống kê tổng quan
    print("[3/5] Thống kê tổng quan...")
    summary = compute_summary(df)
    print(f"- Tổng số dòng: {summary['n_rows']}")
    print(f"- Tổng số cột: {summary['n_cols']}")
    print(f"- Lương trung vị: {summary['salary_stats'].get('50%', 'N/A')}")
    print(f"- Năm phân bố: {summary['year_distribution']}")
    print("- Cột dự án có tỷ lệ thiếu cao nhất:")
    focus_cols = [
        "salary_usd", "languages_used", "languages_wanted", "databases_used",
        "webframes_used", "remote_work", "EdLevel", "Country", "DevType",
        "YearsCode", "OrgSize", "Age",
    ]
    missing_focus = {c: summary["missing_pct"].get(c, 0) for c in focus_cols}
    for col, pct in sorted(missing_focus.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  - {col}: {pct*100:.1f}%")

    # Bước 4 - Vẽ biểu đồ
    print("[4/5] Đang vẽ 5 biểu đồ...")
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    paths = {
        "salary_trend": FIGURES_DIR / "salary_trend.png",
        "tech_popularity": FIGURES_DIR / "tech_popularity.png",
        "remote_work": FIGURES_DIR / "remote_work.png",
        "education": FIGURES_DIR / "education.png",
        "salary_box": FIGURES_DIR / "salary_box.png",
    }

    plot_salary_trend(df, paths["salary_trend"])
    print(f"Đã lưu: {paths['salary_trend']}")

    df_lang = explode_multiselect(df, "languages_used")

    plot_tech_popularity(df_lang, "languages_used", paths["tech_popularity"])
    print(f"Đã lưu: {paths['tech_popularity']}")

    plot_remote_work_distribution(df, paths["remote_work"])
    print(f"Đã lưu: {paths['remote_work']}")

    plot_education_distribution(df, paths["education"])
    print(f"Đã lưu: {paths['education']}")

    plot_salary_boxplot(df, paths["salary_box"], "EdLevel")
    print(f"Đã lưu: {paths['salary_box']}")

    # Bước 5 - Phân tích công nghệ và lương
    print("[5/5] Phân tích công nghệ và lương...")
    tech_demand = analyze_tech_demand(df_lang, "languages_used", top_n=15)
    print(tech_demand.to_string(index=False))

    salary_by_ed = analyze_salary_by_group(df, "EdLevel")
    print(salary_by_ed.head(10).to_string(index=False))

    print("HOÀN TẤT - xem biểu đồ trong figures/")


if __name__ == "__main__":
    main()
