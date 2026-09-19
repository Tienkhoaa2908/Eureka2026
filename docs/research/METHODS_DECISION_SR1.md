# Quyết định phương pháp SR1

## 1. Ngăn xếp phương pháp chính

### 1.1. Hiệu ứng cố định hai chiều (Two-Way Fixed Effects — Hiệu ứng cố định theo tỉnh và năm)

Mô hình:
[
y_{it}=\alpha_i+\lambda_t+\beta G_{i,t-1}+\varepsilon_{it}
]

Vai trò:
- loại đặc điểm tỉnh không đổi theo thời gian;
- hấp thụ cú sốc quốc gia chung theo năm;
- tập trung vào biến động trong tỉnh.

Không giải quyết:
- nhiễu thay đổi theo thời gian;
- phản hồi ngược;
- sai số đo lường;
- lan tỏa không gian.

### 1.2. Sai số chuẩn gom cụm theo tỉnh

63 tỉnh là đơn vị cụm. Đây là mặc định cho suy luận cơ sở.

### 1.3. Benjamini–Hochberg

Áp dụng riêng trong từng họ giả thuyết H1–H3 để kiểm soát tỷ lệ phát hiện sai.

### 1.4. Phân rã trong/giữa tỉnh

Dùng dạng Mundlak/correlated random effects như một phép chẩn đoán:
[
G_{it} = \bar G_i + (G_{it}-\bar G_i)
]

Mục tiêu là phân biệt structural differences với own-province improvement.

## 2. Độ trễ

Đặc tả chính: (t-1).

Độ nhạy: (t-1) và (t-2) cùng mô hình. Không quét hàng loạt độ trễ để tìm ý nghĩa.

Lag giúp thứ tự thời gian rõ hơn nhưng không tạo nhận dạng nhân quả.

## 3. Phân rã kế toán

Đây là phương pháp trung tâm chứ không phải robustness phụ.

Nếu cùng mẫu và cùng thiết kế:
[
\hat\beta_{Deltaln R}
=
\hat\beta_{Deltaln F}
+
\hat\beta_{Deltaln R/F}
]

và:
[
\hat\beta_{Deltaln R/F}
=
\hat\beta_{Deltaln L/F}
+
\hat\beta_{Deltaln R/L}
]

Mã phải kiểm tra residual additivity ở mức sai số số học.

## 4. Kiểm định phản chứng

- lead (t+1) của governance;
- permutation nguyên quỹ đạo tỉnh;
- leave-one-province;
- leave-one-year;
- loại 2020–2022;
- raw score vs within-year z-score.

Không có một “điểm robustness” tổng hợp. Báo từng thất bại.

## 5. Phụ thuộc chéo và không gian

Trình tự:
1. kiểm tra phụ thuộc chéo của residual;
2. nếu đáng kể, xem xét sai số chuẩn Driscoll–Kraay như độ nhạy;
3. dựng ma trận tiếp giáp và khoảng cách;
4. chỉ khi lý thuyết + chẩn đoán cùng ủng hộ mới mở mô hình SAR/SEM/SDM.

Không dùng spatial model như trang trí.

## 6. Mô hình bảng động và GMM

Arellano–Bond / system GMM **không phải mặc định**.

Lý do:
- N≈63 và T≈9 cho panel cơ chế là không lớn theo hướng thuận lợi nhất của GMM;
- instrument proliferation có thể nghiêm trọng;
- outcome chính không nhất thiết phải có lag của chính nó trong phương trình;
- causal interpretation vẫn cần exogeneity assumptions.

Chỉ mở nếu câu hỏi chuyển sang persistence động và có kế hoạch giới hạn instruments, kiểm tra AR(2), Hansen/Sargan và độ nhạy.

## 7. Driscoll–Kraay, PCSE, CCE

- Driscoll–Kraay: độ nhạy nếu residual có phụ thuộc chéo; T ngắn khiến suy luận phải thận trọng.
- PCSE (panel-corrected standard errors — sai số chuẩn hiệu chỉnh bảng): không thay thế nhận dạng; chỉ xem xét nếu cấu trúc lỗi phù hợp.
- CCE (common correlated effects — hiệu ứng tương quan chung): có thể hữu ích nếu factor chung không được year FE hấp thụ, nhưng với T ngắn phải dùng rất thận trọng.

## 8. Mô hình ngưỡng / phi tuyến

Không mở lại câu chuyện threshold chỉ vì có thể chạy. Cần một lý thuyết về ngưỡng, đủ variation và preregistration.

## 9. Trung gian nhân quả

Không gọi phân rã kế toán là causal mediation (trung gian nhân quả). Chưa có giả định sequential ignorability và chưa nhận dạng được direct/indirect causal effects.

## 10. DiD / event study / synthetic control

Không sử dụng nếu chưa có một reform/shock có:
- thời điểm rõ;
- exposure/treatment rõ;
- nhóm so sánh hợp lý;
- giả định xu hướng song song/thiết kế đối chứng có thể bảo vệ.

SEZ là một hướng literature đáng chú ý nhưng không tự động biến thành instrument cho bài này.

## 11. Học máy

Không thuộc ngăn xếp chính của SR1.

Nếu sau này cần dự báo như phụ lục:
- split theo thời gian;
- nested tuning;
- so baseline mạnh;
- không dùng feature importance để tuyên bố cơ chế.

## 12. Gói phần mềm dự kiến

Python:
- `statsmodels`: OLS, covariance, kiểm định cơ bản;
- `linearmodels`: mô hình bảng và covariance nâng cao nếu cần;
- `scipy`: kiểm định;
- `statsmodels.stats.multitest`: Benjamini–Hochberg;
- `geopandas`, `shapely`, `libpysal`, `spreg`: không gian, chỉ sau khi SR5 mở;
- `matplotlib`: đồ thị;
- `numpy`: phép biến đổi và kiểm tra identity.

R chỉ dùng để đối chiếu nếu cần:
- `fixest`;
- `plm`;
- `sandwich`;
- `spdep` / `splm`.

Không thêm package chỉ vì “hiện đại”.
