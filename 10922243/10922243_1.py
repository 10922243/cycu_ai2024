#給我一段爬蟲的程式碼，先建立一個資料夾'M05A'在"c:\Users\x\Downloads"中 
#接著在'https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/'這個網站上下載壓縮檔 
#我需要從'20240101'到'20240419'的所有檔案，並儲存在這個資料夾中 
#如果沒有壓縮檔，則改為以迴圈的方式下載每五分鐘的 csv 檔案，直到沒有檔案可下載為止 
#接著新增一個資料夾'解壓縮後'於'M05A'中，用迴圈的方式進行解壓縮，並將所有解壓縮後的檔案儲存於該資料夾中 
#然後刪除原本的壓縮檔 #最後合併所有的 csv 檔案，並將其儲存於'M05A'資料夾中

import os
import requests
import pandas as pd
from datetime import timedelta, date
import tarfile
import time
from pathlib import Path

# 建立資料夾
base_dir = r"c:\Users\x\Downloads\M05A"
os.makedirs(base_dir, exist_ok=True)

# 建立解壓縮後的資料夾
extract_dir = os.path.join(base_dir, '解壓縮後')
os.makedirs(extract_dir, exist_ok=True)

# 建立日期範圍
start_date = date(2024, 1, 1)
end_date = date(2024, 4, 30)
delta = timedelta(days=1)

# 下載壓縮檔或 CSV 檔案
while start_date <= end_date:
    date_str = start_date.strftime("%Y%m%d")
    tar_url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/M05A_{date_str}.tar.gz"
    tar_path = os.path.join(base_dir, f"M05A_{date_str}.tar.gz")
    response = requests.get(tar_url)
    if response.status_code == 200:
        with open(tar_path, 'wb') as f:
            f.write(response.content)
    else:
        for i in range(24):
            for j in range(0, 60, 5):
                csv_url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/{date_str}/{i:02d}/TDCS_M05A_{date_str}_{i:02d}{j:02d}00.csv"
                csv_path = os.path.join(base_dir, f"TDCS_M05A_{date_str}_{i:02d}{j:02d}00.csv")
                response = requests.get(csv_url)
                if response.status_code == 200:
                    with open(csv_path, 'wb') as f:
                        f.write(response.content)
                else:
                    break
    start_date += delta

# 解壓縮檔案並刪除壓縮檔
for file in os.listdir(base_dir):
    if file.endswith(".tar.gz"):
        file_path = os.path.join(base_dir, file)
        with tarfile.open(file_path, 'r:gz') as tar:
            tar.extractall(path=extract_dir)
        os.remove(file_path)


# 合併檔案
# 這段程式碼會根據日期來選擇合併方式。如果日期小於或等於 2024-04-30，則使用第一種方式合併；否則，使用第二種方式合併。
# 建立日期範圍
dates = pd.date_range(start='20240101', end='20240430')

# 合併所有 CSV 檔案
dfs = [pd.read_csv(f"C:\\Users\\x\\Downloads\\M05A\\解壓縮後\\M05A\\{filename}") for filename in os.listdir("C:\\Users\\x\\Downloads\\M05A\\解壓縮後\\M05A") if filename.endswith('.csv')]
df = pd.concat(dfs, ignore_index=True) if dfs else print("在指定的目錄下沒有找到任何 CSV 檔案。")

df2 = pd.read_csv(r"C:\Users\x\Downloads\國道計費門架座標及里程牌價表104.09.04版_373038.csv", encoding="cp950", usecols=["編號", "緯度(北緯)", "經度(東經)"])
df2 = df2.rename(columns={"緯度(北緯)": "緯度", "經度(東經)": "經度", "編號": "Gantry"})
df2["Gantry"] = df2["Gantry"].str.replace("-", "").str.replace(".", "")

# 合併 df 和 df2
df = df.merge(df2, left_on="GantryFrom", right_on="Gantry", how="left").rename(columns={"緯度": "緯度(GantryFrom)", "經度": "經度(GantryFrom)"}).drop(columns=["Gantry"])
df = df.merge(df2, left_on="GantryTo", right_on="Gantry", how="left").rename(columns={"緯度": "緯度(GantryTo)", "經度": "經度(GantryTo)"}).drop(columns=["Gantry"])
print(df)    