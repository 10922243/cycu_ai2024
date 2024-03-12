import pandas as pd


#得到這個檔案 __file__ 是這個檔案的路徑
import os
path = os.path.abspath(__file__)
#get the folder of this file
path = os.path.dirname(path)


# 從 Excel 文件讀取數據
excel_file = '112年1-10月交通事故簡訊通報資料.xlsx'

filepath = os.path.join(path ,excel_file)


# 讀取 Excel 文件
df = pd.read_excel(filepath, sheet_name='交通事故簡報通報資料')

#篩選 欄位名稱 為'國道名稱' 的資料， 我只要名稱為'國道1號'的資料
df1 = df[df['國道名稱'] == '國道3號']
# 將 "方向" 列的 "南向" 值替換為 "南"，"北向" 值替換為 "北"
df['方向'] = df['方向'].replace({'南向': '南', '北向': '北', '東向': '東', '西向': '西'})
#篩選方向為'南'的資料
df1 = df1[df1['方向'] == '北']

#把 欄位 '年' '月' '日' '時' '分'
#合併成一個欄位 '日期' , 並且轉換成日期格式
df1['事件開始'] = df1['年'].astype(str) + '-' + df1['月'].astype(str) + '-' + df1['日'].astype(str) + ' ' + df1['時'].astype(str) + ':' + df1['分'].astype(str)
df1['事件開始'] = pd.to_datetime(df1['事件開始'])

#把 欄位 '年' '月' '日' '事件排除'  合併成一個欄位 '事件排除' , 並且轉換成日期格式
df1['事件排除'] = df1['年'].astype(str) + '-' + df1['月'].astype(str) + '-' + df1['日'].astype(str) + ' ' + df1['事件排除'].astype(str)
df1['事件排除'] = pd.to_datetime(df1['事件排除'])

#drop 欄位 '年' '月' '日' '時' '分'
df1 = df1.drop(columns=['年', '月', '日', '時', '分'])


#將 '事件開始' '事件排除' 兩個欄位轉換成 unix time stamp 並使用整數表示
import pandas as pd

# 假設 df 是您的 DataFrame，並且 '事件開始' 和 '事件排除' 是 datetime 欄位

df1['事件開始1'] = df1['事件開始'].apply(lambda x: int(x.timestamp()))
df1['事件排除1'] = df1['事件排除'].apply(lambda x: int(x.timestamp()))

#只印出 '事件開始' '事件排除' '國道名稱' '事件類型' '事件描述'
print(df1[['事件開始', '事件排除', '國道名稱','里程','事件開始1','事件排除1']])

#以 '里程' 為 y軸 , '事件開始1' 為 x軸 起點 , '事件排除1' 為 x軸 終點 繪製線段
import matplotlib.pyplot as plt

# 假設 df 是您的 DataFrame
for index, row in df1.iterrows():
    plt.plot([row['事件開始1'], row['事件排除1']], [row['里程'], row['里程']])

from matplotlib.font_manager import FontProperties

# 設定字體為 SimHei
myfont = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
plt.rcParams['axes.unicode_minus'] = False

# 在標題、軸標籤和圖例中使用設定的字體
plt.title('國道3號北向', fontproperties=myfont)
plt.xlabel('事件時間', fontproperties=myfont)
plt.ylabel('里程', fontproperties=myfont)
plt.show()