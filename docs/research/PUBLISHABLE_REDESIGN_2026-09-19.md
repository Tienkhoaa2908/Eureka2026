# Thiết kế khoa học đang hoạt động — 2026-09-20

Trạng thái: **HƯỚNG NGHIÊN CỨU CHÍNH DUY NHẤT.**

## 1. Câu hỏi nghiên cứu

> **Những cơ chế thể chế cấp tỉnh đã được ghi nhận trong các nghiên cứu trước có còn tái hiện trong giai đoạn sau năm 2015 tại Việt Nam hay không; và nếu có, chúng biểu hiện qua biên gia nhập doanh nghiệp, quy mô doanh nghiệp, năng suất lao động, khả năng sinh lời, giá trị lao động và cường độ vốn nào?**

Hướng này thay thế hoàn toàn câu hỏi cũ về thành phần PCI nào liên hệ mạnh nhất với doanh thu và liệu PCI có cải thiện dự báo bằng học máy (machine learning — học máy) hay không.

## 2. Đóng góp khoa học mục tiêu

Đóng góp không nằm ở việc dùng thuật toán mới. Bài nghiên cứu cố gắng trả lời ba vấn đề có thể kiểm chứng:

1. **Tính bền vững theo thời gian:** cơ chế từng được báo cáo trong giai đoạn trước có còn xuất hiện sau năm 2015 không.
2. **Vị trí của cơ chế:** quan hệ thể chế xuất hiện ở gia nhập, quy mô, doanh thu trên lao động, lợi nhuận, thu nhập lao động hay cường độ vốn.
3. **Tính hội tụ phép đo:** bằng chứng từ PCI có được đối chiếu bởi PAPI hay không, với điều kiện hai thước đo được giữ đúng bản chất khác nhau.

## 3. Khung cơ chế

### Gia nhập và mật độ doanh nghiệp
Chi phí gia nhập, minh bạch và thiết chế pháp lý có thể làm thay đổi chi phí thành lập, khả năng tiếp cận thông tin và mức độ chắc chắn của môi trường kinh doanh.

### Chi phí giao dịch
Chi phí thời gian và chi phí không chính thức có thể thể hiện trước hết ở hiệu quả vận hành, doanh thu trên lao động, doanh thu trên doanh nghiệp và khả năng sinh lời.

### Năng lực
Hỗ trợ doanh nghiệp và chính sách lao động có thể liên hệ với kỹ năng, giá trị lao động và cường độ vốn.

## 4. Phân rã kế toán bắt buộc

[
\Delta \log(R)=\Delta \log(F)+\Delta \log(R/F)
]

[
\Delta \log(R/F)=\Delta \log(L/F)+\Delta \log(R/L)
]

Phân rã này được dùng để xác định doanh thu tổng hợp thay đổi chủ yếu qua số doanh nghiệp, quy mô lao động trên doanh nghiệp hay doanh thu trên lao động. Đây là phân rã mô tả, không phải trung gian nhân quả.

## 5. Dữ liệu

Nguồn dự kiến:
- PCI;
- PAPI;
- NSO PX-Web về doanh nghiệp đăng ký mới, doanh nghiệp đang hoạt động, lao động, vốn, doanh thu, lợi nhuận, tỷ suất lợi nhuận, thu nhập lao động và tài sản cố định;
- dân số cấp tỉnh.

Bảng chính mục tiêu: 2015–2023. Cửa sổ gia nhập được xác định riêng theo độ phủ nguồn.

## 6. Ước lượng chính

[
y_{it}=\alpha_i+\lambda_t+\beta G_{i,t-1}+\varepsilon_{it}
]

trong đó:
- (alpha_i): hiệu ứng cố định tỉnh;
- (lambda_t): hiệu ứng cố định năm;
- (G_{i,t-1}): chỉ số quản trị trễ một năm.

Báo cáo sai số chuẩn gom cụm theo tỉnh và hiệu chỉnh Benjamini–Hochberg trong từng họ giả thuyết.

## 7. Bộ kiểm định độ bền và phản chứng

- điểm số thô so với chuẩn hóa theo năm;
- đồng thời so với trễ;
- độ trễ một và hai năm;
- loại 2020–2022;
- phân rã trong tỉnh và giữa tỉnh;
- giá trị quản trị tương lai làm giả dược;
- loại lần lượt tỉnh/năm;
- hoán vị quỹ đạo tỉnh;
- chẩn đoán phụ thuộc chéo và không gian.

Không tự động dùng mô hình không gian hoặc mô hình bảng động nếu chẩn đoán không yêu cầu.

## 8. Những gì bị loại khỏi hướng mới

- xếp hạng “thành phần PCI quan trọng nhất”;
- dùng Rừng ngẫu nhiên (Random Forest — Rừng ngẫu nhiên) hoặc XGBoost làm nguồn đóng góp;
- dùng tầm quan trọng đặc trưng để suy ra tác động;
- mở rộng lưới PCI × kết quả rồi chọn ô có ý nghĩa;
- tạo câu chuyện ngưỡng hoặc COVID sau khi nhìn kết quả;
- gọi mối liên hệ là nhân quả khi chưa có thiết kế nhận dạng.

## 9. Tiêu chuẩn kết luận

Một kết quả yếu hoặc bằng không vẫn là kết quả khoa học hợp lệ.

Nếu cơ chế cũ không tái hiện sau năm 2015, đóng góp của bài sẽ là bằng chứng về giới hạn tính bền vững theo thời gian và giới hạn của việc dùng chỉ số quản trị tổng hợp để suy ra kết quả doanh nghiệp.
