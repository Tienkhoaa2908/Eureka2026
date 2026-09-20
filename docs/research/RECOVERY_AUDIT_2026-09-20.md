# Kiểm toán phục hồi SR1 — 20/09/2026 UTC

Trạng thái: **đang thu thập và thẩm định; chưa khóa dữ liệu, chưa chạy kết quả nghiên cứu cuối.**

## Biên nhận và dữ liệu

- Main lúc phục hồi: `b456ec67c953caa83a9ce15a4a89204f65b86d3f`.
- Nhánh PR13 được phục hồi cùng main trong commit `126267c4f418cb4c33364a316b9450177f8e429c`; [PR16](https://github.com/Tienkhoaa2908/Eureka2026/pull/16) còn là bản nháp.
- ZIP người dùng: panel 945 dòng = 63 tỉnh × 2010–2024; chỉ PCI tổng hợp, không có mười thành phần hay các biên doanh nghiệp cần cho SR1. Kiểm toán chi tiết: `artifacts/qa/handoff/handoff_inventory.json`.
- [Run 35465367100](https://github.com/Tienkhoaa2908/Eureka2026/actions/runs/35465367100) tải được 11 bảng NSO; artifact `10590813129`, SHA-256 ZIP `48c2945c695e28e61082c42265894c30321efccec5f1c66a92a936f22f66d87f`. Đã tải và kiểm tra lại hash CSV nguồn và chuẩn hóa: 11/11 khớp.
- E05.08, .11, .17, .23, .35, .38, .41, .44: mỗi bảng 567 quan sát, 63 tỉnh × 2015–2023, không thiếu giá trị. E05.02: 567 quan sát 2016–2024. E05.04 và .05: mỗi bảng 504 quan sát 2017–2024. Đây là kiểm tra độ phủ, không tự xác nhận định nghĩa hay đơn vị.
- E05.38 và E05.41 đều có 79 giá trị âm: không log trực tiếp lợi nhuận, không xóa quan sát vì âm.
- Đối chiếu `100 × E05.38 / E05.23` với E05.41: chỉ 465/567 ô lệch không quá 0,01 điểm phần trăm; chênh lớn nhất khoảng 0,416 điểm ở Lai Châu 2016. **Chưa được gọi hai biến là đồng nhất.** Cần đọc mẫu số/định nghĩa và các lần sửa số liệu trước khi khóa biến lợi nhuận.

## Lỗi đã sửa và lỗi đang mở

Đã sửa đường dẫn đầu vào panel gia nhập; từ chối khóa PCI trùng; từ chối tự chọn chiều phụ chưa rõ; dùng cùng mẫu đầy đủ khi kiểm tra tính cộng hệ số phân rã; chặn chạy mô hình nếu thiếu khóa dữ liệu/đặc tả có hash; giữ artifact khi CI lỗi.

Commit `ce4f4fdcc8f28ee6ec7a08886bfd4b2f619a6aa9` bổ sung ánh xạ nhãn NSO `Hue` vào Thừa Thiên Huế **chỉ khi toàn bộ năm yêu cầu ≤ 2024** và lưu nhãn gốc. Cơ sở địa giới: [Nghị quyết 175/2024/QH15](https://congbao.chinhphu.vn/van-ban/nghi-quyet-so-175-2024-qh15-43363/53105.htm), thành phố mới trên toàn bộ tỉnh cũ, hiệu lực 01/01/2025. Không dùng quy tắc này cho địa giới sau sáp nhập 2025.

32 kiểm thử toàn repo qua ở máy làm việc. `research-ci` run 35482730390 thành công. Online run 35482730406 vẫn lỗi: nhãn Huế đã qua, nhưng CSV dân số E02.03-07 chưa được parser nhận diện tiêu đề năm. Đây **không phải** bằng chứng thiếu dân số hay thiếu năm. Cần giữ phản hồi gốc để kiểm tra bố cục, đồng thời tải các nguồn độc lập còn lại. Chưa có kết quả ước lượng mới.

## Các điều kiện khoa học bổ sung trước khóa

1. **PCI đổi phép đo:** đọc toàn văn Kokko, Nguyen và Nilsson Hakkala (2026), [ADB WP856](https://www.adb.org/publications/business-climate-economic-complexity-performance-provincial-viet-nam), DOI 10.22617/WPS260325-2, mục 3.3, trang in 18–19. Tác giả dùng 41 chỉ báo nhất quán để dựng thành phần theo thời gian. Bài dùng dữ liệu 2006–2020 và xét cả doanh thu, việc làm, doanh thu/lao động, quy mô doanh nghiệp. Trùng lặp đáng kể với dự án; không được nhận là phát hiện đầu tiên hay mặc nhiên coi hậu 2015 chưa được nghiên cứu.
2. Chuẩn hóa điểm thành phần theo năm chỉ đổi thang đo; không sửa thay đổi câu hỏi khảo sát. Phải kiểm tra chỉ báo gốc giữ nguyên, hoặc thu hẹp cửa sổ có phương pháp ổn định. **Chưa chọn cửa sổ cuối.**
3. Đối chiếu nghiên cứu doanh nghiệp chế biến chế tạo tư nhân với toàn bộ doanh nghiệp cấp tỉnh không tách được thay đổi theo thời gian khỏi thay đổi quần thể. H4 hiện chỉ là mục tiêu đối chiếu, chưa đủ điều kiện kiểm định tái hiện trực tiếp.
4. Đồng nhất thức log đúng về số học không chứng minh cơ chế nhân quả. Dữ liệu tỉnh tổng hợp không theo dõi doanh nghiệp sống sót, gia nhập, rút lui hay tái phân bổ giữa doanh nghiệp.
5. SCOLI là giá sinh hoạt tương đối theo không gian; không tự là chỉ số giảm phát sản lượng ngành. Doanh thu/lao động danh nghĩa không được đổi tên thành năng suất thực.
6. Biến quản trị tương lai có tự tương quan: hệ số lead khác không chưa đủ bác bỏ hay xác nhận nhân quả. Hoán vị quỹ đạo cần giả định trao đổi được; phụ thuộc không gian có thể làm giả định sai.
7. Chưa xác minh được bộ PAPI đủ năm và phép đo tương thích; không mở H5 chỉ để tăng số phép thử.

## Quyết định thiết kế tạm thời, trước kết quả

| Ứng viên | Giá trị tiềm năng | Điều kiện còn thiếu | Quyết định |
|---|---|---|---|
| Phân rã kế toán trên cùng mẫu, PCI đo nhất quán | Kiểm tra kết luận quản trị gắn với biên nào; bảng đối chiếu tái lập | Chỉ báo PCI nhất quán, mẫu số và quần thể | Giữ làm ứng viên chính, chưa khóa |
| Tái hiện trực tiếp nghiên cứu trước/sau 2015 | Kiểm tra tính ổn định thực nghiệm | Cùng quần thể, biến, đặc tả, dữ liệu trước 2015 | Chưa khả thi với panel hiện có |
| Cú sốc chính sách triển khai khác thời điểm | Có thể tăng sức mạnh nhận dạng | Lịch triển khai, nhóm đối chứng, giả định xu hướng và ngoại sinh | Chưa có bằng chứng đủ; không tự dựng DiD |
| PCI–PAPI và lan tỏa không gian | Kiểm tra độ hội tụ và phụ thuộc | Mapping khái niệm, dữ liệu và ma trận không gian khóa trước | Phân tích thứ cấp có điều kiện |

Không chọn mô hình theo p-value. Không merge như một nghiên cứu hoàn tất, viết kết luận hay dọn bỏ lịch sử trước khi chốt thiết kế và qua cổng.
