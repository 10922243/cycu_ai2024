import folium
import pandas as pd

# 讀取Excel文件，從第二行開始讀取
excel_path = r'C:\Users\User\Downloads\地震活動彙整_638482866531342197.xlsx'
data = pd.read_excel(excel_path, header=1)

# 創建地圖物件
m = folium.Map(location=[23.7, 120.9], zoom_start=7)  # 台灣的經緯度中心點

# 在地圖上標註位置
for index, row in data.iterrows():
    quake_time = row['地震時間']
    longitude = row['經度']
    latitude = row['緯度']
    depth = row['規模']
    magnitude = row['深度']

    popup_text = f"地震時間：{quake_time.strftime('%Y年%m月%d日 %H時%M分%S秒')}<br>" \
                 f"震央位置：北緯 {latitude} ° 東經 {longitude} °<br>" \
                 f"地震深度：{depth} 公里<br>" \
                 f"芮氏規模：{magnitude}"
    
    folium.Marker([latitude, longitude], popup=popup_text).add_to(m)

# 顯示地圖
m.save('台灣地震分佈.html')
