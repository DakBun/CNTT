"""Analysis utilities for cleaned survey DataFrames."""

import pandas as pd


def compute_summary(df: pd.DataFrame) -> dict:
    """
    Tổng hợp thống kê mô tả từ DataFrame đã làm sạch.

    Args:
        df: DataFrame đầu vào (kết quả từ load_all_years() hoặc sau
        clean_missing/filter_salary_outliers).

    Returns:
        dict: Từ điển chứa số dòng, số cột, tỷ lệ giá trị thiếu theo cột,
        thống kê lương cơ bản, và phân phối năm khảo sát.
    """
    raise NotImplementedError


def analyze_salary_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Phân tích xu hướng lương trung vị theo năm và nhóm nghề nghiệp.

    Args:
        df: DataFrame đã có cột survey_year và salary_usd.

    Returns:
        pd.DataFrame: Bảng thống kê lương theo năm/nhóm nghề nghiệp,
        giữ NaN riêng biệt.
    """
    raise NotImplementedError


def analyze_tech_demand(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Thống kê nhu cầu công nghệ từ cột đã explode dạng long.

    Args:
        df: DataFrame dạng long từ explode_multiselect, ví dụ cột
        `languages_used` đã explode.
        column: Tên cột công nghệ cần phân tích.

    Returns:
        pd.DataFrame: Bảng xếp hạng công nghệ theo tần suất xuất hiện.
    """
    raise NotImplementedError


def analyze_remote_work(df: pd.DataFrame) -> pd.DataFrame:
    """
    Thống kê xu hướng làm việc từ xa theo năm và quy mô công ty.

    Args:
        df: DataFrame đầu vào đã làm sạch.

    Returns:
        pd.DataFrame: Tổ hợp tỷ lệ làm việc từ xa theo các nhóm.
    """
    raise NotImplementedError
