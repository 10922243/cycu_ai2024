import pandas as pd
import glob
import folium

# 讀取車道位置
gantry_locations = pd.read_csv('gantry_locations.csv')

# 找到所有含有 "M05A" 的檔案
files = glob.glob('downloaded_files/*M05A*.csv') + glob.glob('downloaded_files/*M05A*.gz')

# 讀取所有檔案
data = pd.concat([pd.read_csv(f, compression='gzip' if f.endswith('.gz') else 'infer') for f in files])

# 選擇 VehicleType 為 31 的數據
data = data[data['VehicleType'] == 31]

# 合併數據和車道位置
data = pd.merge(data, gantry_locations, how='left', left_on='GantryID', right_on='GantryID')

# 創建地圖
m = folium.Map(location=[23.5, 121], zoom_start=7)

# 為每個時間點添加標記
for time in data['TimeInterval'].unique():
    temp = data[data['TimeInterval'] == time]
    for i, row in temp.iterrows():
        folium.Marker([row['Latitude'], row['Longitude']], popup=row['GantryID']).add_to(m)

# 保存地圖
m.save('map.html')

#M05A : TimeInterval、GantryFrom、GantryTo、VehicleType、SpaceMeanSpeed、交通量 請幫我讀取目錄中下載的資料夾中含"M05A"的資料，資料檔案包含gz和csv，並利用folium繪製台灣動態地圖，並有時間序列，VehicleType以"31"的為主