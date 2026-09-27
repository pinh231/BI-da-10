import pandas as pd
from readcsv import df_trans, df_month
from avg_month_point import customer_master

# -- BƯỚC BỔ SUNG: Tính tổng chi tiêu theo từng kênh giao dịch --
spend_by_channel = df_trans.pivot_table(
    index='consumer_id', 
    columns='transaction_channel', 
    values='spend_amount_vnd', 
    aggfunc='sum', 
    fill_value=0
)
# Đổi tên cột cho khớp với công thức bên dưới (spend_POS, spend_E-commerce...)
spend_by_channel.columns = ['spend_' + col for col in spend_by_channel.columns]

# Ghép bảng chi tiêu này vào bảng customer_master
customer_master = pd.merge(customer_master, spend_by_channel, on='consumer_id', how='left')

# 1. Tính tổng chi tiêu cả năm
customer_master['total_spend'] = customer_master[['spend_POS', 'spend_E-commerce', 'spend_Mobile App', 'spend_QR Payment', 'spend_Recurring Payment']].sum(axis=1)

# 2. Tính tỷ lệ Digital Spend (Theo định nghĩa: E-commerce + Mobile App + QR)
customer_master['digital_spend'] = customer_master['spend_E-commerce'] + customer_master['spend_Mobile App'] + customer_master['spend_QR Payment']
customer_master['digital_spend_share'] = customer_master['digital_spend'] / customer_master['total_spend']

# 3. Recency (Số ngày gần nhất từ lần quẹt thẻ cuối đến cuối năm)
# Chuyển cột thời gian về định dạng Date
df_trans['activity_datetime'] = pd.to_datetime(df_trans['activity_datetime'])
# Tìm ngày giao dịch cuối cùng của mỗi khách
last_txn_date = df_trans.groupby('consumer_id')['activity_datetime'].max().reset_index()
last_txn_date.rename(columns={'activity_datetime': 'last_transaction_date'}, inplace=True)
# Mốc thời gian đối chiếu (Ngày cuối năm 2025)
reference_date = pd.to_datetime('2025-12-31')
last_txn_date['recency_days'] = (reference_date - last_txn_date['last_transaction_date']).dt.days

# Ghép Recency vào bảng Master
customer_master = pd.merge(customer_master, last_txn_date[['consumer_id', 'recency_days']], on='consumer_id', how='left')

# Xem thành quả tuyệt vời của chúng ta
print(customer_master.head())
