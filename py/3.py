import os
import pandas as pd

# 指定文件夹路径
folder_path = r'C:\Users\User\Desktop\python'

# 获取文件夹中所有的 CSV 文件
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 遍历所有的 CSV 文件
for csv_file in csv_files:
    # 读取 CSV 文件
    df = pd.read_csv(os.path.join(folder_path, csv_file))

    # 将 'm_val' 列中的字符串值转换为浮点数
    df['m_val'] = pd.to_numeric(df['m_val'], errors='coerce')

    # 将 DataFrame 写回到 CSV 文件中
    df.to_csv(os.path.join(folder_path, csv_file), index=False)