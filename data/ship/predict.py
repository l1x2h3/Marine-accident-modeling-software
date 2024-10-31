import joblib
import numpy as np
import pandas as pd

# 加载标准化器
scaler = joblib.load('data/ship/scaler.pkl')

# 加载模型
model = joblib.load('data/ship/best_collision_model.pkl')

# 定义输入参数的列名
input_columns = ['d_sense_max', 'epsilon', 't_react', 'v_ship', 'v_obj', 'd_init', 'N_samples', 'bias_angle', 'time_interval']

def predict_collision_probability(input_params):
    # 将输入参数转换为DataFrame
    input_df = pd.DataFrame([input_params], columns=input_columns)
    
    # 标准化输入参数
    input_scaled = scaler.transform(input_df)
    
    # 预测碰撞概率
    collision_probability = model.predict(input_scaled)[0]
    
    return collision_probability

if __name__ == "__main__":
    print("请逐行输入以下参数：")
    input_params = []
    
    # 逐行读取用户输入
    for col in input_columns:
        value = float(input(f"{col}: "))
        input_params.append(value)
    
    # 预测碰撞概率
    collision_probability = predict_collision_probability(input_params)
    
    # 打印输入参数和预测结果
    print("\n输入参数：")
    for col, value in zip(input_columns, input_params):
        print(f"{col}: {value}")
    
    print(f"\n预测的碰撞概率: {collision_probability:.4f}")