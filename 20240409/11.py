import folium
from folium.plugins import TimestampedGeoJson
import pandas as pd

# 讀取Excel文件，從第二行開始讀取
excel_path = r'C:\Users\User\Downloads\地震活動彙整_638482866531342197.xlsx'
data = pd.read_excel(excel_path, header=1)

# 創建地圖物件
m = folium.Map(location=[23.7, 120.9], zoom_start=7)  # 台灣的經緯度中心點

# 創建一個空的 GeoJson 特徵集
features = []

# 將每個地震點轉換為 GeoJson 特徵並添加到特徵集中
for index, row in data.iterrows():
    number = row['編號']
    quake_time = row['地震時間']
    longitude = row['經度']
    latitude = row['緯度']
    depth = row['規模']
    magnitude = row['深度']

    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [longitude, latitude],
        },
        'properties': {
            'time': quake_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'popup': f"編號：{number}<br>"
                     f"地震時間：{quake_time.strftime('%Y年%m月%d日 %H時%M分%S秒')}<br>" \
                     f"震央位置：北緯 {latitude} ° 東經 {longitude} °<br>" \
                     f"地震深度：{depth} 公里<br>" \
                     f"芮氏規模：{magnitude}",
        },
    }
    features.append(feature)

# 將特徵集添加到時間序列 GeoJson 中
TimestampedGeoJson(
    {'type': 'FeatureCollection',
     'features': features},
    period='PT1H',  # 每1小時顯示一個點
    duration='P1M',  # 顯示一個月的時間
    auto_play=True,  # 自動播放
    loop=False,  # 不循環播放
    add_last_point=True,  # 在最後一個時間點添加點
    max_speed=1,  # 最大速度
    loop_button=True,  # 顯示循環播放按鈕
    date_options='YYYY-MM-DD HH:mm:ss',  # 日期顯示格式
    time_slider_drag_update=True  # 拖動時間滑塊時更新
).add_to(m)

# 顯示地圖
m.save('台灣地震時間序列.html')
