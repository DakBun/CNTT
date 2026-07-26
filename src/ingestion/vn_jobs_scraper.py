"""Web scraping utilities for Vietnamese IT job listings."""

import pandas as pd


def scrape_vn_jobs(source: str, limit: int = 100) -> pd.DataFrame:
    """
    Cào dữ liệu tin tuyển dụng CNTT Việt Nam từ 1 nguồn (itviec hoặc topcv).
    Trả về DataFrame với các cột: job_title, company, required_skills
    (list các công nghệ/kỹ năng yêu cầu, dạng chuỗi cách nhau bởi ';' để
    đồng bộ với cách xử lý languages_used), location, salary_range (str,
    giữ nguyên dạng text gốc vì mỗi tin đăng ghi khác nhau), posted_date.
    Nếu không lấy được 1 field nào đó, để giá trị None, không được bỏ qua
    cả dòng.

    Args:
        source: Nguồn cào dữ liệu, ví dụ "itviec" hoặc "topcv".
        limit: Số lượng tin tối đa cần lấy trong 1 lần chạy.

    Returns:
        pd.DataFrame: DataFrame chứa thông tin tin tuyển dụng đã chuẩn hóa,
        các cột thiếu sẽ là None thay vì bỏ qua dòng.
    """
    raise NotImplementedError
