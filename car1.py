import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 讀取 Excel 文件
df = pd.read_excel('C:\\Users\\User\\Documents\\GitHub\\cycu_ai2024\\112年1-10月交通事故簡訊通報資料.xlsx')

# 將 "方向" 列的 "南向" 值替換為 "南"，"北向" 值替換為 "北"
df['方向'] = df['方向'].replace({'南向': '南', '北向': '北', '東向': '東', '西向': '西'})

# 按照 "里程" 和 "方向" 列來分組資料，並計算每個組別的 "事件發生" 次數
grouped_df = df.groupby(['里程', '方向'])['事件發生'].count().reset_index()

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 繪製圖表
plt.figure(figsize=(10, 6))
sns.barplot(x='里程', y='事件發生', hue='方向', data=grouped_df)
plt.xlabel('里程')
plt.ylabel('事件發生次數')
plt.title('每個里程的事件發生次數')

# 設定 y 軸的範圍，將最大值向上取整到最接近的 10 的倍數
plt.ylim(0, np.ceil(grouped_df['事件發生'].max() / 10) * 10)

plt.show()