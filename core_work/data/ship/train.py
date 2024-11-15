import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# 加载数据
df = pd.read_csv('data/temp/collision_data.csv')

# 处理输入特征和目标变量
X = df[['d_sense_max', 'epsilon', 't_react', 'v_ship', 'v_obj', 'd_init', 'N_samples', 'bias_angle', 'time_interval']]
y = df['collision_probability']

# 标准化特征
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 定义模型
models = {
    'Linear Regression': LinearRegression(),
    'Decision Tree Regression': DecisionTreeRegressor(),
    'Random Forest Regression': RandomForestRegressor(),
    'Support Vector Regression': SVR()
}

# 交叉验证评估模型性能
results = {}
for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    results[name] = -scores.mean()

# 选择性能最好的模型
best_model_name = min(results, key=results.get)
best_model = models[best_model_name]

# 训练最佳模型
best_model.fit(X_train, y_train)

# 在测试集上评估模型
y_pred = best_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Best Model: {best_model_name}")
print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# 保存最佳模型
joblib.dump(best_model, 'data/temp/best_collision_model.pkl')

# 保存标准化器
joblib.dump(scaler, 'data/temp/scaler.pkl')