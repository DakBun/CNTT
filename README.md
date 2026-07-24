# Phân tích thị trường việc làm ngành CNTT

Dự án phân tích dữ liệu thị trường việc làm ngành CNTT sử dụng Stack Overflow Developer Survey (2019-2025) và dữ liệu crawl từ ITviec/TopCV.

## Cấu trúc thư mục

```
CNTT/
├── .venv/                  # Virtual environment (không commit)
├── .env                    # Biến môi trường (không commit)
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── notebooks/              # Jupyter notebooks để khám phá và trình bày
├── src/
│   ├── __init__.py
│   ├── config.py           # Hằng số đường dẫn dùng chung
│   ├── ingestion/          # Lấy dữ liệu đầu vào
│   │   ├── __init__.py
│   │   ├── survey_loader.py
│   │   └── vn_jobs_scraper.py
│   ├── processing/         # Làm sạch và chuẩn hóa
│   │   ├── __init__.py
│   │   └── cleaner.py
│   ├── analysis/           # Phân tích số liệu
│   │   ├── __init__.py
│   │   └── analyzer.py
│   └── visualization/      # Vẽ biểu đồ xuất ra figures
│       ├── __init__.py
│       └── charts.py
├── data/
│   ├── raw/                # Dữ liệu thô từ survey / crawl
│   ├── processed/          # Dữ liệu đã làm sạch
│   └── external/           # Dữ liệu tham chiếu bên ngoài
└── figures/                # Sinh biểu đồ, ảnh xuất ra
```

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

## Ghi chú

- Không commit dữ liệu lớn trong `data/raw/` (đã cấu hình `.gitignore`).
- Sử dụng `src/config.py` để đảm bảo đường dẫn nhất quán, KHÔNG hard-code tuyệt đối.
- Tuân theo kiến trúc layered: `ingestion -> processing -> analysis -> visualization`.
