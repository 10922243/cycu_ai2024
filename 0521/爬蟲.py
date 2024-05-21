#我需要一個網路爬蟲程式，爬以下網址的資料
#url=https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/
#爬取2024年1月1日的資料到2024年4月30日的資料
#2024年1月1日的檔案類型如下是一個壓縮檔
#https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/M05A_20240101.tar.gz
#2024年4月16日檔案形式如下
#https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240416/00/TDCS_M05A_20240416_000000.csv
#https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240416/00/TDCS_M05A_20240416_000500.csv
#檔案內資料格式如下
# filename 最後面的數字代表的是小時 分鐘 與秒，例如 000000 代表 00:00:00 
# 000500 代表 00:05:00
# 如果每5分鐘一筆資料,利用迴圈產生檔名
# 例如: TDCS_M03A_20240325_000000.csv
#        TDCS_M03A_20240325_000500.csv
#也就是 2024 4 月 16 日 的 00:05:00 的資料
#請幫我自行判斷每一天的檔案狀態。import urllib.request

import requests
import datetime
import os
import urllib.request
import tarfile
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 其他程式碼...
def url_exists(url):
    response = requests.head(url)
    return response.status_code == 200

def download_file(url, filename):
    urllib.request.urlretrieve(url, filename)

start_date = datetime.date(2024, 1, 1)
end_date = datetime.date(2024, 4, 30)

current_date = start_date
while current_date <= end_date:
    file_date = current_date.strftime("%Y%m%d")
    tar_file_url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/M05A_{file_date}.tar.gz"
    tar_file_name = f"downloaded_files/M05A_{file_date}.tar.gz"

    if url_exists(tar_file_url):
        download_file(tar_file_url, tar_file_name)
        with tarfile.open(tar_file_name, 'r:gz') as tar:
            tar.extractall(path="downloaded_files")
    else:
        for hour in range(24):
            for minute in range(0, 60, 5):
                file_url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/{file_date}/{str(hour).zfill(2)}/TDCS_M05A_{file_date}_{str(hour).zfill(2)}{str(minute).zfill(2)}00.csv"
                file_name = f"downloaded_files/M05A_{file_date}_{str(hour).zfill(2)}{str(minute).zfill(2)}00.csv"
                if url_exists(file_url):
                    download_file(file_url, file_name)
    
    current_date += datetime.timedelta(days=1)