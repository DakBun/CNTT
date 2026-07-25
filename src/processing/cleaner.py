"""Data cleaning utilities for survey DataFrames."""

import pandas as pd


def explode_multiselect(df: pd.DataFrame, column: str, sep: str = ";") -> pd.DataFrame:
    """
    Tách 1 cột chứa nhiều giá trị nối bằng dấu ';' thành nhiều dòng (long format),
    mỗi dòng 1 giá trị. Dùng cho các cột như languages_used, databases_used,
    webframes_used. Giữ nguyên các cột khác, chỉ explode cột được chỉ định.
    Cần xử lý: giá trị NaN (không explode ra dòng rỗng), khoảng trắng thừa
    quanh dấu ';'.

    Args:
        df: DataFrame đầu vào (ví dụ: đầu ra từ load_all_years()).
        column: Tên cột cần explode (ví dụ: "languages_used").
        sep: Ký tự phân tách các giá trị trong ô, mặc định ';'.

    Returns:
        pd.DataFrame: DataFrame ở dạng long với các cột gốc được giữ lại,
        trừ cột bị explode bị thay thế bằng giá trị từng dòng.
    """
    raise NotImplementedError


def filter_salary_outliers(
    df: pd.DataFrame,
    salary_col: str = "salary_usd",
    method: str = "iqr",
) -> pd.DataFrame:
    """
    Lọc bỏ các dòng có giá trị lương phi thực tế (0, âm, hoặc quá lớn do nhập
    sai đơn vị). Hỗ trợ 2 phương pháp: 'iqr' (loại theo khoảng tứ phân vị) và
    'percentile' (loại theo phần trăm cao/thấp nhất, ví dụ 1%-99%). Trả về
    DataFrame đã lọc, giữ nguyên các dòng có salary_col là NaN (không lọc nhầm
    người không trả lời câu hỏi lương).

    Args:
        df: DataFrame đầu vào.
        salary_col: Tên cột lương đã chuẩn hóa, mặc định "salary_usd".
        method: Phương pháp lọc outlier: "iqr" hoặc "percentile".

    Returns:
        pd.DataFrame: DataFrame đã loại bỏ các dòng lương phi thực tế,
        giữ lại NaN.
    """
    raise NotImplementedError


def clean_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Xử lý giá trị thiếu cho các cột chính (13 cột chung + salary_usd). Không
    tự ý điền giá trị cho các cột đa lựa chọn (languages_used, v.v.) vì NaN ở
    đó có nghĩa là "không trả lời", cần giữ nguyên để phân biệt với "trả lời
    rỗng".

    Args:
        df: DataFrame đầu vào (kết quả từ load_all_years() hoặc sau explode).

    Returns:
        pd.DataFrame: DataFrame đã xử lý missing theo từng nhóm cột,
        giữ nguyên cấu trúc và các cột đa lựa chọn.
    """
    raise NotImplementedError
