# Dữ liệu

Kho mã này phân biệt **dữ liệu có thể tái phân phối** với **dữ liệu chỉ được truy xuất có kiểm soát**.

## Thư mục

- `metadata/`: danh mục nguồn, từ điển, dấu vân tay và quy tắc dữ liệu.
- `raw/`: chỉ dành cho nguồn được phép lưu công khai. Mọi tệp phải bất biến sau khi tải.
- `processed/`: bảng dẫn xuất tái tạo được bằng mã.
- dữ liệu bị hạn chế tái phân phối phải được tải khi chạy và không đưa tệp gốc vào Git.

## Tài liệu chuẩn

- `metadata/SR1_DATA_CATALOG.csv`: mọi nguồn đã xem xét và quyết định dùng/không dùng.
- `metadata/DATA_DICTIONARY_SR1.csv`: định nghĩa biến mục tiêu.
- `../docs/research/DATA_ACQUISITION_PLAN.md`: lý do khoa học và quy tắc giấy phép.

## Quy tắc

1. Không sửa dữ liệu nguồn bằng tay.
2. Mọi chuyển đổi nằm trong mã.
3. Mọi tệp nguồn có SHA-256.
4. Không nội suy dữ liệu chính thức bị thiếu nếu chưa có quyết định nghiên cứu.
5. Không tải tệp PCI gốc của VCCI lên kho công khai.
6. Không dùng địa giới 34 tỉnh sau năm 2025 cho giai đoạn nghiên cứu 2015–2023.
