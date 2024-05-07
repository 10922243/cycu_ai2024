import os
import requests
from bs4 import BeautifulSoup
import shutil
import pandas as pd

def download_csv(url, save_dir, headers):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = [a['href'] for a in soup.find_all('a') if a['href'].endswith('.csv') or a['href'].endswith('/')]

    for link in links:
        link = url + link
        if link.endswith('.csv'):
            response = requests.get(link, stream=True)
            file_name = os.path.join(save_dir, link.split('/')[-1])
            with open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

            df = pd.read_csv(file_name, header=None)
            df.columns = headers
            df.to_csv(file_name, index=False)
        else:
            download_csv(link, save_dir, headers)

save_dir = 'csv_files'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240429/'
headers = ['時間', '起點里程數', '終點里程數', '車種', '車速', '交通量']
download_csv(url, save_dir, headers)

url2 = 'https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/20240429/'
headers = ['時間', '起點里程數', '方向', '車種', '交通量']
download_csv(url2, save_dir, headers)

csv_files = [file for file in os.listdir(save_dir) if file.endswith('.csv')]

merged_data = pd.DataFrame()

for file in csv_files:
    file_path = os.path.join(save_dir, file)
    df = pd.read_csv(file_path)
    if '終點里程數' not in df.columns:
        df['終點里程數'] = None
    if '車速' not in df.columns:
        df['車速'] = None
    if '方向' not in df.columns:
        df['方向'] = None
    merged_data = pd.concat([merged_data, df])

merged_data.sort_values(['起點里程數', '時間'], inplace=True)

merged_file_path = os.path.join(save_dir, 'merged.csv')
merged_data.to_csv(merged_file_path, index=False)

# 讀取CSV檔案
df = pd.read_csv('C:\Users\User\Documents\GitHub\cycu_ai2024\20240409\csv_files')

# 將 'time' 欄位的值轉換為 datetime 對象
df['time'] = pd.to_datetime(df['time'])

# 將時間以每5分鐘劃分為一個區段
df['time'] = df['time'].dt.floor('5T')

# 將時間區段轉換為類別，並獲取每個類別的編碼
df['time'] = pd.Categorical(df['time']).codes + 1

# 將 'Direction' 欄位的值轉換為對應的標籤
df['Direction'] = df['Direction'].map({'N': '1', 'S': '2'})

# 將處理後的數據儲存到一個新的CSV檔案中
df.to_csv('C:/Users/User/Desktop/labelled_file.csv', index=False)