# Phân tích thị trường việc làm ngành CNTT

Dự án phân tích dữ liệu thị trường việc làm ngành CNTT sử dụng Stack Overflow Developer Survey (3 kỳ khảo sát: 2019, 2022, 2025) kết hợp dữ liệu tin tuyển dụng CNTT Việt Nam thu thập thủ công.

## Cấu trúc thư mục

```
CNTT/
├── .gitignore
├── .clinerules
├── requirements.txt
├── README.md
├── notebooks/              # không sử dụng (dự án chạy bằng script .py, không dùng Jupyter)
├── src/
│   ├── config.py           # Hằng số đường dẫn dùng chung
│   ├── ingestion/          # Lấy dữ liệu đầu vào
│   │   ├── survey_loader.py
│   │   ├── vn_jobs_scraper.py
│   │   └── sql_loader.py
│   ├── processing/         # Làm sạch và chuẩn hóa
│   │   └── cleaner.py
│   ├── analysis/           # Phân tích số liệu
│   │   ├── analyzer.py
│   │   └── sql_analyzer.py
│   └── visualization/      # Vẽ biểu đồ xuất ra figures
│       └── charts.py
├── data/
│   ├── raw/                # Dữ liệu thô từ survey / crawl
│   ├── processed/          # Dữ liệu đã làm sạch
│   └── external/           # Dữ liệu tham chiếu bên ngoài
│       └── vn_jobs_manual.csv
├── scripts/
│   ├── load_respondent_skills_only.py
│   └── setup_sql.py
└── figures/                # Sinh biểu đồ, ảnh xuất ra
```

## Nguồn dữ liệu

- **Stack Overflow Developer Survey** các năm 2019, 2022, 2025 — tải qua Kaggle mirror (ghi rõ đây là bản mirror của dữ liệu chính thức survey.stackoverflow.co), giấy phép **Open Database License (ODbL)** — ghi nguồn khi trích dẫn kết quả.
- **Dữ liệu tuyển dụng CNTT Việt Nam**: thu thập thủ công 5 tin từ ITviec (`data/external/vn_jobs_manual.csv`). Việc cào tự động không khả thi — xem mục Hạn chế bên dưới.


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

Chạy toàn bộ pipeline với tiến độ:

```powershell
.venv\Scripts\python.exe main.py
```

Hoặc chạy từng đoạn script nhỏ:

```powershell
.venv\Scripts\python.exe -c "from src.ingestion.survey_loader import load_all_years; df = load_all_years([2019, 2022, 2025]); print(df.shape)"
```

Hoặc chạy trực tiếp file `.py` bằng nút **Run** trong VS Code.
## Tạo lại biểu đồ

Thư mục `figures/` không được commit (đã gitignore) — chạy lệnh sau để tạo lại 5 biểu đồ:

```powershell
.venv\Scripts\python.exe -c "from src.ingestion.survey_loader import load_all_years; from src.processing.cleaner import clean_missing, filter_salary_outliers, explode_multiselect, normalize_remote_work, normalize_edlevel; from src.visualization.charts import plot_salary_trend, plot_tech_popularity, plot_remote_work_distribution, plot_education_distribution, plot_salary_boxplot; from src.config import FIGURES_DIR; df = load_all_years([2019,2022,2025]); df = clean_missing(df); df = normalize_remote_work(df); df = normalize_edlevel(df); df = filter_salary_outliers(df); plot_salary_trend(df, FIGURES_DIR/'salary_trend.png'); dl = explode_multiselect(df,'languages_used'); plot_tech_popularity(dl,'languages_used', FIGURES_DIR/'tech_popularity.png'); plot_remote_work_distribution(df, FIGURES_DIR/'remote_work.png'); plot_education_distribution(df, FIGURES_DIR/'education.png'); plot_salary_boxplot(df, FIGURES_DIR/'salary_box.png','EdLevel')"
```

## Trạng thái hiện tại

- [x] Thu thập dữ liệu SO Survey (2019, 2022, 2025) — đã xác minh đúng năm qua số dòng dữ liệu
- [x] `load_all_years()` — gộp 3 năm thành 1 DataFrame (211.274 dòng x 275 cột; còn 202.739 dòng sau khi lọc outlier lương)
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

(`pyodbc` cố ý KHÔNG đưa vào requirements.txt vì cần driver ODBC hệ thống — chỉ cài khi muốn dùng phần SQL Server.)

Đây là phần **MỞ RỘNG**, không ảnh hưởng pipeline pandas chính — máy không có SQL Server vẫn chạy được toàn bộ phần phân tích/báo cáo qua `src/analysis/analyzer.py` bình thường.

Cách chạy:
```powershell
python -c "from src.ingestion.sql_loader import load_to_sql_server; load_to_sql_server()"
```

Kết nối mặc định: `localhost\SQLEXPRESS`, Windows Authentication, database `DT20_CNTT` (tự tạo nếu chưa có).

## Hạn chế đã biết

- Cỡ mẫu tin tuyển dụng VN nhỏ (5 tin) — kết quả so sánh VN vs toàn cầu chỉ mang tính minh họa, chưa đủ khái quát hóa.
- Cào tự động ITviec/TopCV không khả thi: robots.txt cho phép nhưng cả 2 trang không trả dữ liệu tin tuyển dụng trong HTML thô và không có API công khai ổn định (đã kiểm tra JSON-LD, __NEXT_DATA__, Algolia).
- Tỷ lệ không trả lời cao ở một số câu hỏi (remote_work: 19-31% tùy năm).
- Khảo sát 2022 không tách chi tiết mức độ hybrid như 2019/2025, nên các mức hybrid được gộp chung khi so sánh xuyên năm.
