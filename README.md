# 030238220101_Nguy-n-Nh-t-Qu-nh-Lan_AI-Agent
# Dashboard Đánh Giá Khả Năng Triển Khai AI Agent Một Cách Có Trách Nhiệm

## Giới thiệu dự án

Sự phát triển nhanh chóng của AI Agent đang mở ra nhiều cơ hội tự động hóa trong doanh nghiệp. Tuy nhiên, việc triển khai AI không chỉ phụ thuộc vào khả năng công nghệ mà còn chịu ảnh hưởng bởi mức độ chấp nhận của người lao động, nhu cầu kiểm soát của con người và các rủi ro liên quan đến nghề nghiệp.

Dự án này xây dựng một dashboard phân tích nhằm xác định những nhiệm vụ phù hợp nhất để triển khai AI Agent, dựa trên cả yếu tố kỹ thuật và yếu tố con người.

Mục tiêu của dự án là hỗ trợ doanh nghiệp đưa ra quyết định triển khai AI Agent một cách hiệu quả và có trách nhiệm.

---

## Bài toán nghiên cứu

Trong thực tế, nhiều tổ chức đánh giá cơ hội ứng dụng AI chủ yếu dựa trên câu hỏi:

"AI có thể thực hiện công việc này hay không?"

Tuy nhiên, một nhiệm vụ dù có thể được AI thực hiện tốt vẫn có thể gặp khó khăn khi triển khai nếu:

* Người lao động không sẵn sàng sử dụng AI.
* Công việc đòi hỏi sự kiểm soát chặt chẽ của con người.
* Tồn tại lo ngại về ảnh hưởng tới nghề nghiệp.

Vì vậy, dự án tập trung trả lời câu hỏi:

**Những nhiệm vụ nào nên được ưu tiên triển khai AI Agent để đạt hiệu quả cao nhất nhưng vẫn đảm bảo tính chấp nhận và kiểm soát rủi ro?**

---

## Dữ liệu sử dụng

Bộ dữ liệu bao gồm:

* 147 nhiệm vụ công việc
* 17 nghề nghiệp thuộc lĩnh vực Công nghệ thông tin

Các nguồn dữ liệu được sử dụng:

* Đánh giá khả năng tự động hóa của AI (Automation Capacity)
* Đánh giá mức độ mong muốn tự động hóa của người lao động (Automation Desire)
* Mức độ cần sự kiểm soát của con người (Human Agency)
* Mức độ lo ngại về an toàn nghề nghiệp (Job Security)
* Mức độ tiêu tốn thời gian của nhiệm vụ (Time Consumption)
* Thống kê lao động theo nghề nghiệp
* Mức lương trung bình theo nghề nghiệp

---

## Phương pháp xây dựng mô hình

### 1. Agent Fit Score

Đây là chỉ số trung tâm của dashboard, được sử dụng để đánh giá mức độ phù hợp của một nhiệm vụ đối với việc triển khai AI Agent.

Công thức:

Agent Fit Score

= 0.35 × Capacity

* 0.25 × Desire

* 0.15 × Time

* 0.15 × (6 − Human Agency)

* 0.10 × (6 − Job Security)

Trong đó:

* Capacity: Khả năng AI thực hiện nhiệm vụ.
* Desire: Mức độ người lao động mong muốn tự động hóa.
* Time: Mức độ tiêu tốn thời gian của nhiệm vụ.
* Human Agency: Mức độ cần sự kiểm soát của con người.
* Job Security: Mức độ lo ngại về ảnh hưởng nghề nghiệp.

Điểm càng cao cho thấy nhiệm vụ càng phù hợp để triển khai AI Agent.

---

### 2. Trust Gap

Chỉ số Trust Gap được xây dựng nhằm đo lường khoảng cách giữa khả năng công nghệ và mức độ sẵn sàng chấp nhận của người lao động.

Công thức:

Trust Gap = Capacity − Desire

Ý nghĩa:

* Trust Gap > 0: AI có khả năng thực hiện nhưng người lao động chưa thực sự sẵn sàng.
* Trust Gap < 0: Người lao động mong muốn tự động hóa nhiều hơn khả năng hiện tại của AI.
* Trust Gap ≈ 0: Công nghệ và mức độ chấp nhận đang cân bằng.

---

### 3. Impact Score

Impact Score được sử dụng để xác định những nhiệm vụ mang lại giá trị triển khai lớn nhất.

Công thức:

Impact Score = Agent Fit Score × Employment × Wage

Trong đó:

* Agent Fit Score phản ánh mức độ phù hợp.
* Employment phản ánh số lượng lao động chịu tác động.
* Wage phản ánh giá trị kinh tế của nghề nghiệp.

Những nhiệm vụ có Impact Score cao sẽ được ưu tiên trong quá trình triển khai AI Agent.

---

## Cấu trúc Dashboard

### 1. Foundation

Phân tích tổng quan về khả năng triển khai AI Agent.

Bao gồm:

* Phân phối Agent Fit Score
* So sánh Desire và Capacity
* Ma trận tương quan giữa các biến

---

### 2. Tension

Phân tích sự khác biệt giữa khả năng của AI và mong muốn của người lao động.

Bao gồm:

* AI Deployment Tension Map
* Opportunity Quadrant

---

### 3. Trust & Gap

Đánh giá khoảng cách niềm tin giữa công nghệ và người lao động.

Bao gồm:

* Trust Gap Distribution
* Trust Gap theo nghề nghiệp

---

### 4. Autonomy

Xác định mức độ tự chủ phù hợp của AI Agent.

Các mức độ:

* Assistant
* Human-in-the-loop
* Semi-Autonomous
* Autonomous

---

### 5. Risk

Đánh giá các rủi ro khi triển khai AI Agent.

Bao gồm:

* Human Control Risk
* Job Security Risk
* Risk vs Opportunity Matrix

---

### 6. Recommendations

Đề xuất các nhiệm vụ nên ưu tiên triển khai AI Agent.

Bao gồm:

* Automation Sweet Spot
* Top 20 High Impact Tasks
* Pareto Analysis

---

## Kết quả nổi bật

Một số phát hiện quan trọng từ dashboard:

* Điểm Automation Capacity trung bình đạt 3.56, cao hơn mức Automation Desire trung bình là 3.21.
* Web Administrators là nhóm nghề có Agent Fit Score cao nhất.
* Database Administrators là nhóm nghề có Trust Gap lớn nhất.
* Phần lớn cơ hội triển khai nằm trong nhóm "Khả năng AI cao nhưng mức độ sẵn sàng của người lao động còn thấp".
* Mô hình Human-in-the-loop phù hợp với phần lớn nhiệm vụ được phân tích.

---

## Ý nghĩa thực tiễn

Kết quả nghiên cứu cho thấy việc triển khai AI Agent không nên chỉ dựa trên khả năng công nghệ.

Doanh nghiệp cần đồng thời xem xét:

* Năng lực của AI
* Mức độ chấp nhận của người lao động
* Quyền kiểm soát của con người
* Các rủi ro liên quan đến nghề nghiệp

Framework được đề xuất trong dự án có thể hỗ trợ doanh nghiệp xác định các cơ hội triển khai AI Agent mang lại giá trị cao và giảm thiểu rủi ro.

---

## Hạn chế của nghiên cứu

* Trọng số trong Agent Fit Score được xác định dựa trên giả định chuyên gia.
* Chưa xem xét chi phí triển khai thực tế.
* Phạm vi nghiên cứu chỉ giới hạn trong các nghề nghiệp thuộc lĩnh vực CNTT.
* Kết quả phụ thuộc vào chất lượng dữ liệu khảo sát và đánh giá chuyên gia.

---

## Hướng phát triển

* Áp dụng AHP hoặc Machine Learning để xác định trọng số tối ưu.
* Bổ sung phân tích ROI và chi phí triển khai.
* Mở rộng nghiên cứu sang các lĩnh vực ngoài CNTT.
* Xây dựng mô hình mô phỏng các kịch bản triển khai AI Agent.

---

## Công nghệ sử dụng

* Python
* Pandas
* Plotly
* Streamlit

---

## Tác giả

Nguyễn Nhật Quỳnh Lan - 030238220101

