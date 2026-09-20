# BÀN GIAO CHO MÔ HÌNH NGÔN NGỮ TIẾP THEO

## Cập nhật phục hồi 20/09/2026 UTC

Nhánh hoạt động: `research/sr1-recovery-audit`, [PR16](https://github.com/Tienkhoaa2908/Eureka2026/pull/16), kế thừa PR13 và main. PR13 chưa merge; không dùng mô tả lỗi cũ thay cho log mới.

Đã tải 11 bảng doanh nghiệp NSO, lao động qua đào tạo, SCOLI và 7.560 giá trị thành phần PCI (63 tỉnh × 12 năm × 10 thành phần, không thiếu). Dân số đã tải CSV gốc, lỗi parser do tiêu đề `Total 2015`; nhãn năm 2024 là `Prel. 2024` cần giữ cờ sơ bộ. Đang sửa và chạy lại thu thập. Chưa có ước lượng nghiên cứu mới.

Khóa mô hình chưa được tạo. Các điểm chặn khoa học: phép đo PCI thay đổi; quần thể so sánh H4 chưa đồng nhất; E05.41 chưa khớp tỷ suất tự tính. Đọc `docs/research/RECOVERY_AUDIT_2026-09-20.md` và `docs/eureka/EUREKA_PROCEEDINGS_BENCHMARK.md` trước khi dùng các đặc tả dự kiến bên dưới. Các đặc tả này **chưa được khóa**.


Cập nhật: 2026-09-20

## 1. Không được khởi động lại từ hướng cũ

Hướng cũ “thành phần PCI nào mạnh nhất đối với doanh thu + học máy” đã đóng. Không được phục hồi nó dù thấy mã nguồn/kết quả trong lịch sử Git.

Câu hỏi chuẩn duy nhất:

> **Những cơ chế thể chế cấp tỉnh đã được ghi nhận trong các nghiên cứu trước có còn tái hiện trong giai đoạn sau năm 2015 tại Việt Nam hay không; và nếu có, chúng biểu hiện qua biên gia nhập doanh nghiệp, quy mô doanh nghiệp, doanh thu trên lao động, khả năng sinh lời, giá trị lao động và cường độ vốn nào?**

## 2. Đọc theo đúng thứ tự

1. `PROJECT_STATE.md`
2. `LLM_HANDOFF.md` (tệp này)
3. `docs/research/RESEARCH_PROTOCOL_SR1.md`
4. `docs/research/HYPOTHESES_SR1.md`
5. `docs/research/DATA_ACQUISITION_PLAN.md`
6. `data/metadata/SR1_DATA_CATALOG.csv`
7. `data/metadata/DATA_DICTIONARY_SR1.csv`
8. `docs/research/QUALITY_GATES.md`
9. `docs/research/NEXT_EXPERIMENT.md`
10. kiểm tra nhánh, yêu cầu hợp nhất, vấn đề và kiểm thử tự động hiện tại.

## 3. Trạng thái mã nguồn

Yêu cầu hợp nhất số 13 là nhánh triển khai SR1:
`research/sr1-mechanism`.

Nó chứa:
- `src/eureka2026/sr1_fetch.py`: tải dữ liệu NSO và PCI;
- `src/eureka2026/sr1_build.py`: dựng bảng cơ chế;
- `src/eureka2026/sr1_models.py`: chạy mô hình đã khóa;
- `tests/test_sr1.py`;
- quy trình GitHub Actions để chạy thu thập dữ liệu trực tuyến.

Không được hợp nhất PR #13 nếu quy trình trực tuyến chưa chạy qua toàn bộ các bước thu thập → dựng bảng → mô hình → tải hiện vật.

## 4. Điểm chặn kỹ thuật gần nhất

PX-Web của NSO cho phép giao diện web tải CSV nhưng điểm cuối API chuẩn đã trả 404 trong môi trường GitHub Actions.

Giải pháp đang triển khai:
- gửi biểu mẫu ASP.NET công khai của PX-Web;
- giữ `__VIEWSTATE`, `__EVENTVALIDATION`;
- chọn đúng 63 tỉnh lịch sử;
- chọn năm;
- yêu cầu định dạng CSV có tiêu đề;
- lưu cả bản xuất nguồn, bản chuẩn hóa và SHA-256.

Nếu lần chạy mới thất bại, đọc log của bước “Acquire official NSO and PCI data” trước khi sửa.

## 5. Nguồn dữ liệu bắt buộc

Khối doanh nghiệp NSO:
E05.02, E05.04, E05.05, E05.08, E05.11, E05.17, E05.23, E05.35, E05.38, E05.41, E05.44.

Khối bổ sung:
- E02.03-07 dân số;
- E02.55 lao động qua đào tạo;
- E11.23 chỉ số giá sinh hoạt theo không gian;
- PCI thành phần;
- PAPI lõi sau kiểm tra tính so sánh;
- ranh giới 63 tỉnh trước 2025 cho chẩn đoán không gian.

## 6. Giấy phép

Không đưa tệp PCI gốc của VCCI vào kho công khai. Chính sách VCCI hạn chế chia sẻ lại/đóng gói lại trái phép.

PAPI cho tải dữ liệu tổng hợp; dữ liệu vi mô cấp cá nhân cần yêu cầu UNDP và điều khoản riêng.

Dữ liệu NSO được lấy trực tiếp từ bảng công khai và phải lưu đường dẫn/hàm băm.

## 7. Nguyên tắc khoa học

- Không chọn giả thuyết sau khi xem hệ số.
- Không gọi quan hệ là nhân quả.
- Không dùng học máy làm novelty.
- Không thêm biến kiểm soát nếu chưa phân loại nó trong sơ đồ cơ chế.
- Không dùng dữ liệu 34 tỉnh sau 2025 cho bảng 63 tỉnh lịch sử.
- Không nội suy năm thiếu.
- Không giấu kết quả bằng không.
- Không báo số nếu không tái tạo được bằng mã và dấu vân tay dữ liệu.

## 8. Việc cần làm ngay sau khi tiếp quản

1. Xem PR #13 và lần chạy mới nhất.
2. Làm cho bộ tải NSO chạy hết các bảng.
3. Kiểm tra độ phủ 63 tỉnh × năm cho từng series.
4. Kiểm tra mẫu số/tử số trước khi dựng tỷ lệ.
5. Tải và kiểm tra PAPI lõi 2015–2023.
6. Thêm ranh giới lịch sử và dựng ma trận láng giềng.
7. Khóa phiên bản dữ liệu bằng SHA-256.
8. Chỉ sau đó chạy mô hình H1–H3.
9. H5 PAPI chỉ chạy sau khi khóa cặp khái niệm.
10. Cập nhật `PROJECT_STATE.md` trước khi bàn giao lần nữa.

## 9. Điều không được làm

Không quay lại bản thảo cũ, không trích kết quả CSTP5 cũ làm bằng chứng xác nhận H2, không cherry-pick, không thêm XGBoost/Rừng ngẫu nhiên chỉ để trông hiện đại.
