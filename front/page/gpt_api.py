import joblib
import numpy as np
import pandas as pd
import requests
import os,sys

# sys.path.append(os.path.abspath('../../../'))
# from data.ship.predict import get_res

# 定义输入参数的列名
input_columns = ['d_sense_max', 'epsilon', 't_react', 'v_ship', 'v_obj', 'd_init', 'N_samples', 'bias_angle', 'time_interval']

def predict_collision_probability(input_params):
    # 调用另一个文件中的函数
    #collision_probability = get_res(input_params)
    collision_probability = 1
    
    return collision_probability

def analyze_with_deepseek(prompt):
    # DeepSeek API 接口地址
    api_url = "https://api.deepseek.com/analyze"
    
    # 请求头
    headers = {
        "Authorization": "sk-717a13f51d684c3eb3d10bc9d888f557",
        "Content-Type": "application/json"
    }
    
    # 请求体
    payload = {
        "prompt": prompt
    }
    
    # 发送请求
    response = requests.post(api_url, headers=headers, json=payload)
    
    # 解析响应
    if response.status_code == 200:
        analysis_result = response.json()
        return analysis_result
    else:
        return None

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
    
    # 生成 DeepSeek 的 prompt
    prompt = f"分析以下输入参数和预测结果的原因：\n输入参数：{input_params}\n预测结果：{collision_probability:.4f}"
    
    # 调用 DeepSeek API 进行分析
    analysis_result = analyze_with_deepseek(prompt)
    
    if analysis_result:
        print("\nDeepSeek 分析结果：")
        print(analysis_result)
    else:
        print("\nDeepSeek API 调用失败")