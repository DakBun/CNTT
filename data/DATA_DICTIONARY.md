# Data Dictionary

Mô tả các trường dữ liệu chính dùng trong phân tích (DataFrame sau `load_all_years` + làm sạch).

| Tên trường | Ý nghĩa | Giá trị / đơn vị | Ghi chú |
|---|---|---|---|
| `survey_year` | Năm khảo sát | 2019, 2022, 2025 | Thêm vào trong `survey_loader.py` |
| `Country` | Quốc gia người được hỏi | Tên quốc gia | Giữ nguyên theo survey |
| `EdLevel` | Trình độ học vấn | Các mức giá trị đã gộp nhóm | Multi-choice không áp dụng; đã gộp qua `EDLEVEL_GROUPS` |
| `DevType` | Loại hình công việc | Danh sách giá trị phân cách bằng `;` | Multi-select |
| `YearsCode` | Số năm kinh nghiệm lập trình | Số năm (0–50+) | Dùng `pd.cut()` để thành `experience_group` |
| `experience_group` | Nhóm kinh nghiệm | 0-2 năm / 3-5 năm / 6-10 năm / 11-20 năm / 20+ năm | Tạo trong cleaner |
| `salary_usd` | Lương đã quy đổi sang USD | USD/năm | NaN = không trả lời; đã lọc ngoại lai IQR |
| `remote_work` | Hình thức làm việc từ xa | 4 nhóm: Toàn thời gian từ xa / Hybrid / Hầu như tại văn phòng / Khác/linh hoạt | Đã gộp qua `REMOTE_WORK_GROUPS` |
| `OrgSize` | Quy mô công ty | Nhỏ / vừa / lớn... | Multi-select không áp dụng |
| `Age` | Độ tuổi | Số nguyên hoặc nhóm tuổi | Dạng chuỗi |
| `languages_used` | Ngôn ngữ đã dùng | Danh sách phân cách bởi `;` | Multi-select |
| `languages_wanted` | Ngôn ngữ muốn học | Danh sách phân cách bởi `;` | Multi-select |

Ghi chú chung:
- Cột multi-select: `DevType`, `languages_used`, `languages_wanted`, `databases_used`, `webframes_used`.
- Cột đã gộp nhóm: `EdLevel` (11 nhóm), `remote_work` (4 nhóm).

## Dữ liệu tuyển dụng VN (`vn_jobs_manual.csv`)

| Tên trường | Ý nghĩa | Giá trị / đơn vị |
|---|---|---|
| `job_title` | Tiêu đề tin tuyển dụng | Chuỗi |
| `company` | Tên công ty | Chuỗi |
| `required_skills` | Kỹ năng yêu cầu | Danh sách phân cách bởi `;` |
| `location` | Địa điểm làm việc | Chuỗi |
| `posted_date` | Ngày đăng | Chuỗi (định dạng gốc) |
