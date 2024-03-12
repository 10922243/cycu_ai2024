import pandas as pd

# 讀取 Excel 文件
df = pd.read_excel('C:\\Users\\User\\Documents\\GitHub\\cycu_ai2024\\112年1-10月交通事故簡訊通報資料.xlsx')

# 指定 "國道名稱"、"里程" 和 "方向" 的值
specified_road_name = '國道3號'
specified_mileage = 54  # 將里程改為數字
specified_direction = '南'

# 篩選出符合指定 "國道名稱"、"里程" 和 "方向" 的資料
filtered_df = df[(df['國道名稱'] == specified_road_name) & (df['里程'] == specified_mileage) & (df['方向'] == specified_direction)]

# 計算 "事件發生" 列的出現次數
event_count = filtered_df['事件發生'].count()

print(event_count)