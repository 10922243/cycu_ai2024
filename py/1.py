import os
import pandas as pd

# 指定資料夾路徑
folder_path = r'C:\Users\User\Desktop\python'

# 獲取資料夾中所有的 csv 文件
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 遍歷所有的 csv 文件
for csv_file in csv_files:
    # 讀取 csv 文件
    df = pd.read_csv(os.path.join(folder_path, csv_file), encoding='utf-8')

    # 將 'm_time' 列轉換為 datetime 對象，並只保留日期部分
    df['m_time'] = pd.to_datetime(df['m_time']).dt.date

    # 根據 'epb'，'cno'，'itemdesc' 和 'm_time' 進行分組，並將 'm_val' 的值相加
    grouped_df = df.groupby(['epb', 'cno', 'itemdesc', 'm_time'])['m_val'].sum().reset_index()

    # 新增一列將 'm_val' 的值除以 24
    grouped_df['m_val_divided_by_24'] = grouped_df['m_val'] / 24

    # 將結果寫入 excel 文件，文件名為原始 csv 文件名（去掉 `.csv` 擴展名）
    output_file = os.path.join(folder_path, csv_file.replace('.csv', '.xlsx'))
    grouped_df.to_excel(output_file, index=False)