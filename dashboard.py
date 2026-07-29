"""Dashboard Streamlit: khám phá dữ liệu khảo sát CNTT."""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.analysis.analyzer import (
    analyze_remote_work,
    analyze_salary_by_group,
    analyze_tech_demand,
)
from src.config import PROCESSED_DIR
from src.processing.cleaner import explode_multiselect

st.set_page_config(page_title="Phân tích thị trường việc làm CNTT", layout="wide")


@st.cache_data
def load_data():
    path = PROCESSED_DIR / "dashboard_data.pkl"
    if not path.exists():
        st.error(
            "Chưa có cache dữ liệu. Chạy trước: "
            "`.venv\\Scripts\\python.exe scripts\\build_processed_cache.py`"
        )
        st.stop()
    return pd.read_pickle(path)


def main() -> None:
    st.title("Phân tích thị trường việc làm CNTT")

    df = load_data()

    # Sidebar filter
    years = sorted(df["survey_year"].dropna().unique().tolist())
    selected_years = st.sidebar.multiselect("Chọn năm", years, default=years)
    countries = sorted(df["Country"].dropna().unique().tolist())
    country_options = ["Tất cả"] + countries
    selected_country = st.sidebar.selectbox("Chọn quốc gia", country_options, index=0)

    view = df[df["survey_year"].isin(selected_years)]
    if selected_country != "Tất cả":
        view = view[view["Country"] == selected_country]

    # Metrics
    total_responses = len(view)
    median_salary = view["salary_usd"].median() if "salary_usd" in view.columns else None
    n_countries = view["Country"].nunique() if "Country" in view.columns else None
    remote_rate = (
        view["remote_work"].value_counts(normalize=True).get("Toàn thời gian từ xa", 0) * 100
        if "remote_work" in view.columns
        else None
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng số phản hồi", f"{total_responses:,}")
    col2.metric(
        "Lương trung vị (USD)",
        f"{median_salary:,.0f}" if pd.notna(median_salary) else "N/A",
    )
    col3.metric("Số quốc gia", n_countries if n_countries is not None else "N/A")
    col4.metric(
        "Tỷ lệ làm việc từ xa toàn thời gian",
        f"{remote_rate:.1f}%" if remote_rate is not None else "N/A",
    )

    tabs = st.tabs(["Công nghệ", "Lương", "Làm việc từ xa", "Học vấn"])

    with tabs[0]:
        st.subheader("Công nghệ phổ biến và mong muốn học")
        used = explode_multiselect(view, "languages_used")
        wanted = explode_multiselect(view, "languages_wanted")

        used_demand = analyze_tech_demand(used, "languages_used", top_n=15)
        wanted_demand = analyze_tech_demand(wanted, "languages_wanted", top_n=15)

        c1, c2 = st.columns(2)
        with c1:
            st.caption("Đã dùng")
            st.bar_chart(used_demand.set_index("languages_used")["count"])
        with c2:
            st.caption("Muốn học")
            st.bar_chart(wanted_demand.set_index("languages_wanted")["count"])

        used_full = used["languages_used"].dropna().value_counts(normalize=True).mul(100).rename("pct_used")
        wanted_full = wanted["languages_wanted"].dropna().value_counts(normalize=True).mul(100).rename("pct_wanted")
        gap_table = pd.concat([used_full, wanted_full], axis=1).fillna(0)
        gap_table["gap"] = gap_table["pct_wanted"] - gap_table["pct_used"]
        gap_table = gap_table.sort_values("gap", ascending=False).reset_index().rename(columns={"index": "tech"})
        st.subheader("Chênh lệch nhu cầu: muốn học - đã dùng (%)")
        st.dataframe(gap_table.round(2))

    with tabs[1]:
        st.subheader("Phân tích lương")
        group_options = [
            "experience_group",
            "EdLevel",
            "Country",
            "languages_used",
        ]
        group_col = st.selectbox("Chiều phân tích", group_options)
        if group_col == "languages_used":
            salary_df = explode_multiselect(view, group_col)
        else:
            salary_df = view
        salary_table = analyze_salary_by_group(salary_df, group_col)
        st.bar_chart(salary_table.groupby(group_col)["median"].mean().sort_values(ascending=False))
        st.dataframe(salary_table.reset_index(drop=True))

    with tabs[2]:
        st.subheader("Phân bố hình thức làm việc từ xa theo năm")
        remote_table = analyze_remote_work(view)
        pivot = (
            remote_table.pivot_table(
                index="remote_work", columns="survey_year", values="pct"
            )
            .fillna(0)
            .sort_values(view["survey_year"].max(), ascending=False)
        )
        st.bar_chart(pivot.T)
        st.dataframe(remote_table.reset_index(drop=True))

    with tabs[3]:
        st.subheader("Phân bố trình độ học vấn theo năm")
        edu_table = (
            view.groupby(["survey_year", "EdLevel"]).size().reset_index(name="count")
        )
        pivot_edu = edu_table.pivot(index="EdLevel", columns="survey_year", values="count").fillna(0)
        st.bar_chart(pivot_edu.T)
        st.dataframe(edu_table.reset_index(drop=True))


if __name__ == "__main__":
    main()
