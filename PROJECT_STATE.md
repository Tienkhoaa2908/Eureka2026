# TRẠNG THÁI DỰ ÁN — Euréka 2026

## Cập nhật phục hồi 20/09/2026 UTC

Nhánh hoạt động: `research/sr1-recovery-audit`, [PR16](https://github.com/Tienkhoaa2908/Eureka2026/pull/16), kế thừa PR13 và main. PR13 chưa merge; không dùng mô tả lỗi cũ thay cho log mới.

Đã tải 11 bảng doanh nghiệp NSO, lao động qua đào tạo, SCOLI và 7.560 giá trị thành phần PCI (63 tỉnh × 12 năm × 10 thành phần, không thiếu). Dân số đã tải CSV gốc, lỗi parser do tiêu đề `Total 2015`; nhãn năm 2024 là `Prel. 2024` cần giữ cờ sơ bộ. Đang sửa và chạy lại thu thập. Chưa có ước lượng nghiên cứu mới.

Khóa mô hình chưa được tạo. Các điểm chặn khoa học: phép đo PCI thay đổi; quần thể so sánh H4 chưa đồng nhất; E05.41 chưa khớp tỷ suất tự tính. Đọc `docs/research/RECOVERY_AUDIT_2026-09-20.md` và `docs/eureka/EUREKA_PROCEEDINGS_BENCHMARK.md` trước khi dùng các đặc tả dự kiến bên dưới. Các đặc tả này **chưa được khóa**.


Cập nhật: 2026-09-20 (UTC+7)

Trạng thái: **hướng cũ đã đóng; hướng cơ chế và tính bền vững theo thời gian là hướng nghiên cứu duy nhất đang hoạt động.**

## 1. Câu hỏi nghiên cứu chính

> **Những cơ chế thể chế cấp tỉnh đã được ghi nhận trong các nghiên cứu trước có còn tái hiện trong giai đoạn sau năm 2015 tại Việt Nam hay không; và nếu có, chúng biểu hiện qua biên gia nhập doanh nghiệp, quy mô doanh nghiệp, năng suất lao động, khả năng sinh lời, giá trị lao động và cường độ vốn nào?**

Mục tiêu không còn là tìm “thành phần PCI mạnh nhất” và cũng không còn là chứng minh rằng PCI cải thiện dự báo doanh thu.

## 2. Trạng thái của hướng cũ

Hướng cũ gồm:
- doanh thu doanh nghiệp cấp tỉnh là biến kết quả trung tâm;
- hồi quy mười thành phần PCI trên doanh thu;
- so sánh mô hình học máy (machine learning — học máy);
- đánh giá giá trị dự báo ngoài mẫu;
- thử diễn giải một thành phần PCI nổi bật.

Hướng này **đã đóng vĩnh viễn như một hướng nghiên cứu**.

Các cổng G1–G6, mã nguồn, kết quả và hiện vật trước đây vẫn được giữ nguyên để bảo toàn khả năng kiểm toán. Chúng chỉ là **tư liệu lưu trữ**, không còn là đóng góp chính, không còn quyết định tiêu đề, câu hỏi, giả thuyết hay kết luận của bài mới.

## 3. Kiến trúc khoa học đang hoạt động

### 3.1. Tính bền vững theo thời gian

Đối chiếu các cơ chế đã được nghiên cứu trong giai đoạn trước với dữ liệu hậu 2015 để xem dấu hiệu có tái hiện hay không.

### 3.2. Phân rã cơ chế doanh nghiệp

Các biên kết quả chính:
- gia nhập và mật độ doanh nghiệp;
- quy mô doanh nghiệp;
- doanh thu trên lao động;
- khả năng sinh lời;
- thu nhập lao động;
- vốn trên lao động.

Phân rã kế toán bắt buộc:

[
\Delta \log(R)=\Delta \log(F)+\Delta \log(R/F)
]

[
\Delta \log(R/F)=\Delta \log(L/F)+\Delta \log(R/L)
]

Không được gọi doanh thu trên lao động là năng suất nhân quả; đây là chỉ báo hiệu quả hoạt động ở cấp tổng hợp.

### 3.3. Đối chiếu phép đo quản trị

PCI là phép đo hướng tới môi trường kinh doanh. PAPI là phép đo trải nghiệm quản trị của người dân. Hai hệ đo được dùng để kiểm tra tính hội tụ của bằng chứng, không được xem là thay thế cho nhau.

## 4. Dữ liệu chính cần xây dựng

Bảng dữ liệu mục tiêu ghép theo tỉnh-năm:
- PCI;
- PAPI có tính so sánh theo thời gian;
- số doanh nghiệp đang hoạt động;
- doanh nghiệp đăng ký mới;
- lao động doanh nghiệp;
- vốn kinh doanh;
- doanh thu thuần;
- lợi nhuận trước thuế;
- tỷ suất lợi nhuận;
- thu nhập bình quân lao động;
- tài sản cố định trên lao động;
- dân số.

Khoảng thời gian ưu tiên: **2015–2023** cho bảng cơ chế chính. Cửa sổ gia nhập doanh nghiệp được xác định theo độ phủ dữ liệu chính thức.

## 5. Phương pháp luận chính

Mô hình cơ sở:
- hiệu ứng cố định tỉnh và năm (two-way fixed effects — hiệu ứng cố định hai chiều);
- chỉ số quản trị trễ một năm;
- chuẩn hóa trong từng năm ở đặc tả chính;
- sai số chuẩn gom cụm theo tỉnh;
- hiệu chỉnh tỷ lệ phát hiện sai Benjamini–Hochberg theo từng họ giả thuyết.

Bộ kiểm tra bắt buộc:
- điểm số thô thay cho chuẩn hóa;
- biến đồng thời;
- độ trễ một và hai năm;
- loại giai đoạn 2020–2022;
- phân rã trong tỉnh và giữa tỉnh;
- biến quản trị tương lai làm kiểm định giả dược;
- loại lần lượt tỉnh và năm;
- hoán vị quỹ đạo tỉnh;
- kiểm tra phụ thuộc chéo và không gian.

Mô hình động, mô hình không gian, hồi quy lượng tử hoặc phương pháp học máy nhân quả chỉ được mở nếu chẩn đoán và điều kiện nhận dạng thực sự yêu cầu.

## 6. Giả thuyết đang hoạt động

- H1: chi phí gia nhập, tính minh bạch và thiết chế pháp lý liên hệ với gia nhập/mật độ doanh nghiệp.
- H2: chi phí thời gian và chi phí không chính thức liên hệ với doanh thu trên lao động, lợi nhuận và doanh thu trên doanh nghiệp.
- H3: hỗ trợ doanh nghiệp và chính sách lao động liên hệ với doanh thu trên lao động, thu nhập lao động và cường độ vốn.
- H4: các cơ chế trên được kiểm tra tính tái hiện trong giai đoạn hậu 2015 so với bằng chứng trước đó.
- H5: PAPI chỉ được dùng làm lớp đối chiếu thứ cấp sau khi khóa tính so sánh theo thời gian.

Chi tiết: `docs/research/HYPOTHESES_SR1.md`.

## 7. Cổng hiện tại

**SR1 — TÍNH BỀN VỮNG THEO THỜI GIAN VÀ CƠ CHẾ DOANH NGHIỆP.**

Điều kiện để đi tiếp:
- nguồn dữ liệu chính thức có nguồn gốc và hàm băm;
- bảng cơ chế ghép được và kiểm toán được;
- giả thuyết được khóa trước khi đọc kết quả cuối;
- phân rã kế toán khớp số học;
- kết quả chính không phụ thuộc một tỉnh, một năm hay một đặc tả;
- kết quả phản chứng được báo cáo đầy đủ, kể cả khi làm yếu câu chuyện.

## 8. Việc tiếp theo duy nhất

Thực hiện `docs/research/NEXT_EXPERIMENT.md`: hoàn tất thu thập dữ liệu chính thức, khóa từ điển dữ liệu, dựng bảng cơ chế và chỉ sau đó mới chạy ước lượng chính.

## 9. Thứ tự phục hồi

1. `PROJECT_STATE.md`
2. `docs/research/PUBLISHABLE_REDESIGN_2026-09-19.md`
3. `docs/research/HYPOTHESES_SR1.md`
4. `docs/research/QUALITY_GATES.md`
5. `DECISIONS.md`
6. `EXPERIMENTS.md`
7. `PROGRESS.md`
8. `CHANGELOG.md`
9. `docs/research/NEXT_EXPERIMENT.md`
10. nhánh, yêu cầu hợp nhất, vấn đề và trạng thái kiểm thử hiện tại.

Không dùng bản thảo của hướng cũ để phục hồi câu hỏi nghiên cứu.
