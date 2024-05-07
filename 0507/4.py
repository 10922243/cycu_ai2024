import io
import requests
import datetime
import requests
import pandas as pd



# M03A : TimeInterval、GantryID、Direction、VehicleType、交通量
# M04A : TimeInterval、GantryFrom、GantryTo、VehicleType、TravelTime、交通量
# M05A : TimeInterval、GantryFrom、GantryTo、VehicleType、SpaceMeanSpeed、交通量
# M06A : VehicleType、DetectionTime_O、GantryID_O、DetectionTime_D、GantryID_D、TripLength、TripEnd、TripInformation

data_columns = {
    'M03A':['TimeInterval','GantryID','Direction','VehicleType','TrafficVolume'],
    'M04A':['TimeInterval','GantryFrom','GantryTo','VehicleType','TravelTime','TrafficVolume'],
    'M05A':['TimeInterval','GantryFrom','GantryTo','VehicleType','SpaceMeanSpeed','TrafficVolume']
    }

#define a function to get one day data
def get_one_day_data(year, month, day, data_type):

    today = datetime.datetime(year, month, day, 0, 0, 0)

    if data_type not in data_columns:
        raise ValueError('data_type should be one of M03A, M04A, M05A, M06A')
       
    df_columns = data_columns[data_type]

    target_df = pd.DataFrame(columns=df_columns)

    # sample url https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/20240429/00/TDCS_M03A_20240429_005500.csv
    for i in range(0, 288):
        timestep = today + datetime.timedelta(minutes=5*i)
        timestep_str_d = timestep.strftime('%Y%m%d')
        timestep_str_h = timestep.strftime('%H')
        timestep_str_m = timestep.strftime('%H%M00')

        filename = 'TDCS_' + data_type + '_' + timestep_str_d + '_' + timestep_str_m + '.csv'

        url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/' + data_type + '/' + timestep_str_d + '/' + timestep_str_h + '/' + filename

        print(url)
        r = requests.get(url)

        # convert r to dataframe without column names in the first row
        # specify header=None to avoid the first row being treated as column names
        # column names will be {'t','g','d','vtype','num'}
        df = pd.read_csv(io.StringIO(r.text), header=None)
        df.columns = df_columns
        
        target_df = pd.concat([target_df, df], ignore_index=True)
        print (target_df.head(), target_df.tail(), target_df.shape)

    output_filename = 'data/TDCS_' + data_type + '_' + timestep_str_d + '.csv'
    target_df.to_csv(output_filename, index=False)

    return target_df



if __name__ == '__main__':
    # 讀取 CSV 檔案
    df = pd.read_csv('C:\\Users\\User\\Documents\\GitHub\\cycu_ai2024\\csv_files\\merged.csv', header=0)
    
    print(df.head(), df.tail(), df.shape)
    df_31 = df [df['VehicleType'] == 31]
    df_32 = df [df['VehicleType'] == 32]
    df_41 = df [df['VehicleType'] == 41]
    df_42 = df [df['VehicleType'] == 42]
    df_5  = df [df['VehicleType'] == 5]

    df_31.reset_index(drop=True, inplace=True)
    df_32.reset_index(drop=True, inplace=True)
    df_41.reset_index(drop=True, inplace=True)
    df_42.reset_index(drop=True, inplace=True)
    df_5.reset_index(drop=True, inplace=True)

    df_5['tv31']    = df_31['TrafficVolume']
    df_5['tv32']    = df_32['TrafficVolume']
    df_5['tv41']    = df_41['TrafficVolume']
    df_5['tv42']    = df_42['TrafficVolume']
    df_5['tv5']     = df_5['TrafficVolume']

    # Print the updated dataframe
    print(df_5.head(), df_5.tail(), df_5.shape)

    #df_31 將使用來進行機器學習，在之前我們需要先對資料進行 feature engneering
    #1. 將 TimeInterval 轉換成 每日的第幾個五分鐘(0~287)                                    
    print(df_31.head())
    df_31['TimeInterval'] = df_31['TimeInterval'].str.slice(11, 16)
    df_31['TimeInterval'] = df_31['TimeInterval'].str.replace(':', '')
    df_31['TimeInterval'] = df_31['TimeInterval'].str.slice(0, 2).astype(int) * 12 + df_31['TimeInterval'].str.slice(2, 4).astype(int) / 5

    #2. GratryFrom 代表地點，首先我們只取出 所有前三的字元是 'F01' 與結尾是 'S' 的資料，並將'F01'取代成空字串，'S'取代成空字串
    df_31 = df_31[df_31['GantryFrom'].str.slice(0, 3) == 'F01']
    #剩下的字元轉換成數字 代表道路的里程數
    df_31['GantryFrom'] = df_31['GantryFrom'].str.replace('F01', '')
    df_31['GantryFrom'] = df_31['GantryFrom'].str.replace('S', '')
    df_31['GantryFrom'] = df_31['GantryFrom'].astype(int)

    print(df_31.head(), df_31.tail(), df_31.shape)

    #3.SpaceMeanSpeed 代表速度，20以下作為一區間 紫色，20~39作為一區間 紅色，40~59作為一區間 橘色，60~79以上作為一區間 黃色，80以上作為一區間 綠色
    #將 SpaceMeanSpeed 進行特徵化
    df_31['SpaceMeanSpeed'] = pd.cut(df_31['SpaceMeanSpeed'], bins=[0, 20, 40, 60, 80, 100], labels=['purple', 'red', 'orange', 'yellow', 'green'])
    #繪製xyz圖，x軸是TimeInterval，y軸是GantryFrom，z軸是SpaceMeanSpeed的3D圖
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df_31['TimeInterval'], df_31['GantryFrom'], df_31['SpaceMeanSpeed'])
    plt.show()
    

