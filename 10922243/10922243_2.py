# 用迴圈方式讀取此 CSV 檔案 從 "c:\Users\x\Downloads\M05A\解壓縮後\M05A\M05A_20240101.csv" c:\Users\x\Downloads\M05A\解壓縮後\M05A\M05A_20240430.csv"
# 並做以下處理 
# 將 TimeInterval 欄位轉換成每天的第幾個5分鐘(1~288)
# 新增 "WEEKDAY" 欄位，根據 TimeInterval 欄位，顯示該筆資料是星期幾(星期日到星期六為0到6)   
# 新增 "HELLDAY" 欄位，根據 TimeInterval 欄位，顯示該筆資料是否為假日(0為非假日，1為假日，-1為假日前一天)，假日定義為星期六、星期日及中秋節、元旦、春節、清明節、端午節、國慶日、勞動節、雙十節、元宵節、重陽節、除夕
# 新增 "WAYIDFROM" 欄位，顯示根據 "GantryFrom" 欄位對應的前三碼(字串)
# 新增 **WayIDTo** 欄位：顯示根據 "GantryTo" 欄位對應的前三碼(字串)
# 新增 **WayMilageFrom**欄位：顯示根據 "GantryFrom" 欄位對應的第 4 碼到第 7 碼(數值)
# 新增 **WayMilageTo** 欄位：顯示根據 "GantryTo" 欄位對應的第 4 碼到第 7 碼(數值)
# 新增 **WayDirectionFrom**：顯示根據 "GantryFrom"對應的最後一碼（字串，N：北，S：南，W：西，E：東）
# 新增 **WayDirectionTo**：顯示根據 "GantryTo"對應的最後一碼（字串，N：北，S：南，W：西，E：東）
# 新增 **速度分級 SpeedClass** 欄位：（0, 1, 2, 3, 4, 5）
# 0: 速度 < 20
# 1: 20 <= 速度 < 40
# 2: 40 <= 速度 < 60
# 3: 60 <= 速度 < 80
# 4: 80 <= 速度 < 100
# 5:       速度 >= 100
# 存於此位置 c:\Users\x\Downloads\M05A\特徵化過的M05A"，並命名為 "M05A_20240101_feature.csv"，"M05A_20240102_feature.csv"，...，"M05A_20240430_feature.csv"，每個檔案的內容為上述處理後的資料
import pandas as pd
from datetime import datetime

# 定義假日
holidays = ['2024-01-01', '2024-02-10', '2024-02-11', '2024-02-12', '2024-04-04', '2024-05-01', '2024-05-12', '2024-09-15', '2024-10-10', '2024-02-24', '2024-09-28', '2024-02-09']

# 生成日期範圍
dates = pd.date_range(start='2024-01-01', end='2024-04-30')

# 迴圈讀取和處理每一個 CSV 檔案
for date in dates:
    # 讀取 CSV 檔案  從此 位置 讀取"C\\Users\\x\\Downloads\\M05A\\解壓縮後\\M05A.csv"   
    data = pd.read_csv(fNo such file or directory: 'C:\\Users\\x\\Downloads\\M05A\\解壓縮後\\M05A.csv'")

    # 若資料中有 TimeInterval GantryFrom GantryTo 皆相同的資料合併成同一行，並保留 v31, v32, v41, v5 ，SpaceMeanSpeed 的第一個出現的值
    data = data.groupby(["TimeInterval", "GantryFrom", "GantryTo"]).agg({'v31': 'first', 'v32': 'first', 'v41': 'first', 'v5': 'first', 'SpaceMeanSpeed': 'first'}).reset_index()

    # 將 TimeInterval 欄位轉換成日期格式
    data["Date"] = pd.to_datetime(data["TimeInterval"])

    # 新增 "WEEKDAY" 欄位，根據 TimeInterval 欄位，顯示該筆資料是星期幾(星期日到星期六為0到6)
    data["WEEKDAY"] = data["Date"].dt.dayofweek

    # 新增 "HELLDAY" 欄位，根據 TimeInterval 欄位，顯示該筆資料是否為假日(0為非假日，1為假日，-1為假日前一天)，假日定義為星期六、星期日及中秋節、元旦、春節、清明節、端午節、國慶日、勞動節、雙十節、元宵節、重陽節、除夕
    data["HELLDAY"] = data["Date"].apply(lambda x: 1 if x.strftime('%Y-%m-%d') in holidays or x.weekday() >= 5 else (0 if (x + pd.Timedelta(days=1)).strftime('%Y-%m-%d') not in holidays and x.weekday() < 5 else -1))

    # 將 TimeInterval 欄位轉換成每天的第幾個5分鐘(1~288)
    data["TimeInterval"] = data["TimeInterval"].apply(lambda x: datetime.strptime(x, '%Y/%m/%d %H:%M').hour * 12 + datetime.strptime(x, '%Y/%m/%d %H:%M').minute // 5 + 1)

    # 其他的程式碼...
    # 新增 "WAYIDFROM" 欄位
    data["WAYIDFROM"] = data["GantryFrom"].apply(lambda x: x[:3])

    # 新增 "WayIDTo" 欄位
    data["WayIDTo"] = data["GantryTo"].apply(lambda x: x[:3])

    # 新增 "WayMilageFrom"欄位
    # 將 "GantryFrom" 欄位的第 4 到第 7 個字元轉換為整數，如果無法轉換，則改為 第 5 個字元 到 第 7 個字元轉換為整數
    data["WayMilageFrom"] = data["GantryFrom"].apply(lambda x: int(x[3:7]) if x[3:7].isdigit() else int(x[4:7]))

    # 新增 "WayMilageTo" 欄位的第 4 到第 7 個字元轉換為整數，如果無法轉換，則改為 第 5 個字元 到 第 7 個字元轉換為整數
    data["WayMilageTo"] = data["GantryTo"].apply(lambda x: int(x[3:7]) if x[3:7].isdigit() else int(x[4:7]))

    # 新增 "WayDirectionFrom"
    data["WayDirectionFrom"] = data["GantryFrom"].apply(lambda x: x[-1])

    # 新增 "WayDirectionTo"
    data["WayDirectionTo"] = data["GantryTo"].apply(lambda x: x[-1])

    # 新增 "速度分級 SpeedClass" 欄位
    bins = [-1, 20, 40, 60, 80, 100, float('inf')]
    labels = [0, 1, 2, 3, 4, 5]
    data["SpeedClass"] = pd.cut(data["SpaceMeanSpeed"], bins=bins, labels=labels)

    # 將檔案重新命名為 'M05A_日期_feature'，並存檔於指定位置 "C:\Users\x\Downloads\M05A\解壓縮後\M05A特徵化"
    data.to_csv(f"C:\\Users\\x\\Downloads\\M05A\\解壓縮後\\M05A特徵化\\M05A_{date.strftime('%Y%m%d')}_feature.csv", index=False)

    print(f"已處理 {date.strftime('%Y-%m-%d')} 的資料")