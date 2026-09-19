# Euréka 2026 — Thể chế địa phương và các cơ chế phát triển doanh nghiệp tại Việt Nam

Kho mã này phục vụ nghiên cứu dự thi **Giải thưởng Sinh viên Nghiên cứu khoa học Euréka 2026**.

## Câu hỏi nghiên cứu đang hoạt động

> **Những cơ chế thể chế cấp tỉnh đã được ghi nhận trong các nghiên cứu trước có còn tái hiện trong giai đoạn sau năm 2015 tại Việt Nam hay không; và nếu có, chúng biểu hiện qua biên gia nhập doanh nghiệp, quy mô doanh nghiệp, năng suất lao động, khả năng sinh lời, giá trị lao động và cường độ vốn nào?**

Đây là hướng nghiên cứu duy nhất đang hoạt động.

Hướng cũ — xếp hạng các thành phần PCI theo doanh thu tổng hợp và kiểm tra giá trị dự báo bằng học máy (machine learning — học máy) — **đã đóng**. Mã nguồn, kết quả và hiện vật cũ chỉ được giữ lại làm dấu vết kiểm toán và không còn được dùng làm câu hỏi nghiên cứu, đóng góp chính hay cơ sở để xây dựng kết luận.

## Kiến trúc khoa học mới

Nghiên cứu tập trung vào ba nhóm cơ chế:

- **Biên mở rộng**: gia nhập doanh nghiệp và mật độ doanh nghiệp.
- **Biên thâm dụng**: quy mô doanh nghiệp, doanh thu trên lao động và khả năng sinh lời.
- **Năng lực sản xuất**: thu nhập lao động và cường độ vốn.

Phân rã kế toán trung tâm:

[
\Delta \log(R) = \Delta \log(F) + \Delta \log(R/F)
]

[
\Delta \log(R/F) = \Delta \log(L/F) + \Delta \log(R/L)
]

trong đó (R) là doanh thu, (F) là số doanh nghiệp và (L) là lao động.

## Phương pháp chính

- hồi quy hiệu ứng cố định hai chiều (two-way fixed effects — hiệu ứng cố định theo tỉnh và năm);
- biến thể chế trễ một năm;
- sai số chuẩn gom cụm theo tỉnh;
- hiệu chỉnh đa kiểm định Benjamini–Hochberg;
- phân rã trong tỉnh và giữa tỉnh;
- mô hình độ trễ phân phối;
- kiểm định giả dược bằng giá trị thể chế tương lai;
- loại lần lượt tỉnh/năm;
- hoán vị quỹ đạo tỉnh;
- kiểm tra phụ thuộc chéo và không gian trước khi dùng mô hình không gian;
- đối chiếu PCI với PAPI như hai phép đo quản trị khác nhau.

Không sử dụng học máy (machine learning — học máy) như trụ cột đóng góp của bài mới.

## Dữ liệu đang mở rộng

Nguồn chính:
- PCI cấp tỉnh;
- PAPI cấp tỉnh;
- Tổng cục Thống kê / Cục Thống kê qua PX-Web: doanh nghiệp đang hoạt động, doanh nghiệp đăng ký mới, lao động, vốn, doanh thu, lợi nhuận, khả năng sinh lời, thu nhập lao động, tài sản cố định;
- dân số cấp tỉnh để chuẩn hóa mật độ doanh nghiệp.

Khoảng thời gian mục tiêu của bảng cơ chế chính: **2015–2023**. Phần gia nhập doanh nghiệp có thể có cửa sổ riêng tùy độ phủ chính thức.

## Trạng thái hiện tại

**Cổng nghiên cứu hiện tại: SR1 — kiểm định tính bền vững theo thời gian và cơ chế doanh nghiệp.**

Trước khi diễn giải hệ số cuối cùng phải:
1. xác minh và đóng băng nguồn dữ liệu;
2. đóng băng giả thuyết;
3. dựng bảng dữ liệu cơ chế có thể tái tạo;
4. chạy mô hình chính và bộ kiểm định phản chứng;
5. chỉ sau đó mới viết bản thảo cuối.

## Bắt đầu từ đây

1. `PROJECT_STATE.md`
2. `docs/research/PUBLISHABLE_REDESIGN_2026-09-19.md`
3. `docs/research/HYPOTHESES_SR1.md`
4. `docs/research/NEXT_EXPERIMENT.md`
5. `docs/research/QUALITY_GATES.md`
6. `DECISIONS.md`
7. `PROGRESS.md`
8. `docs/handover/RECOVERY_PROMPT.md`

Hạn đăng ký Euréka 2026 đang được theo dõi riêng trong tài liệu cuộc thi.
