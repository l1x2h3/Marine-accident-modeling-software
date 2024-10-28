import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# 加载数据
data = pd.read_csv('data/temp/collision_data.csv')

# 特征和标签
X = data[['visibility', 'distance', 'speed', 'mass']]
y = data['collision']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建XGBoost分类器
model = xgb.XGBClassifier(objective='binary:logistic', eval_metric='logloss')

# 训练模型
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估模型
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.4f}')
print(classification_report(y_test, y_pred))

# 导出模型
model.save_model('data/temp/xgboost_model.json')
print("模型已导出为 xgboost_model.json")