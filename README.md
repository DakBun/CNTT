# Phân tích thị trường việc làm ngành CNTT

Dự án phân tích dữ liệu thị trường việc làm ngành CNTT sử dụng Stack Overflow Developer Survey (3 kỳ khảo sát: 2019, 2022, 2025) kết hợp dữ liệu tin tuyển dụng CNTT Việt Nam thu thập thủ công.

## Cấu trúc thư mục

```
CNTT/
├── .clinerules                 # Quy tắc và chính sách cho Cline
├── .env.example                # Mẫu biến môi trường
├── .gitignore                  # Danh sách file/thư mục bị bỏ qua
├── README.md                   # Tài liệu dự án
├── dashboard.py                # Dashboard Streamlit 4 tab tương tác
├── main.py                     # Chạy toàn bộ pipeline bằng 1 lệnh
├── requirements.txt            # Danh sách dependencies Python
├── data/
│   ├── external/               # Dữ liệu tham chiếu bên ngoài
│   │   └── vn_jobs_manual.csv  # 5 tin tuyển dụng VN thu thập thủ công
│   ├── raw/                    # Dữ liệu thô SO Survey (survey_results_public.csv KHÔNG commit vì >100MB — phải tải tay, xem mục Nguồn dữ liệu)
│   │   ├── 2019/               # Khảo sát SO 2019
│   │   │   └── survey_results_schema.csv  # Mô tả câu hỏi khảo sát (đã commit, file nhẹ)
│   │   ├── 2022/               # Khảo sát SO 2022
│   │   │   └── survey_results_schema.csv
│   │   └── 2025/               # Khảo sát SO 2025
│   │       └── survey_results_schema.csv
│   └── processed/              # Dữ liệu đã làm sạch (không commit — tự sinh khi chạy)
│       └── dashboard_data.pkl  # Cache cho dashboard Streamlit
├── scripts/                    # Script tiện ích
│   ├── build_processed_cache.py    # Build cache dữ liệu cho dashboard
│   ├── load_respondent_skills_only.py # Nạp respondent_skills vào SQL Server
│   └── setup_sql.py            # Tạo database + bảng SQL Server
├── figures/                    # Biểu đồ xuất ra (không commit — tự sinh khi chạy)
└── src/                        # Mã nguồn chính
    ├── config.py               # Hằng số đường dẫn và cấu hình
    ├── analysis/               # Phân tích số liệu
    │   ├── analyzer.py         # 5 hàm phân tích chính
    │   └── sql_analyzer.py     # 4 câu demo SQL Server
    ├── ingestion/              # Lấy dữ liệu đầu vào
    │   ├── survey_loader.py    # Load 3 năm SO Survey + COLUMN_MAPPING
    │   ├── vn_jobs_scraper.py  # Scraper VN jobs (chưa triển khai auto)
    │   └── sql_loader.py       # Nạp dữ liệu vào SQL Server
    ├── processing/             # Làm sạch và chuẩn hóa
    │   └── cleaner.py          # explode, lọc outlier, gộp nhóm
    └── visualization/          # Vẽ biểu đồ
        └── charts.py           # 5 loại biểu đồ xuất ra figures/
```

## Nguồn dữ liệu

- **Stack Overflow Developer Survey** các năm 2019, 2022, 2025 — tải qua Kaggle mirror (ghi rõ đây là bản mirror của dữ liệu chính thức survey.stackoverflow.co), giấy phép **Open Database License (ODbL)** — ghi nguồn khi trích dẫn kết quả.
  - **Cách tải:** tìm "Stack Overflow Developer Survey [năm]" trên kaggle.com, tải và đặt file `survey_results_public.csv` vào đúng thư mục `data/raw/2019/`, `data/raw/2022/`, `data/raw/2025/`. Không có 3 file này thì `main.py` và `build_processed_cache.py` sẽ báo lỗi `FileNotFoundError`.
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

### Phần kỹ thuật — hoàn thành
- [x] Thu thập dữ liệu SO Survey 2019/2022/2025 — đã xác minh đúng năm qua số dòng (88.883 / 73.268 / 49.123)
- [x] `survey_loader.py` — gộp 3 năm qua COLUMN_MAPPING (211.274 dòng x 275 cột), chuẩn hóa dấu nháy đơn toàn cục
- [x] `cleaner.py` — explode multi-select, lọc ngoại lai lương (IQR), gộp nhóm `remote_work` (4 nhóm) và `EdLevel` (11 nhóm); còn 202.739 dòng sau lọc
- [x] `analyzer.py` — 5 hàm: `compute_summary`, `analyze_salary_by_group`, `analyze_tech_demand`, `analyze_remote_work`, `compare_vn_vs_global_skills`
- [x] `charts.py` — 5 loại biểu đồ (line, bar ngang, bar chồng, bar nhóm, boxplot), xuất ra `figures/`
- [x] `main.py` — chạy toàn bộ pipeline bằng 1 lệnh, in tiến độ 5 bước
- [x] Dashboard Streamlit — 4 tab tương tác (Công nghệ / Lương / Làm việc từ xa / Học vấn), filter theo năm và quốc gia
- [x] Tích hợp SQL Server (nâng cao) — 4 bảng quan hệ, 4 câu demo GROUP BY / JOIN / window function / CTE+FULL OUTER JOIN
- [x] Dữ liệu tuyển dụng VN — 5 tin thu thập thủ công (`data/external/vn_jobs_manual.csv`)

### Phần báo cáo — đang thực hiện
- [x] Mục 3 — Kết quả phân tích (đã có số liệu và diễn giải đầy đủ cho 4 câu hỏi phân tích)
- [ ] Mục 1 — Giới thiệu
- [ ] Mục 2 — Dữ liệu và phương pháp
- [ ] Mục 4 — Hạn chế (có thể dùng lại mục "Hạn chế đã biết" cuối README này)
- [ ] Mục 5 — Kết luận
- [ ] Phụ lục — bảng phân công và tự đánh giá % đóng góp
- [ ] Đóng gói file nộp (DOCX + PDF + mã nguồn + dữ liệu)

### Câu hỏi phân tích đã trả lời
1. Xếp hạng công nghệ đã dùng vs mong muốn học — Rust (+2,9đ%), Go (+2,7đ%), Kotlin (+1,6đ%) dẫn đầu chênh lệch nhu cầu
2. Lương theo 4 chiều: kinh nghiệm, học vấn, quốc gia, ngôn ngữ lập trình
3. So sánh VN/Đông Nam Á với thế giới — PHP phổ biến hơn tương đối ở khu vực
4. Xu hướng làm việc từ xa 2019→2025 — tăng vọt 9,5%→34,6% (COVID-19) rồi giảm về 22,2%

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

## Dashboard (Streamlit)

Chạy 1 lần để tạo cache dữ liệu:
```powershell
.venv\Scripts\python.exe scripts\build_processed_cache.py
```

Sau đó mở dashboard:
```powershell
.venv\Scripts\python.exe -m streamlit run dashboard.py
```

Dashboard tự mở trên trình duyệt tại `http://localhost:8501`.

## Hạn chế đã biết

- Cỡ mẫu tin tuyển dụng VN nhỏ (5 tin) — kết quả so sánh VN vs toàn cầu chỉ mang tính minh họa, chưa đủ khái quát hóa.
- Cào tự động ITviec/TopCV không khả thi: robots.txt cho phép nhưng cả 2 trang không trả dữ liệu tin tuyển dụng trong HTML thô và không có API công khai ổn định (đã kiểm tra JSON-LD, __NEXT_DATA__, Algolia).
- Tỷ lệ không trả lời cao ở một số câu hỏi (remote_work: 19-31% tùy năm).
- Khảo sát 2022 không tách chi tiết mức độ hybrid như 2019/2025, nên các mức hybrid được gộp chung khi so sánh xuyên năm.
