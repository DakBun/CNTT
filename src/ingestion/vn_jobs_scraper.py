"""Web scraping utilities for Vietnamese IT job listings."""

import pandas as pd

from src.config import EXTERNAL_DIR


def scrape_vn_jobs(source: str, limit: int = 100) -> pd.DataFrame:
    """
    Cào dữ liệu tin tuyển dụng CNTT Việt Nam từ 1 nguồn (itviec hoặc topcv).
    Trả về DataFrame với các cột: job_title, company, required_skills
    (list các công nghệ/kỹ năng yêu cầu, dạng chuỗi cách nhau bởi ';' để
    đồng bộ với cách xử lý languages_used), location, salary_range (str,
    giữ nguyên dạng text gốc vì mỗi tin đăng ghi khác nhau), posted_date.
    Nếu không lấy được 1 field nào đó, để giá trị None, không được bỏ qua
    cả dòng.

    Lưu ý:
        Tự động cào bị chặn bởi cấu trúc trang động (không tìm thấy card tin
        trong HTML thô, không có Algolia public) — xem
        ``load_manual_vn_jobs()`` để dùng dữ liệu thu thập thủ công thay thế.

    Args:
        source: Nguồn cào dữ liệu, ví dụ "itviec" hoặc "topcv".
        limit: Số lượng tin tối đa cần lấy trong 1 lần chạy.

    Returns:
        pd.DataFrame: DataFrame chứa thông tin tin tuyển dụng đã chuẩn hóa,
        các cột thiếu sẽ là None thay vì bỏ qua dòng.
    """
    raise NotImplementedError


def load_manual_vn_jobs() -> pd.DataFrame:
    """
    Đọc dữ liệu tin tuyển dụng CNTT Việt Nam đã thu thập thủ công (do việc
    cào tự động từ ITviec/TopCV không khả thi trong thời gian cho phép —
    cả 2 trang không có dữ liệu tuyển dụng trong HTML thô, không phát hiện
    API công khai ổn định để gọi trực tiếp).

    Returns:
        pd.DataFrame: DataFrame chứa các cột ``job_title``, ``company``,
        ``required_skills``, ``location``, ``posted_date``.
    """
    path = EXTERNAL_DIR / "vn_jobs_manual.csv"
    return pd.read_csv(path)
