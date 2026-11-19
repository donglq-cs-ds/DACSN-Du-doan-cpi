# Từ điển dữ liệu
# Từ điển dữ liệu

File: `data/processed/cpi_monthly_clean.csv` (250 dòng, từ 01/2006 đến 10/2026)

| Cột | Kiểu | Ý nghĩa | Ví dụ |
|---|---|---|---|
| date | ngày | Ngày đầu tháng quan sát | 2006-01-01 |
| mom | số thực | CPI so với tháng trước (tháng trước = 100) | 101.2 |
| pct | số thực | % thay đổi so với tháng trước, bằng mom - 100 | 1.2 |
| index | số thực | Chỉ số liên hoàn, kỳ gốc 01/2006 = 100 | 100.0 |

## Nguồn
- 01/2006 đến 12/2025: bảng V11.01 của cơ quan thống kê nhà nước (NSO), file `data/raw/cpi_2006_2025.xlsx`.
- 01/2026 đến 10/2026: bản tin hằng tháng của NSO, link từng tháng nằm trong `data/raw/cpi_2026_bo_sung.csv`.

## Thời điểm đóng băng
19/11/2026. Chỉ dùng dữ liệu đến tháng 10/2026, không dùng tháng 11 và 12.

## Kỳ gốc
01/2006 = 100. Chỉ số được dựng bằng công thức: index(t) = index(t-1) x mom(t) / 100.

## Ghi chú
- Năm 2006 và 2007 chỉ có 1 chữ số thập phân, các năm sau có 2 chữ số, nên độ chính xác không đồng đều.
- Hai cột `pct` và `index` do mã nguồn tính ra (file `cleaning.py`), không phải số công bố trực tiếp.