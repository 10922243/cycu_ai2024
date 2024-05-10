import os
import pandas as pd
from collections import defaultdict

# 指定文件夹路径
folder_path = r'C:\Users\User\Desktop\python'

# 获取文件夹中所有的 Excel 文件
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# 创建一个字典来存储每个前缀对应的 DataFrame
dfs = defaultdict(pd.DataFrame)

# 遍历所有的 Excel 文件
for excel_file in excel_files:
    # 提取文件名前缀
    prefix = excel_file.rsplit('(', 1)[0]

    # 读取 Excel 文件
    df = pd.read_excel(os.path.join(folder_path, excel_file))

    # 将 'm_time' 列转换为 datetime 对象，并只保留日期部分
    df['m_time'] = pd.to_datetime(df['m_time']).dt.date

    # 根据 'epb'，'cno'，'itemdesc' 和 'm_time' 进行分组，并将 'm_val' 的值相加
    grouped_df = df.groupby(['epb', 'cno', 'itemdesc', 'm_time'])['m_val'].sum().reset_index()

    # 新增一列将 'm_val' 的值除以 24
    grouped_df['m_val_divided_by_24'] = grouped_df['m_val'] / 24

    # 将分组的结果添加到对应的 DataFrame 中
    dfs[prefix] = pd.concat([dfs[prefix], grouped_df])

# 遍历字典，将每个 DataFrame 写入到一个新的 Excel 文件中
for prefix, df in dfs.items():
    output_file = os.path.join(folder_path, f'{prefix}_grouped.xlsx')
    df.to_excel(output_file, index=False)