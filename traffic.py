import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# 假設你的資料儲存在一個名為 'data.csv' 的 CSV 檔案中
data = pd.read_csv('data.csv') 

# 將地點和時間轉換為數值
le = LabelEncoder()
data['地點'] = le.fit_transform(data['地點'])
data['時間'] = le.fit_transform(data['時間'])

# 建立標籤
data['標籤'] = data['車速'].apply(lambda x: '順暢' if x >= 70 else '車多')

# 將特徵和標籤分開
X = data[['地點', '里程數', '時間']]
y = data['標籤']

# 分割訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 建立 SVC 模型
svc = SVC()
svc.fit(X_train, y_train)

# 進行預測
y_pred = svc.predict(X_test)

# 計算準確率
accuracy = accuracy_score(y_test, y_pred)
print(f'準確率: {accuracy:.2f}')