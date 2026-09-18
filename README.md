# Eureka 2026 — PCI, thể chế địa phương và kết quả doanh nghiệp Việt Nam

Kho lưu trữ nghiên cứu cho đề tài dự thi **Giải thưởng Sinh viên Nghiên cứu khoa học Euréka 2026**.

## Research question

> Những chiều cạnh nào của chất lượng điều hành kinh tế cấp tỉnh (10 chỉ số thành phần PCI) có quan hệ dự báo ổn định với kết quả doanh nghiệp ở cấp tỉnh, sau khi kiểm soát khác biệt cố hữu giữa tỉnh và cú sốc chung theo năm; và machine learning có cải thiện dự báo ngoài mẫu so với các baseline kinh tế lượng hay không?

Cho tới khi có chiến lược nhận dạng nhân quả đủ mạnh, dự án dùng ngôn ngữ **association / relationship / predictive signal**, không suy diễn feature importance thành “tác động nhân quả”.

## Current data

- 63 tỉnh/thành × 15 năm (2010–2024) = 945 province-year observations.
- PCI tổng hợp + doanh thu thuần SXKD doanh nghiệp theo tỉnh.
- 10 chỉ số thành phần PCI; chỉ số 6 bắt đầu từ 2013, vì vậy mẫu đủ 10 chỉ số là 2013–2024 và mẫu lag 1 năm là 2014–2024.
- Nguồn chính: PCI/VCCI và GSO/NSO.

## Start here

1. `PROJECT_STATE.md` — trạng thái chuẩn hiện tại.
2. `docs/research/NEXT_EXPERIMENT.md` — đúng một bước nghiên cứu ưu tiên tiếp theo.
3. `docs/research/QUALITY_GATES.md` — các gate bắt buộc trước khi chấp nhận kết quả.
4. `docs/research/AUDIT_2026-09-18.md` — lỗi và rủi ro đã phát hiện.
5. `docs/research/METHODOLOGY_V1.md` — thiết kế phương pháp đề xuất.
6. `docs/research/LITERATURE_REVIEW.md` — bản đồ tài liệu gần nhất.
7. `docs/competition/EUREKA_2026.md` — deadline/rubric/format và định hướng từ các năm gần đây.
8. `docs/handover/RECOVERY_PROMPT.md` — prompt phục hồi trạng thái ở chat mới.
9. `docs/handover/SYNC_PROMPT.md` — prompt đồng bộ phiên làm việc lên GitHub.

## Operating rules

- Không báo cáo metric nếu không tái tạo được từ code + dữ liệu xác định.
- Không sửa dữ liệu thô tại chỗ.
- Không random-split province-year cho bài toán dự báo tương lai.
- Không impute CSTP6 cho 2010–2012 như missing-at-random.
- Inference và prediction là hai track riêng.
- `PROJECT_STATE.md` là single source of truth; tránh nhân bản file “current status”.

## Current gate

**G1 — Data integrity: OPEN.**

Việc ưu tiên hiện tại là xác minh độc lập ba chênh lệch subtotal doanh thu GSO/NSO đã được phát hiện và xây data-lineage machine-readable. Không tune XGBoost trước khi G1/G2 qua.

## Local validation

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
```

CI chạy cùng hai bước trên cho mọi push/PR.
