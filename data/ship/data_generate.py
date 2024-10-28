import numpy as np
import pandas as pd
from scipy.stats import norm

# 设置随机种子以确保结果可重复
np.random.seed(42)

# 生成正态分布的数据
num_samples = 1000

# 可见度（越低越容易碰撞）
visibility = np.random.normal(loc=100, scale=20, size=num_samples)

# 距离（越近越容易碰撞）
distance = np.random.normal(loc=500, scale=100, size=num_samples)

# 速度（越快越容易碰撞）
speed = np.random.normal(loc=20, scale=5, size=num_samples)

# 质量（越大越容易碰撞）
mass = np.random.normal(loc=1000, scale=200, size=num_samples)

# 计算碰撞概率（正态分布）
collision_prob = norm.cdf(-visibility / 100) * norm.cdf(-distance / 500) * norm.cdf(speed / 20) * norm.cdf(mass / 1000)

# 保留三位小数
collision_prob = np.round(collision_prob, 3)

# 生成碰撞标签（二分类）
collision = np.random.binomial(1, collision_prob)

# 创建DataFrame
data = pd.DataFrame({
    'visibility': visibility,
    'distance': distance,
    'speed': speed,
    'mass': mass,
    'collision_prob': collision_prob,
    'collision': collision
})

# 保存到CSV文件
data.to_csv('collision_data.csv', index=False)

print("数据已生成并保存到 collision_data.csv")