# Eureka 2026 — PCI, thể chế địa phương và kết quả doanh nghiệp Việt Nam

Kho lưu trữ nghiên cứu cho đề tài dự thi **Giải thưởng Sinh viên Nghiên cứu khoa học Euréka 2026**.

## Research question

> Những chiều cạnh nào của chất lượng điều hành kinh tế cấp tỉnh (10 chỉ số thành phần PCI) có quan hệ dự báo ổn định với kết quả doanh nghiệp ở cấp tỉnh, sau khi kiểm soát khác biệt cố hữu giữa tỉnh và cú sốc chung theo năm; và machine learning có cải thiện dự báo ngoài mẫu so với các baseline kinh tế lượng hay không?

Cho tới khi có chiến lược nhận dạng nhân quả đủ mạnh, dự án dùng ngôn ngữ **association / relationship / predictive signal**, không suy diễn feature importance thành “tác động nhân quả”.

## Current data

- 63 tỉnh/thành × 15 năm (2010–2024) = 945 province-year observations.
- PCI tổng hợp + doanh thu thuần SXKD doanh nghiệp theo tỉnh.
- 10 chỉ số thành phần PCI; CSTP6 bắt đầu từ 2013.
- Mẫu đủ 10 CSTP contemporaneous: 756 rows (2013–2024).
- Mẫu đủ 10 CSTP lag 1 năm: 693 rows (2014–2024).
- Nguồn chính: PCI/VCCI và GSO/NSO.

## Canonical build

Hai binary migration inputs không commit vào public repo. Đặt chúng tại:

```text
data/raw/migration/panel_PCI_doanhthu_2010_2024.xlsx
data/raw/migration/Panel_10_CSTP_2010_2024.xlsx
```

Sau đó chạy:

```bash
python -m src.eureka2026.pipeline
```

Pipeline sẽ tạo local `data/processed/panel.csv`, tự áp dụng ba correction đã xác minh, tính lại revenue growth/PCI lag/CSTP lag, kiểm 63 × 15 keys, structural missingness và one-to-one merge.

Canonical output fingerprint hiện tại:

`a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd`

Xem `data/metadata/canonical_build_manifest.json` và `artifacts/qa/REPRO-PIPELINE-01.md`.

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
- `PROJECT_STATE.md` là single source of truth.

## Current gate

**G3 — Statistical baseline: CURRENT.**

G1 data integrity và G2 reproducible pipeline đã pass. Bước kế tiếp là two-way fixed-effects baseline trên mẫu lagged 2014–2024, với province FE + year FE + province-clustered standard errors.

Chưa tune XGBoost trước khi G3 hoàn tất.

## Local validation

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
```

CI chạy cùng hai bước trên cho mọi push/PR.
