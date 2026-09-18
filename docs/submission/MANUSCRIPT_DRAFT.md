# MANUSCRIPT DRAFT — Euréka 2026

Status: research-content draft, not final formatted submission  
Updated: 2026-09-18  
Anonymity: do not add author, institution, supervisor, logo, acknowledgements or identifying metadata to the research content.

# Chất lượng điều hành kinh tế cấp tỉnh và kết quả doanh nghiệp tại Việt Nam: Bằng chứng từ dữ liệu bảng và dự báo ngoài mẫu giai đoạn 2010–2024

## Tóm tắt

Nghiên cứu xem xét mối liên hệ giữa chất lượng điều hành kinh tế cấp tỉnh, đo bằng mười chỉ số thành phần của Chỉ số Năng lực cạnh tranh cấp tỉnh (PCI), và kết quả doanh nghiệp tại 63 tỉnh/thành Việt Nam trong giai đoạn 2010–2024. Khác với cách tiếp cận chỉ ước lượng hệ số hoặc xếp hạng tầm quan trọng từ mô hình machine learning, nghiên cứu tách ba lớp bằng chứng: (i) liên hệ có điều kiện trong dữ liệu bảng, (ii) giá trị dự báo ngoài mẫu theo thời gian, và (iii) độ bền/falsification của kết quả. Dữ liệu doanh thu doanh nghiệp cấp tỉnh được kiểm toán nguồn, sửa ba lỗi nhập liệu có bằng chứng và xây dựng lại thành panel chuẩn 945 tỉnh-năm. Mô hình suy luận chính sử dụng mười chỉ số PCI trễ một năm, hiệu ứng cố định tỉnh và năm, sai số chuẩn cụm theo tỉnh và điều chỉnh Benjamini–Hochberg cho đa kiểm định. Không chỉ số nào đạt ngưỡng q<0,05 đối với mức log doanh thu. Đối với thay đổi log doanh thu, chỉ số “Chi phí không chính thức” (CSTP5) là biến duy nhất đạt ngưỡng sau điều chỉnh trong đặc tả chính (beta chuẩn hóa = 0,0363; q = 0,00129). Tuy nhiên, tín hiệu này yếu đi khi loại nghiêm ngặt giai đoạn đại dịch và biến mất trong một số đặc tả thay thế. Trong sáu cửa sổ dự báo mở rộng 2019–2024, Elastic Net không sử dụng PCI đạt MAE trung bình thấp nhất; bổ sung PCI không cải thiện ổn định dự báo so với baseline mạnh này. Kết quả cho thấy một liên hệ thống kê trong mô hình bảng không nhất thiết chuyển hóa thành giá trị dự báo tương lai, qua đó nhấn mạnh nhu cầu phân biệt suy luận, dự báo và diễn giải tầm quan trọng biến trong nghiên cứu thể chế địa phương.

**Từ khóa:** PCI; thể chế địa phương; doanh thu doanh nghiệp; dữ liệu bảng; Elastic Net; Random Forest; XGBoost; dự báo ngoài mẫu.

## 1. Đặt vấn đề

Chất lượng thể chế và môi trường kinh doanh địa phương có thể ảnh hưởng tới chi phí giao dịch, khả năng tiếp cận nguồn lực, mức độ bất định, quyết định gia nhập thị trường và hiệu quả hoạt động của doanh nghiệp. Ở Việt Nam, PCI là hệ thống đo lường cấp tỉnh có độ bao phủ rộng, kết hợp khảo sát doanh nghiệp và các nguồn dữ liệu công bố để hình thành mười chỉ số thành phần phản ánh những chiều cạnh khác nhau của điều hành kinh tế địa phương.

Tuy nhiên, hai vấn đề thực nghiệm thường bị trộn lẫn. Thứ nhất là câu hỏi **suy luận**: sau khi kiểm soát khác biệt cố hữu giữa các tỉnh và các cú sốc chung theo năm, thay đổi trong một chiều cạnh PCI có liên hệ với thay đổi kết quả doanh nghiệp hay không? Thứ hai là câu hỏi **dự báo**: các thông tin PCI có giúp dự báo tốt hơn kết quả doanh nghiệp của những năm tương lai, so với các baseline chỉ sử dụng lịch sử doanh thu và đặc trưng tỉnh hay không?

Sự phân biệt này quan trọng vì một biến có thể có hệ số khác 0 trong mô hình kinh tế lượng nhưng vẫn không cải thiện dự báo ngoài mẫu. Ngược lại, một mô hình machine learning có thể dự báo tốt nhưng feature importance không phải là ước lượng tác động nhân quả. Nếu không tách hai nhiệm vụ, nghiên cứu dễ suy diễn một thứ hạng dự báo thành kết luận chính sách về “tác động mạnh nhất”.

Nghiên cứu này giải quyết vấn đề trên bằng một thiết kế ba lớp: panel fixed effects có điều chỉnh đa kiểm định, benchmark dự báo mở rộng theo thời gian với nested tuning, và robustness/falsification. Mục tiêu không phải tìm một “chỉ số chiến thắng” bằng mọi giá, mà kiểm tra xem tín hiệu thể chế nào thực sự ổn định, ở loại bằng chứng nào, và giới hạn của nó ở đâu.

## 2. Câu hỏi nghiên cứu và đóng góp

### 2.1. Câu hỏi nghiên cứu

**RQ1.** Những chỉ số thành phần PCI trễ một năm nào có liên hệ có điều kiện với kết quả doanh nghiệp cấp tỉnh sau khi kiểm soát hiệu ứng cố định tỉnh và năm?

**RQ2.** Các chỉ số PCI trễ có tạo ra giá trị dự báo ngoài mẫu cho các năm tương lai ngoài những gì đã có trong lịch sử doanh thu, đặc trưng tỉnh và xu hướng thời gian hay không?

**RQ3.** Những kết quả nổi bật có bền với thay đổi giai đoạn, xử lý outlier, cấu trúc độ trễ, loại tỉnh/năm/vùng và placebo theo thời gian hay không?

### 2.2. Đóng góp

Nghiên cứu có bốn đóng góp chính.

Thứ nhất, xây dựng một pipeline dữ liệu có kiểm toán, truy vết nguồn và kiểm tra bất biến, thay vì chỉ làm việc với một workbook thủ công. Ba lỗi doanh thu tỉnh-năm được xác minh từ nguồn đã được sửa bằng code và toàn bộ biến tăng trưởng/độ trễ được tái sinh.

Thứ hai, tách rõ inference và prediction. Mô hình fixed effects được dùng để mô tả liên hệ trong panel; benchmark machine learning được dùng để đánh giá khả năng generalize sang năm tương lai.

Thứ ba, benchmark dự báo sử dụng expanding-window temporal validation và nested temporal tuning, tránh random split có thể làm rò rỉ cấu trúc thời gian.

Thứ tư, nghiên cứu giữ nguyên kết quả âm. Không có feature-importance ranking nào được tạo khi PCI không chứng minh được incremental predictive value vượt baseline mạnh nhất.

## 3. Tổng quan nghiên cứu

PCI/VCCI xây dựng PCI từ dữ liệu khảo sát doanh nghiệp và nguồn dữ liệu công bố, chuẩn hóa thành mười chỉ số thành phần. Một địa phương được xem là có chất lượng tốt ở CSTP5 khi gánh nặng chi phí không chính thức thấp hơn. Nguồn phương pháp: https://pcivietnam.vn/en/about/pci-methodology.html và https://pcivietnam.vn/en/faqs.html.

Nguyen, Le và Bryant (2013) cho thấy thể chế cấp địa phương có vai trò trong mối quan hệ giữa chiến lược và hiệu quả doanh nghiệp, sử dụng thiết kế đa cấp trên doanh nghiệp sản xuất tư nhân tại Việt Nam (DOI 10.1016/j.jwb.2012.06.008). Điều này cho thấy khác biệt thể chế dưới cấp quốc gia là thực chất và cần được mô hình hóa riêng.

Huynh (2022) sử dụng Spatial Durbin Model trên dữ liệu doanh nghiệp giai đoạn 2011–2018 và báo cáo cả hiệu ứng trực tiếp lẫn lan tỏa không gian của chất lượng thể chế; kiểm soát tham nhũng liên hệ thuận với lợi nhuận, trong khi chi phí không chính thức liên hệ nghịch với TFP (DOI 10.1111/apel.12362). Kết quả này đặt ra khả năng phụ thuộc không gian giữa các tỉnh.

Nghiên cứu “Total factor productivity and institutional quality in Vietnam: which institutions matter most?” năm 2024 cho thấy không phải mọi chiều cạnh PCI đều quan trọng như nhau đối với TFP; các chiều như chi phí thời gian và chính sách lao động nổi bật trong các đặc tả được báo cáo (DOI 10.1007/s41685-024-00343-9). Điều này cho thấy thứ hạng thành phần phụ thuộc outcome và thiết kế.

Kokko, Nguyen và Nilsson Hakkala (ADB, 2026) phân tích 63 tỉnh bằng difference-GMM và báo cáo rằng thay đổi PCI có ảnh hưởng hạn chế lên nhiều chỉ tiêu manufacturing như revenue, employment, productivity và economic complexity trong nhiều đặc tả (DOI 10.22617/WPS260325-2). Bằng chứng này đặc biệt quan trọng vì nó cho phép nghiên cứu hiện tại xem kết quả yếu/null là khả năng khoa học hợp lệ.

Thoa và Hung (2026) nghiên cứu gia nhập thị trường doanh nghiệp 2017–2024 bằng FE và sai số chuẩn cụm. Các thành phần có ý nghĩa khác nhau giữa mô hình contemporaneous và lagged; informal charges có ý nghĩa trong mô hình trễ, còn legal institutions/security ổn định hơn qua các mô hình (DOI 10.26459/hueunijed.v135i5C.8471).

Nhìn chung, literature không hỗ trợ giả thuyết rằng tồn tại một thành phần PCI “quan trọng nhất” cho mọi outcome. Khoảng trống phù hợp hơn là đánh giá đồng thời tính ổn định trong suy luận và khả năng dự báo tương lai trên cùng một panel được kiểm toán.

## 4. Dữ liệu

### 4.1. Đơn vị quan sát và thời gian

Đơn vị quan sát là tỉnh-năm. Panel chuẩn có:

- 63 tỉnh/thành;
- 15 năm, 2010–2024;
- 945 quan sát tỉnh-năm.

Mười chỉ số thành phần PCI có sẵn đầy đủ từ 2013. CSTP6 là structural missing trong 2010–2012, vì vậy:
- mẫu contemporaneous đủ 10 thành phần: 2013–2024, N=756;
- mẫu lag một năm đủ 10 thành phần: 2014–2024, N=693.

### 4.2. Outcome

Outcome chính:
- `log_revenue_change = log(revenue_t) - log(revenue_t-1)`.

Outcome phụ:
- `log_revenue = log(revenue_t)`.

Doanh thu là doanh thu thuần sản xuất kinh doanh của doanh nghiệp theo địa phương, đơn vị tỷ đồng.

### 4.3. Kiểm toán dữ liệu

Ba lỗi nhập liệu đã được xác minh và sửa trong dữ liệu dẫn xuất:
- Hòa Bình 2016: 23.040 → 33.040;
- Gia Lai 2023: 133.195 → 131.195;
- An Giang 2023: 212.941 → 212.961.

Sau sửa, toàn bộ 90 kiểm tra subtotal vùng-năm có residual tuyệt đối không quá 3. Dữ liệu raw/legacy được bảo toàn; correction áp dụng bằng code.

Canonical panel có SHA-256:
`a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd`.

## 5. Phương pháp

### 5.1. Mô hình fixed effects

Đặc tả chính:

`y_it = alpha_i + lambda_t + beta' Z(PCI_i,t-1) + epsilon_it`

trong đó:
- `alpha_i`: hiệu ứng cố định tỉnh;
- `lambda_t`: hiệu ứng cố định năm;
- `Z(PCI_i,t-1)`: mười chỉ số thành phần PCI trễ một năm, chuẩn hóa theo SD mẫu.

Sai số chuẩn được cluster theo tỉnh. Suy luận dùng cluster-t với hiệu chỉnh small-sample/df. Do có mười phép kiểm định thành phần trong mỗi outcome/specification, p-value được điều chỉnh Benjamini–Hochberg FDR.

Mô hình FE mô tả association có điều kiện, không phải causal effect.

### 5.2. Benchmark dự báo

Dự báo sử dụng sáu outer folds cố định:
- test 2019, train 2014–2018;
- test 2020, train 2014–2019;
- …
- test 2024, train 2014–2023.

Information set ở năm t chỉ sử dụng:
- log revenue t-1;
- log-revenue change t-1;
- province identity;
- deterministic time trend;
- với PCI-added model: 10 PCI components t-1.

Các mô hình:
- naive;
- Elastic Net ± PCI;
- Random Forest ± PCI;
- XGBoost ± PCI.

Hyperparameter được tune bằng inner expanding temporal splits chỉ trong outer-training set. Không dùng random split.

Metric chính: MAE. Metric phụ: RMSE.

### 5.3. Robustness/falsification

Các kiểm tra gồm:
- strict COVID exclusion: bỏ 2020–2022;
- contemporaneous 10-component model;
- longer-period 9-component lagged model 2011–2024;
- winsorize outcome 1%;
- single-component CSTP5;
- distributed lag 1–2;
- future-lead placebo;
- leave-one-year-out;
- leave-one-region-out;
- Pesaran CD residual diagnostic.

## 6. Kết quả

### 6.1. Fixed-effects baseline

Đối với `log_revenue`, không thành phần PCI nào có BH q<0,05.

Đối với `log_revenue_change`, CSTP5 là thành phần duy nhất đạt ngưỡng sau BH:
- beta chuẩn hóa = **0,03628**;
- cluster SE = 0,00888;
- p = **0,000129**;
- BH q = **0,001289**;
- 95% CI = **[0,01852; 0,05404]**.

Nếu chuyển beta log-change sang revenue-ratio scale, `exp(beta)-1` xấp xỉ **3,69%** cho một SD cao hơn của CSTP5 năm trước, có điều kiện trên FE và các thành phần PCI khác. Đây chỉ là cách biểu diễn association, không phải causal effect.

### 6.2. Dự báo ngoài mẫu

Với `log_revenue_change`, MAE trung bình:
- Elastic Net không PCI: **0,08819**;
- Elastic Net + PCI: 0,08890;
- RF + PCI: 0,09523;
- XGBoost không PCI: 0,10172;
- XGBoost + PCI: 0,10321;
- RF không PCI: 0,10365;
- naive: 0,11484.

Elastic Net không PCI tốt nhất. PCI giúp RF tương đối so với RF không PCI, nhưng RF+PCI vẫn kém Elastic Net không PCI khoảng 7,98% mean MAE và chỉ thắng baseline mạnh này 1/6 test years.

Với `log_revenue`, Elastic Net không PCI tiếp tục tốt nhất, MAE 0,08859. Thêm PCI làm MAE của Elastic Net, RF và XGBoost đều xấu hơn theo trung bình.

Do không PCI-added model nào vừa vượt mean MAE của Elastic Net không PCI vừa thắng tối thiểu 4/6 outer folds, feature-importance gate không đạt. Nghiên cứu không tạo SHAP/permutation ranking.

### 6.3. Temporal instability

Đối với tăng trưởng:
- 2019: PCI Elastic Net tốt nhất;
- 2020: naive tốt nhất;
- 2021–2022: non-PCI Elastic Net tốt nhất;
- 2023: naive tốt nhất;
- 2024: non-PCI Elastic Net tốt nhất, PCI Elastic Net gần như hòa.

Do đó model performance phụ thuộc regime; một thứ hạng dựa trên mean duy nhất không đủ.

### 6.4. Robustness của CSTP5

Kết quả primary không phải do outlier: winsorized model có beta≈0,03416 và q≈0,00149.

Tín hiệu cũng ổn định khi bỏ từng năm hoặc từng vùng:
- leave-one-year beta: 0,03191–0,04924, không đổi dấu;
- leave-one-region beta: 0,02907–0,03990, không đổi dấu.

Tuy nhiên:
- strict COVID exclusion: beta≈0,03316 nhưng q≈0,06720;
- contemporaneous model: beta gần 0, p≈0,994;
- longer 2011–2024 nine-component model: beta≈0,01170, q≈0,311.

Distributed lag cho thấy lag 1 có ý nghĩa (beta≈0,02514; p≈0,00824), lag 2 null. Future-lead placebo null (p≈0,477).

## 7. Thảo luận

Kết quả cho thấy ba lớp bằng chứng không đồng nhất, và chính sự không đồng nhất đó là thông tin khoa học.

Trong mô hình FE chính, CSTP5 có một lagged association tương đối rõ với thay đổi doanh thu. Nhưng association này không ổn định qua mọi giai đoạn/specification và không tạo incremental forecast value vượt baseline có lịch sử doanh thu.

Điều này có thể xuất phát từ ít nhất bốn cơ chế.

Thứ nhất, effect conditional có thể nhỏ so với shocks vĩ mô/năm và độ biến động của doanh thu.

Thứ hai, lịch sử doanh thu có độ giàu thông tin cao. Khi mô hình dự báo đã quan sát mức và thay đổi doanh thu gần nhất, phần thông tin mới mà PCI cung cấp có thể rất nhỏ.

Thứ ba, PCI components có tương quan và đo những khía cạnh liên quan của môi trường điều hành, làm tín hiệu khó được phân tách ổn định ngoài mẫu.

Thứ tư, relationship có thể thay đổi theo regime. Sự khác biệt rõ giữa các test years và sự suy yếu ở strict-COVID specification cho thấy period dependence đáng kể.

Kết quả này phù hợp với literature Việt Nam có tính mixed hơn là với một narrative đơn giản rằng “PCI tốt hơn luôn làm doanh nghiệp tăng trưởng hơn”.

## 8. Hàm ý chính sách

CSTP5 cao biểu thị gánh nặng chi phí không chính thức thấp hơn. Hướng dấu trong primary FE model phù hợp với lập luận kinh tế rằng giảm informal charges có thể cải thiện môi trường kinh doanh.

Tuy nhiên, nghiên cứu không chứng minh một intervention tăng CSTP5 sẽ gây ra mức tăng doanh thu cố định. Không nên dùng beta 3,69% như causal effect và không nên dùng ML importance để xếp ưu tiên chính sách.

Hàm ý phù hợp hơn là:
- cải thiện minh bạch và giảm gánh nặng informal charges vẫn là mục tiêu thể chế hợp lý;
- nhưng quyết định ưu tiên cần dựa thêm trên cơ chế cụ thể, dữ liệu doanh nghiệp vi mô và thiết kế causal/quasi-experimental;
- forecasting evidence hiện tại cho thấy PCI không cung cấp shortcut đáng tin cậy để dự báo tăng trưởng doanh thu cấp tỉnh khi đã có lịch sử doanh thu.

## 9. Hạn chế

Thứ nhất, outcome là doanh thu tổng hợp danh nghĩa cấp tỉnh, không phải profit/TFP ở firm level.

Thứ hai, FE loại bỏ khác biệt tỉnh bất biến và shocks chung theo năm nhưng không loại bỏ mọi confounder thay đổi theo thời gian, như cơ cấu ngành hay số lượng doanh nghiệp.

Thứ ba, common national deflator trong log-level FE với full year FE bị hấp thụ bởi year dummies, nên không tạo robustness độc lập. Muốn kiểm tra scale thực chất cần province-specific price series hoặc revenue per active firm/worker đã verify.

Thứ tư, T ngắn hạn chế sức mạnh của một số spatial diagnostics.

Thứ năm, phương pháp và cấu trúc PCI có thể thay đổi qua thời gian.

Thứ sáu, nguồn Table 151 cho block 2020–2024 được fingerprint và cross-check nhưng exact publication/page ban đầu không còn trong source bundle.

## 10. Kết luận

Nghiên cứu không tìm thấy bằng chứng cho một thành phần PCI có liên hệ ổn định với mức doanh thu qua đặc tả chính sau điều chỉnh đa kiểm định. Đối với tăng trưởng log doanh thu, CSTP5 có lagged association trong mô hình FE 2014–2024, nhưng mức độ bền bị giới hạn bởi thời kỳ và specification.

Quan trọng hơn, các PCI components không tạo thêm giá trị dự báo ngoài mẫu ổn định vượt một Elastic Net không PCI trên sáu năm test 2019–2024. Vì vậy một signal thống kê trong panel không nên tự động được chuyển thành feature-importance story hoặc causal policy ranking.

Đóng góp của nghiên cứu nằm ở thiết kế kiểm chứng ba lớp — inference, prediction và falsification — cùng một pipeline dữ liệu có audit. Cách tiếp cận này cung cấp một khuôn khổ thận trọng hơn để đánh giá bằng chứng thể chế địa phương và kết quả doanh nghiệp.

## Tài liệu tham khảo cốt lõi

- Breiman, L. (2001). Random Forests. *Machine Learning*, 45, 5–32. DOI: 10.1023/A:1010933404324.
- Chen, T. & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. *KDD 2016*, 785–794. DOI: 10.1145/2939672.2939785.
- Huynh, T.N. (2022). Spatial effects of institutional quality on firm performance: evidence from Vietnam. *Asian-Pacific Economic Literature*, 36(2), 89–105. DOI: 10.1111/apel.12362.
- Kokko, A., Nguyen, T.T. & Nilsson Hakkala, K. (2026). Business Climate, Economic Complexity, and Performance at the Provincial Level in Viet Nam. ADB Economics Working Paper. DOI: 10.22617/WPS260325-2.
- Nguyen, T.V., Le, N.T.B. & Bryant, S.E. (2013). Sub-national institutions, firm strategies, and firm performance: A multilevel study of private manufacturing firms in Vietnam. *Journal of World Business*, 48(1), 68–76. DOI: 10.1016/j.jwb.2012.06.008.
- Tashman, L.J. (2000). Out-of-sample tests of forecasting accuracy: an analysis and review. *International Journal of Forecasting*, 16(4), 437–450. DOI: 10.1016/S0169-2070(00)00065-0.
- Thoa, H.T.K. & Hung, N.M. (2026). The impact of the provincial competitiveness index on firms’ market entry in Vietnam. *Hue University Journal of Science: Economics and Development*, 135(5C). DOI: 10.26459/hueunijed.v135i5C.8471.
- Zou, H. & Hastie, T. (2005). Regularization and variable selection via the elastic net. *JRSS B*, 67(2), 301–320. DOI: 10.1111/j.1467-9868.2005.00503.x.
- PCI/VCCI methodology: https://pcivietnam.vn/en/about/pci-methodology.html
