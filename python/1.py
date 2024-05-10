import pandas as pd

# 讀取 csv 文件
df = pd.read_csv(r'C:\Users\User\Desktop\python\2019\3.csv')

# 將 'm_time' 列轉換為 datetime 對象，並只保留日期部分
df['m_time'] = pd.to_datetime(df['m_time']).dt.date

# 根據 'epb'，'cno'，'itemdesc' 和 'm_time' 進行分組，並將 'm_val' 的值相加
grouped_df = df.groupby(['epb', 'cno', 'itemdesc', 'm_time'])['m_val'].sum().reset_index()

# 將結果寫入 excel 文件
grouped_df.to_excel(r'C:\Users\User\Desktop\python\2019\3\grouped_data.xlsx', index=False)