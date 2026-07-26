"""Visualization utilities for analysis results."""

import pandas as pd
from pathlib import Path


def plot_salary_trend(
    df: pd.DataFrame,
    output_path: str | Path,
    salary_col: str = "salary_usd",
    group_col: str | None = None,
) -> None:
    """
    Vẽ biểu đồ xu hướng lương trung vị theo năm, có thể nhóm thêm theo
    một cột phân loại như DevType hoặc Country.

    Args:
        df: DataFrame đã có survey_year và salary_usd.
        output_path: Đường dẫn file ảnh đầu ra, ví dụ "figures/salary_trend.png".
        salary_col: Tên cột lương chuẩn hóa.
        group_col: Cột phân nhóm thêm, ví dụ "DevType".
    """
    raise NotImplementedError


def plot_tech_popularity(
    df: pd.DataFrame,
    column: str,
    output_path: str | Path,
    top_n: int = 20,
) -> None:
    """
    Vẽ biểu đồ cột ngang thể hiện top N công nghệ phổ biến nhất trong
    cột đã explode dạng long.

    Args:
        df: DataFrame dạng long, ví dụ kết quả explode_multiselect().
        column: Tên cột chứa tên công nghệ đã explode.
        output_path: Đường dẫn file ảnh đầu ra.
        top_n: Số lượng công nghệ hiển thị.
    """
    raise NotImplementedError


def plot_remote_work_distribution(
    df: pd.DataFrame,
    output_path: str | Path,
    remote_col: str = "remote_work",
) -> None:
    """
    Vẽ biểu đồ phân phối trạng thái làm việc từ xa, có thể tách theo năm.

    Args:
        df: DataFrame đã làm sạch.
        output_path: Đường dẫn file ảnh đầu ra.
        remote_col: Tên cột biểu thị làm việc từ xa.
    """
    raise NotImplementedError


def plot_education_distribution(
    df: pd.DataFrame,
    output_path: str | Path,
    education_col: str = "EdLevel",
) -> None:
    """
    Vẽ biểu đồ phân bố trình độ học vấn, có thể nhóm theo năm khảo sát.

    Args:
        df: DataFrame đã làm sạch.
        output_path: Đường dẫn file ảnh đầu ra.
        education_col: Tên cột trình độ học vấn.
    """
    raise NotImplementedError
