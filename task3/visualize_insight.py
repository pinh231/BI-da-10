import matplotlib.pyplot as plt
import seaborn as sns
from account_metric import customer_master

# Thiết lập phong cách biểu đồ
plt.style.use('seaborn-v0_8-whitegrid')

# Tạo khung vẽ biểu đồ kích thước 10x6
plt.figure(figsize=(10, 6))

# Vẽ biểu đồ phân tán
sns.scatterplot(
    data=customer_master,
    x='digital_spend_share', 
    y='engagement_score',
    alpha=0.5, # Làm mờ các điểm để nhìn rõ vùng dữ liệu dày đặc
    color='#3498db'
)

# Vẽ thêm đường xu hướng (Trendline) màu đỏ để dễ nhìn ra quy luật
sns.regplot(
    data=customer_master, 
    x='digital_spend_share', 
    y='engagement_score', 
    scatter=False, 
    color='red'
)

# Trang trí tiêu đề
plt.title('Mối quan hệ giữa Tỷ lệ chi tiêu Digital và Điểm tương tác (Engagement)', fontsize=14, fontweight='bold')
plt.xlabel('Tỷ lệ chi tiêu qua kênh Digital (Từ 0 tới 1)', fontsize=12)
plt.ylabel('Điểm Tương tác (Trung bình năm)', fontsize=12)

# Hiển thị biểu đồ
plt.show()
