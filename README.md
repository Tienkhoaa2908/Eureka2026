# Eureka 2026 — PCI, thể chế địa phương và kết quả doanh nghiệp Việt Nam

Kho lưu trữ nghiên cứu cho đề tài dự thi **Giải thưởng Sinh viên Nghiên cứu khoa học Euréka 2026**.

## Câu hỏi nghiên cứu hiện tại

> Những chiều cạnh nào của chất lượng điều hành kinh tế cấp tỉnh (10 chỉ số thành phần PCI) có quan hệ dự báo ổn định với kết quả doanh nghiệp ở cấp tỉnh, sau khi kiểm soát khác biệt cố hữu giữa tỉnh và cú sốc chung theo năm; và các mô hình machine learning có cải thiện năng lực dự báo ngoài mẫu so với mô hình kinh tế lượng bảng hay không?

**Lưu ý khoa học:** cho tới khi có chiến lược nhận dạng nhân quả đủ mạnh, dự án dùng ngôn ngữ **liên hệ / dự báo / association**, không kết luận PCI “gây ra” thay đổi doanh thu.

## Phạm vi dữ liệu hiện có

- 63 tỉnh/thành × 15 năm (2010–2024): 945 quan sát tỉnh-năm.
- PCI tổng hợp và doanh thu thuần SXKD doanh nghiệp theo tỉnh.
- 10 chỉ số thành phần PCI; chỉ số “Cạnh tranh bình đẳng” bắt đầu từ 2013, vì vậy mô hình dùng đủ 10 chỉ số có mẫu chính 2013–2024.
- Nguồn chính: PCI/VCCI và số liệu doanh nghiệp công bố bởi GSO/NSO.

## Nguyên tắc vận hành

1. `PROJECT_STATE.md` là nguồn sự thật duy nhất về trạng thái hiện tại.
2. `DECISIONS.md` ghi quyết định phương pháp và lý do.
3. `EXPERIMENTS.md` ghi mọi thử nghiệm, kể cả kết quả âm.
4. `PROGRESS.md` ghi tiến độ theo thời gian.
5. `docs/handover/RECOVERY_PROMPT.md` dùng để phục hồi trạng thái ở cuộc trò chuyện mới.
6. `docs/handover/SYNC_PROMPT.md` dùng để đồng bộ công việc mới nhất lên GitHub và loại bỏ tài liệu lỗi thời.
7. Không đưa số liệu/metric vào báo cáo nếu chưa có artifact hoặc script tái tạo được.
8. Không sửa dữ liệu thô để “làm đẹp” kết quả; mọi hiệu chỉnh phải có lineage và kiểm tra đối chiếu.

## Trạng thái

Repo đang được bootstrap. Xem `PROJECT_STATE.md` sau khi PR bootstrap được hợp nhất.
