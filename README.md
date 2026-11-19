# Phân tích và dự báo ngắn hạn CPI hàng tháng của Việt Nam

**Đồ án cơ sở ngành** - Trường Đại học Nha Trang, Khoa Công nghệ thông tin

- Sinh viên: Lê Quang Đông - MSSV 66130564 - Lớp 66.KHMT
- GVHD: TS. Phạm Văn Nam

## Mục tiêu
Làm sạch chuỗi CPI hàng tháng của Việt Nam, tự cài đặt các mô hình dự báo ngắn hạn
(Naive, Seasonal Naive, trung bình trượt, hồi quy xu hướng OLS), đánh giá theo đúng
thứ tự thời gian (rolling-origin, tầm 1/3/6 tháng) bằng MAE/MAPE, chẩn đoán phần dư
và làm thí nghiệm rò rỉ dữ liệu.

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

## Cấu trúc thư mục
| Thư mục | Nội dung |
|---|---|
| `data/raw` | Dữ liệu gốc từ cơ quan thống kê (không sửa) |
| `data/processed` | Dữ liệu đã làm sạch |
| `src/cpi_forecast` | Mã nguồn: làm sạch, mô hình, đánh giá |
| `notebooks` | Các notebook trình bày từng bước |
| `tests` | Kiểm thử các hàm tự viết |
| `results` | Hình và bảng kết quả đưa vào báo cáo |
| `docs` | Từ điển dữ liệu, nhật ký họp, báo cáo |
| `app` | Dashboard Streamlit (nếu còn thời gian) |

## Tài liệu tham khảo
- Tài liệu Python, NumPy, pandas, Matplotlib.
- Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*.
- Số liệu CPI do cơ quan thống kê nhà nước công bố.
