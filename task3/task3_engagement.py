import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# CHUẨN BỊ DỮ LIỆU
# ==========================================
print("Đang đọc dữ liệu, vui lòng đợi...")
df_month = pd.read_csv('BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv')
df_trans = pd.read_csv('BI10_ROUND01_DATASET/consumer_transactions_2025.csv')

# Thiết lập biểu đồ
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")

# ==========================================
# YÊU CẦU 1: Phân phối Engagement Score
# ==========================================
print("\n--- YÊU CẦU 1: PHÂN BỔ ENGAGEMENT SEGMENT ---")
segment_pct = df_month['engagement_segment'].value_counts(normalize=True) * 100
print(segment_pct.round(2).astype(str) + '%')

plt.figure(figsize=(10, 6))
sns.histplot(data=df_month, x='engagement_score', hue='engagement_segment', multiple='stack', bins=40)
plt.title('Yêu cầu 1: Phân phối Engagement Score theo Segment')
plt.xlabel('Engagement Score')
plt.ylabel('Số lượng')
plt.show()

# ==========================================
# YÊU CẦU 2: Channel Adoption
# ==========================================
print("\n--- YÊU CẦU 2: TỶ LỆ SỬ DỤNG KÊNH GIAO DỊCH ---")
channel_usage = df_trans['transaction_channel'].value_counts(normalize=True) * 100
print(channel_usage.round(2).astype(str) + '%')

plt.figure(figsize=(10, 6))
sns.barplot(x=channel_usage.index, y=channel_usage.values, palette='viridis')
plt.title('Yêu cầu 2: Tỷ lệ sử dụng các kênh giao dịch (Channel Adoption)')
plt.ylabel('% Sử dụng')
plt.show()

# ==========================================
# YÊU CẦU 3: Category Diversity
# ==========================================
corr_cat = df_month['category_diversity'].corr(df_month['engagement_score'])
print(f"\n--- YÊU CẦU 3: TƯƠNG QUAN CATEGORY DIVERSITY ---")
print(f"Hệ số tương quan (Correlation) với Engagement Score: {corr_cat:.2f}")

plt.figure(figsize=(10, 6))
sns.boxplot(data=df_month, x='category_diversity', y='engagement_score', palette='coolwarm')
plt.title(f'Yêu cầu 3: Phân phối Engagement theo Category Diversity\n(Tương quan r = {corr_cat:.2f})')
plt.xlabel('Số lượng danh mục chi tiêu (Category Diversity)')
plt.show()

# ==========================================
# YÊU CẦU 4: Recency & Frequency
# ==========================================
print("\n--- YÊU CẦU 4: XUẤT BIỂU ĐỒ RECENCY & FREQUENCY ---")
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

sns.scatterplot(data=df_month, x='transaction_recency_days', y='engagement_score', alpha=0.3, ax=axes[0])
axes[0].set_title('Recency (Số ngày từ giao dịch cuối) vs Engagement')
axes[0].invert_xaxis() # Lật ngược trục X vì Recency càng nhỏ càng tốt

sns.scatterplot(data=df_month, x='transaction_count', y='engagement_score', alpha=0.3, color='green', ax=axes[1])
axes[1].set_title('Frequency (Số lượng giao dịch) vs Engagement')

plt.tight_layout()
plt.show()

# ==========================================
# YÊU CẦU 5: Nhóm "Healthy nhưng Disengaged"
# ==========================================
print("\n--- YÊU CẦU 5: NHÓM 'HEALTHY NHƯNG DISENGAGED' ---")
# Cutoff: Sức khỏe >= 80 (Khỏe mạnh/Ổn định) VÀ Tương tác < 40 (Thấp/Bỏ đi)
healthy_disengaged = df_month[(df_month['financial_health_score'] >= 80) & (df_month['engagement_score'] < 40)]

total_rows = len(df_month)
hd_size = len(healthy_disengaged)
hd_pct = (hd_size / total_rows) * 100

print(f"- Quy mô: {hd_size} trường hợp (trên tổng số {total_rows})")
print(f"- Chiếm tỷ lệ: {hd_pct:.2f}% tổng dữ liệu")
print("- Lý giải chọn ngưỡng:")
print("  + Financial Score >= 80: Đảm bảo đây là nhóm có tài chính cực kỳ ổn định, ít nợ xấu, tiêu xài trong tầm kiểm soát.")
print("  + Engagement Score < 40: Mức điểm báo động đỏ cho thấy họ đang dần rời bỏ hệ sinh thái (ít quẹt thẻ, ít đăng nhập).")
print("  => Đây là tập khách hàng VIP 'ngủ đông'. Thay vì phạt họ, công ty nên gọi điện chăm sóc hoặc tặng voucher để đánh thức nhu cầu chi tiêu!")
print("==========================================")
