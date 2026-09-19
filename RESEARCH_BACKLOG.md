# Danh sách việc nghiên cứu đang mở

Mọi mục ở đây phải được xử lý theo thứ tự cổng chất lượng, không theo độ hấp dẫn của mô hình.

## P0 — dữ liệu

- [ ] PR #13 tải thành công tất cả bảng NSO bắt buộc bằng giao diện PX-Web.
- [ ] Xác minh từng bảng có đủ 63 tỉnh lịch sử cho đúng năm cần dùng.
- [ ] So sánh E05.05 với mật độ tự dựng từ E05.04 / E02.03-07.
- [ ] Xác minh định nghĩa E05.41 trước khi so với profit/revenue.
- [ ] Kiểm tra E11.23 có đủ 2015–2023 cho 63 tỉnh.
- [ ] Tải PAPI aggregate 2015–2023.
- [ ] Lập bảng mapping chỉ báo PAPI “lõi” qua các năm.
- [ ] Tải ranh giới 63 tỉnh trước 2025 và tạo ma trận láng giềng.
- [ ] Ghi SHA-256 cho mọi nguồn.

## P1 — chất lượng bảng cơ chế

- [ ] Kiểm tra khóa tỉnh-năm duy nhất.
- [ ] Kiểm tra đơn vị tiền tệ và hệ số nghìn/triệu/tỷ.
- [ ] Kiểm tra doanh nghiệp/worker denominator cùng universe.
- [ ] Kiểm tra accounting identity.
- [ ] Kiểm tra profit âm, zero và phép asinh.
- [ ] Kiểm tra outlier nhưng không winsorize mặc định.
- [ ] Tạo bảng missingness theo series/năm/tỉnh.
- [ ] Đóng băng sample chính của từng H1/H2/H3.

## P2 — suy luận

- [ ] Chạy FE hai chiều đặc tả chính.
- [ ] BH theo family.
- [ ] Within-between.
- [ ] Distributed lag.
- [ ] Future lead placebo.
- [ ] Leave-one-province/year.
- [ ] Trajectory permutation.
- [ ] Robustness bằng SCOLI cho outcome tiền tệ.
- [ ] Chẩn đoán phụ thuộc chéo.

## P3 — không gian và đối chiếu

- [ ] Nếu SR5 mở: dựng contiguity matrix.
- [ ] Kiểm tra độ nhạy distance matrix.
- [ ] PAPI H5 sau khi khóa mapping.
- [ ] So kết quả hậu 2015 với Bach 2017, Huynh 2022, Ha 2024, Thoa & Hung 2026, ADB 2026.

## P4 — viết bài

- [ ] Chốt claim theo evidence thật.
- [ ] Viết lại manuscript từ đầu.
- [ ] Không tái sử dụng bản thảo cũ.
- [ ] Tạo bảng/figure hoàn toàn từ artifact mới.
- [ ] Kiểm tra mọi số trong bài có nguồn artifact.
