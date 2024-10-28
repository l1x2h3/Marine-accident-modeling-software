import numpy as np

# 天气类型及其感知距离因子
weather_factors = {
    '晴朗': 1.0,
    '多云': 0.9,
    '阴天': 0.8,
    '轻雾': 0.7,
    '中雾': 0.5,
    '浓雾': 0.3,
    '小雨': 0.8,
    '中雨': 0.6,
    '大雨': 0.4,
    '暴风雨': 0.2
}

# 天气类型及其概率
weather_probabilities = {
    '晴朗': 0.2,
    '多云': 0.2,
    '阴天': 0.1,
    '轻雾': 0.1,
    '中雾': 0.1,
    '浓雾': 0.1,
    '小雨': 0.1,
    '中雨': 0.05,
    '大雨': 0.03,
    '暴风雨': 0.02
}

def point_in_polygon(point, polygon):
    """判断点是否在多边形内"""
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def calculate_collision_probability(d_sense_max, weather_factors, weather_probabilities, epsilon, t_react, v_ship, v_obj, d_init, N_samples, ship_shape, obj_shape):
    # 随机选择天气类型
    weather_type = np.random.choice(list(weather_factors.keys()), p=list(weather_probabilities.values()))
    
    # 获取天气类型的感知距离因子
    f_weather = weather_factors[weather_type]
    
    # 计算感知距离
    d_sense = d_sense_max * f_weather
    
    # 计算碰撞距离
    d_collision = d_init - (v_ship + v_obj) * t_react
    
    # 判断是否会发生碰撞
    if d_collision <= d_sense + epsilon:
        # 随机采样点
        samples = np.random.uniform(low=[0, 0], high=[100, 20], size=(N_samples, 2))
        
        # 判断采样点是否在动态物体的俯视图范围内
        collision = False
        for sample in samples:
            if point_in_polygon(sample, obj_shape):
                collision = True
                break
        
        return collision
    else:
        return False

# 示例参数
d_sense_max = 1000  # 最大感知距离（米）
epsilon = 50        # 航线规划误差（米）
t_react = 10        # 注意力反应时间（秒）
v_ship = 10         # 船只速度（米/秒）
v_obj = 5           # 动态物体速度（米/秒）
d_init = 2000       # 初始距离（米）
N_samples = 1000    # 采样次数

# 定义船只和动态物体的俯视图形状
ship_shape = np.array([[0, 0], [100, 0], [100, 20], [50, 40], [0, 20]])  # 五边形
obj_shape = np.array([[50, 0], [150, 0], [150, 20], [100, 40], [50, 20]])  # 五边形

# 计算碰撞概率
collision_probability = calculate_collision_probability(d_sense_max, weather_factors, weather_probabilities, epsilon, t_react, v_ship, v_obj, d_init, N_samples, ship_shape, obj_shape)

# 输出结果
if collision_probability:
    print("船只可能会发生碰撞。")
else:
    print("船只不会发生碰撞。")