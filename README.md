# Phân tích thị trường việc làm ngành CNTT

Dự án phân tích dữ liệu thị trường việc làm ngành CNTT sử dụng Stack Overflow Developer Survey (2019-2025) và dữ liệu crawl từ ITviec/TopCV.

## Cấu trúc thư mục

```
CNTT/
├── .gitignore
├── requirements.txt
├── README.md
├── notebooks/              # Jupyter notebooks để khám phá và trình bày
├── src/
│   ├── config.py           # Hằng số đường dẫn dùng chung
│   ├── ingestion/          # Lấy dữ liệu đầu vào
│   │   ├── survey_loader.py
│   │   └── vn_jobs_scraper.py
│   ├── processing/         # Làm sạch và chuẩn hóa
│   │   └── cleaner.py
│   ├── analysis/           # Phân tích số liệu
│   │   └── analyzer.py
│   └── visualization/      # Vẽ biểu đồ xuất ra figures
│       └── charts.py
├── data/
│   ├── raw/                # Dữ liệu thô từ survey / crawl
│   ├── processed/          # Dữ liệu đã làm sạch
│   └── external/           # Dữ liệu tham chiếu bên ngoài
└── figures/                # Sinh biểu đồ, ảnh xuất ra
```

## Nguồn dữ liệu

- **Stack Overflow Developer Survey** các năm 2019, 2022, 2025 — tải qua Kaggle mirror (ghi rõ đây là bản mirror của dữ liệu chính thức survey.stackoverflow.co), giấy phép **Open Database License (ODbL)** — ghi nguồn khi trích dẫn kết quả.
- **Dữ liệu tuyển dụng CNTT Việt Nam**: crawl từ ITviec/TopCV (đang xây dựng).


## Hướng dẫn cài đặt

### 1. Tạo virtual environment

```powershell
# Windows PowerShell
python -m venv .venv
```

```bash
# macOS / Linux
python3 -m venv .venv
```

### 2. Kích hoạt virtual environment

```powershell
# Windows PowerShell
.venv/Scripts/Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

### 3. Cài dependencies

```powershell
pip install -r requirements.txt
```

## Cách chạy

Chạy trực tiếp một đoạn script Python bằng VS Code:

```powershell
.venv\Scripts\python.exe -c "from src.ingestion.survey_loader import load_all_years; df = load_all_years([2019, 2022, 2025]); print(df.shape)"
```

Hoặc chạy trực tiếp file `.py` bằng nút **Run** trong VS Code.
## Trạng thái hiện tại

- [x] Thu thập dữ liệu SO Survey (2019, 2022, 2025) — đã xác minh đúng năm qua số dòng dữ liệu
- [x] `load_all_years()` — gộp 3 năm thành 1 DataFrame (202,739 dòng)
- [x] `cleaner.py` — hoàn thành (explode multi-select, lọc outlier lương, gộp nhóm remote_work/EdLevel)
- [x] `analyzer.py` — hoàn thành (4 hàm phân tích chính + so sánh VN vs global)
- [x] `charts.py` — hoàn thành (5 loại biểu đồ)
- [x] `vn_jobs_manual.csv` — thu thập thủ công 5 tin (do scrape tự động ITviec/TopCV không khả thi — không có dữ liệu trong HTML thô, không có Algolia public). **LƯU Ý:** cỡ mẫu nhỏ, kết quả so sánh VN/global chỉ mang tính minh họa.
- [x] Tích hợp SQL Server (nâng cao) — 4 bảng quan hệ, 4 câu demo GROUP BY/JOIN/window function/CTE+FULL JOIN — xem mục bên dưới

## Phần nâng cao — SQL Server

Yêu cầu: SQL Server Express/LocalDB + ODBC Driver 17, cài qua:
```
pip install pyodbc sqlalchemy
```

Đây là phần **MỞ RỘNG**, không ảnh hưởng pipeline pandas chính — máy không có SQL Server vẫn chạy được toàn bộ phần phân tích/báo cáo qua `src/analysis/analyzer.py` bình thường.

Cách chạy:
```powershell
python -c "from src.ingestion.sql_loader import load_to_sql_server; load_to_sql_server()"
```

Kết nối mặc định: `localhost\SQLEXPRESS`, Windows Authentication, database `DT20_CNTT` (tự tạo nếu chưa có).
