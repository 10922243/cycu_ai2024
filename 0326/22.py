import os
import requests
from bs4 import BeautifulSoup
import shutil
import pandas as pd

def download_csv(url, save_dir):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有的csv連結和子目錄連結
    links = [a['href'] for a in soup.find_all('a') if a['href'].endswith('.csv') or a['href'].endswith('/')]

    # 按照順序下載每個csv文件或遞迴進入每個子目錄
    for link in links:
        link = url + link
        if link.endswith('.csv'):
            response = requests.get(link, stream=True)
            file_name = os.path.join(save_dir, link.split('/')[-1])
            with open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        else:
            download_csv(link, save_dir)

# 創建目錄來保存csv文件
save_dir = 'csv_files'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 指定列名
column_names = ['TimeInterval', 'GantryFrom', 'GantryTo', 'VehicleType', 'SpaceMeanSpeed', '交通量']

# 將下載的csv合併成一個csv
# Get a list of all CSV files in the save_dir directory
csv_files = [file for file in os.listdir(save_dir) if file.endswith('.csv')]

# Create an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# Iterate over each CSV file and merge its data into the merged_data DataFrame
for file in csv_files:
    file_path = os.path.join(save_dir, file)
    df = pd.read_csv(file_path, names=column_names)
    merged_data = pd.concat([merged_data, df])

# Save the merged data to a new CSV file
merged_file_path = os.path.join(save_dir, 'merged.csv')
merged_data.to_csv(merged_file_path, index=False)

url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240429/'
download_csv(url, save_dir)