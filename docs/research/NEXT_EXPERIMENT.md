# THÍ NGHIỆM TIẾP THEO — SR1-CƠ-CHẾ-01

## Cập nhật phục hồi 20/09/2026 UTC

Nhánh hoạt động: `research/sr1-recovery-audit`, [PR16](https://github.com/Tienkhoaa2908/Eureka2026/pull/16), kế thừa PR13 và main. PR13 chưa merge; không dùng mô tả lỗi cũ thay cho log mới.

Đã tải 11 bảng doanh nghiệp NSO, lao động qua đào tạo, SCOLI và 7.560 giá trị thành phần PCI (63 tỉnh × 12 năm × 10 thành phần, không thiếu). Dân số đã tải CSV gốc, lỗi parser do tiêu đề `Total 2015`; nhãn năm 2024 là `Prel. 2024` cần giữ cờ sơ bộ. Đang sửa và chạy lại thu thập. Chưa có ước lượng nghiên cứu mới.

Khóa mô hình chưa được tạo. Các điểm chặn khoa học: phép đo PCI thay đổi; quần thể so sánh H4 chưa đồng nhất; E05.41 chưa khớp tỷ suất tự tính. Đọc `docs/research/RECOVERY_AUDIT_2026-09-20.md` và `docs/eureka/EUREKA_PROCEEDINGS_BENCHMARK.md` trước khi dùng các đặc tả dự kiến bên dưới. Các đặc tả này **chưa được khóa**.


Ưu tiên: P0

## Câu hỏi

Những cơ chế thể chế cấp tỉnh đã được ghi nhận trước đây có còn tái hiện sau năm 2015, và nếu có thì xuất hiện trên biên doanh nghiệp nào?

## Giai đoạn A — khóa dữ liệu

Thu thập trực tiếp từ nguồn chính thức, không chép tay:
- V05.02: doanh nghiệp đăng ký mới;
- V05.08: doanh nghiệp đang hoạt động có kết quả sản xuất kinh doanh;
- V05.11: lao động trong doanh nghiệp;
- V05.17: vốn kinh doanh bình quân năm;
- V05.23: doanh thu thuần;
- V05.35: thu nhập bình quân tháng của lao động;
- V05.38: lợi nhuận trước thuế;
- V05.41: tỷ suất lợi nhuận;
- V05.44: tài sản cố định trên lao động;
- dân số cấp tỉnh;
- PCI hằng năm;
- PAPI hằng năm với ghi chú về tính so sánh theo thời gian.

Mỗi nguồn phải có mã bảng, đơn vị, đường dẫn, ngày cập nhật và SHA-256.

## Giai đoạn B — dựng bảng cơ chế

Mục tiêu chính: 2015–2023.

Biến kết quả:
- số doanh nghiệp đang hoạt động;
- mật độ doanh nghiệp;
- tỷ lệ gia nhập doanh nghiệp;
- doanh thu trên doanh nghiệp;
- lao động trên doanh nghiệp;
- doanh thu trên lao động;
- lợi nhuận trên doanh nghiệp;
- biên lợi nhuận;
- vốn trên doanh nghiệp;
- vốn trên lao động;
- thu nhập lao động.

Không nội suy năm thiếu từ nguồn chính thức.

## Giai đoạn C — kiểm tra phân rã kế toán

Trên cùng một mẫu cân bằng, xác minh:

[
\Delta \log(R)=\Delta \log(F)+\Delta \log(R/F)
]

[
\Delta \log(R/F)=\Delta \log(L/F)+\Delta \log(R/L)
]

Sai số số học phải nằm trong ngưỡng dung sai được ghi trước.

## Giai đoạn D — khóa giả thuyết

Dùng `docs/research/HYPOTHESES_SR1.md`.

Không chạy lưới mười thành phần PCI nhân với mọi biến kết quả để chọn ô có ý nghĩa thống kê.

## Giai đoạn E — ước lượng chính

Cho từng họ giả thuyết đã định trước:
- hiệu ứng cố định tỉnh và năm (two-way fixed effects — hiệu ứng cố định hai chiều);
- chỉ số quản trị trễ một năm;
- điểm chuẩn hóa theo năm ở đặc tả chính;
- sai số chuẩn gom cụm theo tỉnh;
- Benjamini–Hochberg trong từng họ giả thuyết;
- phân rã trong tỉnh và giữa tỉnh;
- độ trễ một và hai năm;
- loại 2020–2022;
- kiểm định giả dược bằng biến quản trị tương lai;
- loại lần lượt tỉnh và năm;
- hoán vị quỹ đạo tỉnh;
- kiểm tra phụ thuộc chéo và không gian.

## Tiêu chí qua cổng

Không yêu cầu phải có kết quả dương.

Một cơ chế chỉ được đưa vào kết luận chính khi:
- hướng dấu phù hợp với cơ chế lý thuyết đã định trước;
- vượt hiệu chỉnh đa kiểm định ở đặc tả chính;
- không bị đảo dấu bởi một tỉnh hay một năm;
- kiểm định giả dược không tạo tín hiệu mâu thuẫn tương đương;
- bằng chứng hoán vị không phủ nhận tín hiệu;
- các thất bại ở đặc tả thay thế được báo cáo công khai;
- có tính tái hiện hợp lý so với bằng chứng trước hoặc có lý do dữ liệu/thể chế rõ ràng cho sự khác biệt.

## Đầu ra bắt buộc

- bản kê nguồn và hàm băm;
- từ điển dữ liệu;
- bảng cơ chế chuẩn;
- báo cáo kiểm tra phân rã;
- bảng hệ số theo từng họ giả thuyết;
- kết quả trong/giữa tỉnh;
- kết quả độ trễ;
- kết quả giả dược và hoán vị;
- đối chiếu PAPI nếu vượt kiểm tra tính so sánh;
- báo cáo kiểm định chất lượng `artifacts/qa/SCIENCE-REDESIGN-01.md`.

## Quy tắc dừng

Không quay lại bài toán xếp hạng PCI theo doanh thu và không khôi phục học máy (machine learning — học máy) làm đóng góp trung tâm chỉ vì kết quả cơ chế yếu hoặc bằng không.
