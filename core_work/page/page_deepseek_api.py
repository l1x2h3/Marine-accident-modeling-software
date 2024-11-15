import joblib
import numpy as np
import pandas as pd
import requests
import os, sys
from openai import OpenAI

# 定义输入参数的列名
input_columns = ['d_sense_max', 'epsilon', 't_react', 'v_ship', 'v_obj', 'd_init', 'N_samples', 'bias_angle', 'time_interval']

def predict_collision_probability(input_params):
    # 调用另一个文件中的函数
    #collision_probability = get_res(input_params)
    collision_probability = 1
    
    return collision_probability

def analyze_with_deepseek(prompt):
    # 初始化 OpenAI 客户端
    client = OpenAI(api_key="sk-717a13f51d684c3eb3d10bc9d888f557", base_url="https://api.deepseek.com")
    
    # 发送请求
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    
    # 解析响应
    if response.choices:
        analysis_result = response.choices[0].message.content
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
    prompt = f"这是模仿一只船只在碰撞前的参数，以上的参数内容分别是d_sense_max: 船只在极端天气的最大感知距离 epsilon:航线规划误差 t_react: 最大反应时间 v_ship: 船只的相对速度 v_obj: 对方船只的速度 d_init: 船只的初始距离 N_samples: 蒙特卡诺采样次数  bias_angle: 两个船只对象驶向的偏角 time_interval: 驾驶员的反应时间 分析以下输入参数和预测结果的原因：\n输入参数：{input_params}\n预测结果：{collision_probability:.4f}"
    
    # 调用 DeepSeek API 进行分析
    analysis_result = analyze_with_deepseek(prompt)
    
    if analysis_result:
        print("\nDeepSeek 分析结果：")
        print(analysis_result)
    else:
        print("\nDeepSeek API 调用失败")


def use_api_part(input_params, collision_probability):
    # print("请逐行输入以下参数：")
    # input_params = []
    
    # 逐行读取用户输入
    # 下面写一个前端，用输入框输入我需要的内容
    # for col in input_columns:
    #     value = float(input(f"{col}: "))
    #     input_params.append(value)
    
    # 预测碰撞概率
    # collision_probability = predict_collision_probability(input_params)
    
    # 打印输入参数和预测结果
    # print("\n输入参数：")
    # for col, value in zip(input_columns, input_params):
    #     print(f"{col}: {value}")
    
    # print(f"\n预测的碰撞概率: {collision_probability:.4f}")
    
    # 生成 DeepSeek 的 prompt
    prompt = f"这是模仿一只船只在碰撞前的参数，以上的参数内容分别是d_sense_max: 船只在极端天气的最大感知距离 epsilon:航线规划误差 t_react: 最大反应时间 v_ship: 船只的相对速度 v_obj: 对方船只的速度 d_init: 船只的初始距离 N_samples: 蒙特卡诺采样次数  bias_angle: 两个船只对象驶向的偏角 time_interval: 驾驶员的反应时间 分析以下输入参数和预测结果的原因：\n输入参数：{input_params}\n预测结果：{collision_probability:.4f}"
    
    # 调用 DeepSeek API 进行分析
    analysis_result = analyze_with_deepseek(prompt)
    
    if analysis_result:
        print("\nDeepSeek 分析结果：")
        print(analysis_result)
    else:
        print("\nDeepSeek API 调用失败")
    
    return analysis_result