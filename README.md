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

## Cách chạy notebook

```powershell
jupyter notebook
```

Mở file `.ipynb` trong thư mục `notebooks/` để bắt đầu phân tích.

Lưu ý: nếu `jupyter notebook` bị lỗi cài đặt (timeout mạng), có thể chạy trực tiếp các module bằng:

```powershell
.venv\Scripts\python.exe -c "from src.ingestion.survey_loader import load_all_years; df = load_all_years([2019, 2022, 2025]); print(df.shape)"
```

hoặc chỉ cài `ipykernel` (nhẹ hơn `jupyter` đầy đủ) nếu dùng notebook trong VS Code.

## Ghi chú

- Không commit dữ liệu lớn trong `data/raw/` (đã cấu hình `.gitignore`).
- Sử dụng `src/config.py` để đảm bảo đường dẫn nhất quán, KHÔNG hard-code tuyệt đối.
- Tuân theo kiến trúc layered: `ingestion -> processing -> analysis -> visualization`.

## Trạng thái hiện tại

- [x] Thu thập dữ liệu SO Survey (2019, 2022, 2025) — đã xác minh đúng năm qua số dòng dữ liệu
- [x] `load_all_years()` — gộp 3 năm thành 1 DataFrame (211,274 dòng x 277 cột)
- [ ] `cleaner.py` — đang làm (explode multi-select, lọc outlier lương)
- [ ] `vn_jobs_scraper.py` — đã có khung, chưa triển khai
- [ ] `analyzer.py`, `charts.py` — chưa bắt đầu
