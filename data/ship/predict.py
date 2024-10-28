import xgboost as xgb
import pandas as pd
import sys

# 加载模型
model = xgb.XGBClassifier()
model.load_model('data/temp/xgboost_model.json')

# 输入参数
print("请输入以下参数（单位：米、米、米/秒、千克）：")
visibility = float(input("可见度: "))
distance = float(input("距离: "))
speed = float(input("速度: "))
mass = float(input("质量: "))

# 转换为DataFrame
input_data = {
    'visibility': [visibility],
    'distance': [distance],
    'speed': [speed],
    'mass': [mass]
}
input_df = pd.DataFrame(input_data)

# 预测
prediction = model.predict_proba(input_df)

# 输出结果
collision_prob = prediction[0][1]
print(f"预测结果：碰撞概率为 {collision_prob:.3f}")

# 后续我们的model只需要load出来就行了