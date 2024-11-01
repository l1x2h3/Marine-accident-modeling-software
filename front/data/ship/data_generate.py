from collision_model import calculate_collision_probability,weather_factors,weather_probabilities
import numpy as np
import pandas as pd
# 生成数据
def generate_data(num_samples):
    data = []
    for _ in range(num_samples):
        d_sense_max = np.random.uniform(500, 1500)  # 最大感知距离（米）
        epsilon = np.random.uniform(20, 100)        # 航线规划误差（米）
        t_react = np.random.uniform(5, 20)          # 注意力反应时间（秒）
        v_ship = np.random.uniform(5, 20)           # 船只速度（米/秒）
        v_obj = np.random.uniform(2, 10)            # 动态物体速度（米/秒）
        d_init = np.random.uniform(1000, 3000)      # 初始距离（米）
        N_samples = np.random.randint(500, 2000)    # 采样次数
        bias_angle = np.random.uniform(0, 90)       # 偏向角（°）
        time_interval = np.random.uniform(1, 10)    # 时间间隔（秒）
        
        # 定义船只和动态物体的俯视图形状
        ship_shapes = [
            np.array([[0, 0], [100, 0], [100, 20], [50, 40], [0, 20]]),  # 五边形
            np.array([[0, 0], [50, 0], [50, 10], [25, 20], [0, 10]])     # 四边形
        ]
        
        obj_shapes = [
            np.array([[50, 0], [150, 0], [150, 20], [100, 40], [50, 20]]),  # 五边形
            np.array([[50, 0], [100, 0], [100, 10], [75, 20], [50, 10]])    # 四边形
        ]
        
        # 船只类型和数量
        ship_types = [100, 200]  # 每种船只的质量
        ship_counts = [np.random.randint(1, 5), np.random.randint(1, 5)]  # 每种船只的数量
        
        # 计算碰撞概率
        collision_probability = calculate_collision_probability(d_sense_max, weather_factors, weather_probabilities, epsilon, t_react, v_ship, v_obj, d_init, N_samples, ship_shapes, obj_shapes, ship_types, ship_counts, bias_angle, time_interval)
        
        # 添加数据
        data.append([d_sense_max, epsilon, t_react, v_ship, v_obj, d_init, N_samples, bias_angle, time_interval, ship_types, ship_counts, collision_probability])
    
    return data

# 生成10,000条数据
num_samples = 1000
data = generate_data(num_samples)

# 转换为DataFrame
columns = ['d_sense_max', 'epsilon', 't_react', 'v_ship', 'v_obj', 'd_init', 'N_samples', 'bias_angle', 'time_interval', 'ship_types', 'ship_counts', 'collision_probability']
df = pd.DataFrame(data, columns=columns)

# 保存数据到CSV文件
df.to_csv('data/ship/collision_data.csv', index=False)

# 输出数据统计信息
print(df.describe())