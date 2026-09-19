# Giao thức nghiên cứu SR1

## Câu hỏi

**Những cơ chế thể chế cấp tỉnh đã được ghi nhận trong các nghiên cứu trước có còn tái hiện trong giai đoạn sau năm 2015 tại Việt Nam hay không; và nếu có, chúng biểu hiện qua biên gia nhập doanh nghiệp, quy mô doanh nghiệp, doanh thu trên lao động, khả năng sinh lời, giá trị lao động và cường độ vốn nào?**

## Đơn vị phân tích

Một quan sát là một tỉnh-năm. Bảng chính dự kiến có 63 tỉnh và các năm 2015–2023, nhưng từng họ giả thuyết dùng đúng cửa sổ mà nguồn chính thức hỗ trợ.

## Ước lượng cơ sở

[
y_{it}=\alpha_i+\lambda_t+\beta G_{i,t-1}+\varepsilon_{it}
]

- (alpha_i): hiệu ứng cố định tỉnh;
- (lambda_t): hiệu ứng cố định năm;
- (G_{i,t-1}): chỉ số quản trị trễ một năm;
- sai số chuẩn gom cụm theo tỉnh.

Đặc tả chính dùng điểm quản trị chuẩn hóa trong từng năm. Điểm thô là kiểm tra độ bền.

## Tại sao không gọi đây là nhân quả

Hiệu ứng cố định loại được dị biệt tỉnh bất biến theo thời gian và cú sốc quốc gia chung theo năm, nhưng không loại được mọi nhiễu thay đổi theo thời gian, phản hồi ngược và sai số đo lường. Vì vậy hệ số chính được diễn giải là quan hệ trong tỉnh có thứ tự thời gian, không phải tác động nhân quả.

## Phân rã trong/giữa tỉnh

Với chỉ số quản trị (G_{it}):

[
G_{it}=\bar G_i + (G_{it}-\bar G_i)
]

Phần thứ hai đo việc một tỉnh tốt/xấu hơn mức bình thường của chính nó. Phần thứ nhất phản ánh khác biệt cấu trúc dài hạn giữa các tỉnh.

## Phân rã kế toán

[
\Delta\log Revenue
=
\Delta\log Firms
+
\Delta\log RevenuePerFirm
]

[
\Delta\log RevenuePerFirm
=
\Delta\log WorkersPerFirm
+
\Delta\log RevenuePerWorker
]

Khi dùng cùng mẫu và cùng ma trận thiết kế, tính tuyến tính của bình phương tối thiểu thông thường yêu cầu các hệ số tương ứng cộng lại trong sai số máy tính. Đây là kiểm tra nội bộ mạnh chống diễn giải sai cơ chế.

## Đa kiểm định

Benjamini–Hochberg được áp dụng trong từng họ H1–H3. Không gom hàng chục mô hình hậu nghiệm rồi chọn hệ số đẹp.

## Kiểm định phản chứng

Bắt buộc:
- giá trị quản trị tương lai;
- loại lần lượt tỉnh;
- loại lần lượt năm;
- hoán vị nguyên quỹ đạo tỉnh;
- loại 2020–2022;
- độ trễ một và hai năm;
- điểm thô so với chuẩn hóa;
- đặc tả trong/giữa tỉnh.

Nếu kết quả chỉ tồn tại trong một đặc tả hoặc bị biến quản trị tương lai “dự báo ngược”, không được gọi là cơ chế bền vững.

## Phụ thuộc không gian

Trước hết kiểm tra phụ thuộc chéo/phần dư. Chỉ nếu có bằng chứng và lý thuyết hợp lý mới mở mô hình không gian. Ma trận láng giềng phải dùng địa giới 63 tỉnh trước năm 2025 và có phân tích độ nhạy với định nghĩa láng giềng.

## Biến kiểm soát

Không thêm biến vì “thường thấy trong bài kinh tế”. Mỗi biến phải được phân loại:
- nhiễu tiền xử lý hợp lý;
- biến trung gian có thể nằm trên cơ chế;
- biến kết quả vĩ mô gần với chính outcome;
- biến hậu nghiệm.

Dân số dùng chủ yếu làm mẫu số. Lao động qua đào tạo là biến bối cảnh/khác biệt năng lực, không tự động kiểm soát H3. GRDP và các outcome vĩ mô chỉ là độ nhạy sau khi lập đồ thị nhân quả khái niệm.

## Tiêu chí kết luận

Một kết quả chính cần đồng thời:
- qua hiệu chỉnh đa kiểm định đã định trước;
- đúng hướng lý thuyết;
- không do một tỉnh/năm;
- không thất bại rõ ở giả dược tương lai;
- không mâu thuẫn với hoán vị;
- có mô tả đầy đủ những đặc tả không ủng hộ;
- có ý nghĩa kinh tế chứ không chỉ ý nghĩa thống kê.

Kết quả bằng không hoặc không tái hiện là kết quả hợp lệ.
