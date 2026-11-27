# Phân tích và dự báo ngắn hạn CPI hàng tháng của Việt Nam

**Đồ án cơ sở ngành** - Trường Đại học Nha Trang, Khoa Công nghệ thông tin

- Sinh viên: Lê Quang Đông - MSSV 66130564 - Lớp 66.KHMT
- Giảng viên hướng dẫn: TS. Phạm Văn Nam

## Mục tiêu

Làm sạch chuỗi CPI hàng tháng của Việt Nam, tự cài đặt các mô hình dự báo ngắn hạn
(Naive, Seasonal Naive, trung bình trượt, hồi quy xu hướng OLS), đánh giá theo đúng thứ tự
thời gian (rolling-origin, tầm 1, 3, 6 tháng) bằng MAE và MAPE, chẩn đoán sai số và làm một
thí nghiệm rò rỉ dữ liệu.

## Dữ liệu

- 01/2006 đến 12/2025: bảng chỉ số giá tiêu dùng (tháng trước = 100) của cơ quan thống kê nhà nước.
- 01/2026 đến 10/2026: nhập tay từ các bản tin hằng tháng của Cục Thống kê (đường dẫn từng tháng nằm trong `data/raw/cpi_2026_bo_sung.csv`).
- Dữ liệu được đóng băng ngày 19/11/2026: 250 quan sát, 01/2006 đến 10/2026.
- Kỳ gốc của chuỗi chỉ số do ta dựng: 01/2006 = 100. Chi tiết cột xem `docs/data_dictionary.md`.

## Kết quả chính

Sai số MAE của đánh giá rolling-origin (càng nhỏ càng tốt). Đầy đủ MAE và MAPE nằm trong `results/tables/`.

**Chuỗi chỉ số** (đơn vị: điểm chỉ số):

| Mô hình | h = 1 | h = 3 | h = 6 |
|---|---|---|---|
| Naive | 1,114 | 2,895 | 5,047 |
| Seasonal Naive | 10,493 | 10,403 | 10,134 |
| Trung bình trượt (k=3) | 1,985 | 3,633 | 5,849 |
| Hồi quy xu hướng (OLS) | 13,791 | 14,660 | 15,886 |

**Chuỗi % thay đổi so với tháng trước** (đơn vị: điểm phần trăm; MAPE không xác định vì có tháng bằng 0):

| Mô hình | h = 1 | h = 3 | h = 6 |
|---|---|---|---|
| Naive | 0,375 | 0,526 | 0,534 |
| Seasonal Naive | 0,517 | 0,520 | 0,493 |
| Trung bình trượt (k=3) | 0,406 | 0,451 | 0,453 |
| Hồi quy xu hướng (OLS) | 0,418 | 0,424 | 0,418 |

Nhận xét ngắn: trên chuỗi chỉ số Naive tốt nhất ở cả ba tầm; trên chuỗi % thay đổi Naive tốt nhất
ở tầm 1 tháng còn hồi quy xu hướng nhỉnh hơn ở tầm 3 và 6 tháng. Mô hình tốt nhất phụ thuộc vào
chuỗi được dự báo và tầm dự báo.

## Cài đặt

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Chạy lại toàn bộ quy trình

```bash
python scripts/run_all.py
```

Lệnh này làm sạch dữ liệu, đánh giá 4 mô hình, chẩn đoán sai số, chạy thí nghiệm rò rỉ dữ liệu,
bóc tách xu hướng và mùa vụ, rồi ghi bảng vào `results/tables/` và hình vào `results/figures/`.

## Kiểm thử

```bash
python -m pytest
```

## Cấu trúc thư mục

| Thư mục | Nội dung |
|---|---|
| `data/raw` | Dữ liệu gốc (không sửa) |
| `data/processed` | Dữ liệu đã làm sạch: `cpi_monthly_clean.csv` |
| `src/cpi_forecast/data` | Đọc và gộp dữ liệu (`loader.py`), kiểm tra và dựng chỉ số (`cleaning.py`) |
| `src/cpi_forecast/models` | Bốn mô hình dự báo |
| `src/cpi_forecast/evaluation` | Chia dữ liệu, MAE/MAPE, rolling-origin, chẩn đoán sai số, rò rỉ dữ liệu |
| `src/cpi_forecast/analysis` | Bóc tách xu hướng và mùa vụ |
| `notebooks` | Năm notebook trình bày từng bước (01 đến 05) |
| `scripts` | `run_all.py`: chạy trọn quy trình |
| `tests` | Kiểm thử các hàm tự viết |
| `results` | Bảng và hình kết quả |
| `docs` | Từ điển dữ liệu, nhật ký họp, báo cáo |

## Chưa làm (phần mở rộng, chỉ làm nếu còn thời gian)

Các file `seasonal_index.py`, `exp_smoothing.py`, `holt.py` trong `src/cpi_forecast/models` và
`app/streamlit_app.py` mới là khung rỗng.

## Tài liệu tham khảo

- Tài liệu chính thức của Python, NumPy, pandas, Matplotlib.
- Hyndman, R. J. và Athanasopoulos, G. *Forecasting: Principles and Practice* (ấn bản 3, 2021), OTexts.
- Số liệu chỉ số giá tiêu dùng của cơ quan thống kê nhà nước.