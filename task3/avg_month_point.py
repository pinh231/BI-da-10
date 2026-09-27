from readcsv import df_month
import pandas as pd


# Tạo bảng thông tin cơ bản: Lấy tuổi, giới tính, tỉnh thành của khách
# (Vì tuổi hay giới tính thì tháng nào cũng vậy, nên ta chỉ cần lấy dòng đầu tiên của mỗi khách)
customer_profile = df_month.groupby('consumer_id').first()[['age', 'gender', 'province_city']]

# Tính điểm Engagement và Health trung bình của cả năm 2025 cho từng khách
customer_scores = df_month.groupby('consumer_id').agg({
    'engagement_score': 'mean',      # Lấy trung bình điểm tương tác
    'financial_health_score': 'mean',# Lấy trung bình điểm sức khỏe
    'transaction_count': 'sum',      # Cộng tổng số lần quẹt thẻ trong năm (Frequency)
    'category_diversity': 'max',     # Lấy số đa dạng danh mục cao nhất họ đạt được
}).reset_index() # Reset index để consumer_id biến lại thành 1 cột bình thường

# Ghép 2 bảng lại với nhau
customer_master = pd.merge(customer_scores, customer_profile, on='consumer_id', how='left')

# Xem thử 5 dòng đầu tiên
print(df_month.head())
