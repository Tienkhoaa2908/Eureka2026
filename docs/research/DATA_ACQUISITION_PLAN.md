# Kế hoạch dữ liệu SR1 — hướng cơ chế hậu 2015

## 1. Kết luận sau khi rà soát nguồn

Bộ dữ liệu hiện tại trên kho mã **chưa đủ** cho câu hỏi mới. Doanh thu và PCI cũ chỉ cho phép thấy một quan hệ tổng hợp; chúng không cho biết doanh thu thay đổi vì số doanh nghiệp, quy mô doanh nghiệp hay doanh thu trên lao động.

Bảng cơ chế chính phải ghép đồng nhất theo tỉnh-năm từ dữ liệu doanh nghiệp của Cục Thống kê/Tổng cục Thống kê. Hai nguồn bổ sung có giá trị khoa học cao nhất ngoài các bảng doanh nghiệp là:

1. **Dân số trung bình E02.03-07** để tự dựng mật độ doanh nghiệp và kiểm tra chéo bảng mật độ E05.05.
2. **Chỉ số giá sinh hoạt theo không gian E11.23** để kiểm tra liệu các kết quả tiền tệ theo tỉnh chỉ phản ánh khác biệt mức giá hay không.

Tỷ lệ lao động qua đào tạo E02.55 được thu thập nhưng chỉ dùng như biến bối cảnh/khác biệt năng lực đã định trước; không tự động đưa vào mọi hồi quy vì nó có thể nằm trên chính đường cơ chế mà H3 muốn nghiên cứu.

## 2. Khối dữ liệu bắt buộc

Khối doanh nghiệp tạo một hệ kế toán thống nhất:
- số doanh nghiệp đang hoạt động và doanh nghiệp có kết quả sản xuất kinh doanh;
- số doanh nghiệp đăng ký mới;
- lao động;
- vốn;
- doanh thu;
- lợi nhuận;
- thu nhập người lao động;
- tỷ suất lợi nhuận;
- tài sản cố định trên lao động.

Khối quản trị:
- mười chỉ số thành phần PCI;
- PAPI chỉ sau khi kiểm tra tính so sánh theo thời gian.

Khối chuẩn hóa:
- dân số;
- chỉ số giá sinh hoạt theo không gian;
- ranh giới 63 tỉnh trước năm 2025 cho chẩn đoán không gian.

## 3. Vì sao không nhồi thêm mọi dữ liệu có thể tìm thấy

Không phải dữ liệu nào cũng làm nhận dạng tốt hơn.

- GRDP/người và tăng trưởng GRDP chỉ có cửa sổ ngắn trong bảng PX-Web đang xác minh, đồng thời rất gần biến kết quả; dùng làm biến kiểm soát chính có thể tạo kiểm soát hậu nghiệm hoặc làm mất chính cơ chế kinh tế đang cần đo.
- FDI theo tỉnh trong nguồn PX-Web đã xác minh chỉ là số lũy kế hoặc ảnh chụp năm 2024, không phải bảng tỉnh-năm phù hợp.
- Chỉ số chuyển đổi số cấp tỉnh có lịch sử ngắn và sau năm 2025 còn gặp thay đổi địa giới.
- Khảo sát Doanh nghiệp của Ngân hàng Thế giới năm 2023 có 1.028 doanh nghiệp nhưng biến vùng lấy mẫu chỉ có 5 vùng lớn, không đủ để ghép trực tiếp với bảng 63 tỉnh.
- VHLSS/LFS khác đơn vị quan sát và tạo gánh nặng hài hòa lớn mà chưa giải quyết trực tiếp câu hỏi cơ chế.
- PAR Index/SIPAS có thể dùng sau như đối chiếu, nhưng PAPI đã là phép đo quản trị độc lập phù hợp hơn và tránh biến nghiên cứu thành “sưu tập chỉ số”.

## 4. Quy tắc giấy phép và tái phân phối

### PCI
Không đưa các tệp PCI gốc do VCCI phát hành vào kho mã công khai. Chính sách của VCCI yêu cầu trích dẫn và cấm chia sẻ lại/đóng gói lại trái phép trên nền tảng khác. Kho mã chỉ giữ:
- đường dẫn nguồn;
- hàm băm của nguồn đã đọc;
- mã tái tạo;
- dữ liệu phân tích dẫn xuất ở mức cần thiết, kèm trích dẫn và rà soát giấy phép trước khi phát hành công khai.

### PAPI
Dữ liệu tổng hợp cấp chiều/tiểu chiều được PAPI cho phép tải dưới Excel/CSV. Dữ liệu vi mô đầy đủ ở cấp người trả lời cần yêu cầu UNDP và chấp nhận điều khoản riêng. Nghiên cứu này chưa cần dữ liệu vi mô để trả lời câu hỏi chính.

### NSO
Các bảng PX-Web dùng trong SR1 được tải trực tiếp, lưu bản xuất nguồn, bản chuẩn hóa và SHA-256. Trang của các bảng đã kiểm tra hiển thị “Copyright: No”, nhưng mọi bản phát hành vẫn phải trích nguồn rõ ràng.

## 5. PAPI: dùng “Core PAPI”, không ghép chỉ số tổng hợp bừa bãi

PAPI đã thay đổi chỉ báo theo thời gian. Báo cáo 2020 xây dựng **Core PAPI (PAPI lõi)** gồm sáu chiều và các chỉ báo không thay đổi từ 2011 để so sánh xuyên thời gian.

Do đó lớp đối chiếu H5 phải:
1. ưu tiên các chiều PAPI lõi có định nghĩa ổn định;
2. lập bảng thay đổi định nghĩa theo năm;
3. khóa trước cặp khái niệm PAPI–kết quả;
4. không chọn chiều PAPI sau khi nhìn hệ số PCI.

Ứng viên lý thuyết:
- Minh bạch trong ra quyết định ở địa phương;
- Kiểm soát tham nhũng trong khu vực công;
- Thủ tục hành chính công.

## 6. Không gian

Chẩn đoán phụ thuộc không gian cần ranh giới 63 tỉnh lịch sử, không được dùng bản đồ 34 tỉnh sau sáp nhập năm 2025.

Nguồn tạm chọn là bộ GeoJSON “trước 2025” của Nguyễn Duy Liêm vì kho nguồn công khai cho phép sử dụng công cộng và yêu cầu ghi nguồn. Trước khi dùng trong kết quả cuối phải:
- kiểm tra đúng 63 đơn vị;
- đối chiếu tên với hợp đồng tên tỉnh của dự án;
- kiểm tra đa giác đảo/đảo xa bờ không tạo láng giềng giả;
- sinh ma trận láng giềng theo tiếp giáp biên đất liền; chạy thêm ma trận khoảng cách như độ nhạy.

## 7. Cấu trúc dữ liệu trên kho mã

```
data/
  README.md
  metadata/
    SR1_DATA_CATALOG.csv
    DATA_DICTIONARY_SR1.csv
    ...
  raw/
    README.md
  processed/
    README.md
```

Các tệp gốc có giấy phép không cho phép tái phân phối không được đưa vào Git. Quy trình phải tải lại được từ nguồn và xác minh hàm băm.

## 8. Tiêu chuẩn “đủ dữ liệu”

SR1 chỉ được chuyển từ cổng dữ liệu sang cổng mô hình khi:
- mọi biến bắt buộc có bảng nguồn chính thức;
- độ phủ tỉnh/năm đã được đo chứ không suy đoán;
- mọi mẫu số của tỷ lệ có cùng phạm vi doanh nghiệp;
- phân rã kế toán khớp;
- PAPI có bảng so sánh định nghĩa;
- ranh giới không gian khớp 63 tỉnh;
- mọi nguồn có chính sách tái phân phối ghi trong danh mục.
