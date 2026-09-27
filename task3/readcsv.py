# 1. Khai báo các công cụ (thư viện)
import pandas as pd # Công cụ xử lý bảng dữ liệu (như Excel nhưng mạnh gấp ngàn lần)
import numpy as np  # Công cụ tính toán số học
import matplotlib.pyplot as plt # Công cụ vẽ biểu đồ cơ bản
import seaborn as sns # Công cụ vẽ biểu đồ đẹp mắt hơn

# Thiết lập một chút để biểu đồ hiển thị to rõ hơn
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")

# 2. Đọc dữ liệu từ file CSV vào "DataFrame" (viết tắt là df)
# Thay đường dẫn trong ngoặc kép bằng đường dẫn thực tế file của bạn trên Colab
print("Đang đọc dữ liệu... Sẽ mất khoảng vài giây vì file Giao dịch khá nặng (1.8 triệu dòng).")

df_month = pd.read_csv('/Users/lelinh/Documents/BI10/BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv')
df_trans = pd.read_csv('/Users/lelinh/Documents/BI10/BI10_ROUND01_DATASET/consumer_transactions_2025.csv')

print("Đọc dữ liệu thành công!")
print(f"Số dòng file Tháng: {len(df_month):,}")
print(f"Số dòng file Giao dịch: {len(df_trans):,}")
