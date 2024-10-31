import numpy as np
from scipy.optimize import minimize

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

def rotate_polygon(polygon, angle):
    """旋转多边形"""
    angle_rad = np.radians(angle)
    cos_angle = np.cos(angle_rad)
    sin_angle = np.sin(angle_rad)
    
    rotated_polygon = []
    for x, y in polygon:
        new_x = x * cos_angle - y * sin_angle
        new_y = x * sin_angle + y * cos_angle
        rotated_polygon.append([new_x, new_y])
    
    return np.array(rotated_polygon)

def calculate_collision_probability(d_sense_max, weather_factors, weather_probabilities, epsilon, t_react, v_ship, v_obj, d_init, N_samples, ship_shapes, obj_shapes, ship_types, ship_counts, bias_angle, time_interval):
    # 随机选择天气类型
    weather_type = np.random.choice(list(weather_factors.keys()), p=list(weather_probabilities.values()))
    
    # 获取天气类型的感知距离因子
    f_weather = weather_factors[weather_type]
    
    # 计算感知距离
    d_sense = d_sense_max * f_weather
    
    # 计算碰撞距离
    d_collision = d_init - (v_ship + v_obj) * t_react
    

    # 计算总质量
    total_mass = sum([ship_types[i] * ship_counts[i] for i in range(len(ship_types))])
    
    # 计算每次调整的角度
    angle_adjustment = time_interval / total_mass
    
    # 计算调整后的角度
    adjusted_angle = bias_angle - angle_adjustment
    
    # 旋转船只和动态物体的形状
    rotated_ship_shapes = [rotate_polygon(shape, adjusted_angle) for shape in ship_shapes]
    rotated_obj_shapes = [rotate_polygon(shape, adjusted_angle) for shape in obj_shapes]
    
    # 定义抛物线方程
    def parabola(t, v, d_init):
        return v * t + 0.5 * 9.8 * t**2 + d_init
    
    # 计算船只和动态物体的抛物线方程
    ship_parabola = lambda t: parabola(t, v_ship, d_init)
    obj_parabola = lambda t: parabola(t, v_obj, d_init)
    
    # 计算最短距离
    def distance(t):
        return np.abs(ship_parabola(t) - obj_parabola(t))
    
    # 使用优化算法求解最短距离
    result = minimize(distance, 0)
    min_distance = result.fun
    
    # 判断是否会发生碰撞
    if min_distance <= d_sense + epsilon:
            # 随机采样点
            samples = np.random.uniform(low=[0, 0], high=[100, 20], size=(N_samples, 2))
            
            # 判断采样点是否在动态物体的俯视图范围内
            overlap_count = 0
            for sample in samples:
                for obj_shape in rotated_obj_shapes:
                    if point_in_polygon(sample, obj_shape):
                        overlap_count += 1
                        break
            
            # 计算基础碰撞概率
            base_collision_probability = overlap_count / N_samples
            
            # 根据偏向角度调整碰撞概率
            adjusted_collision_probability = base_collision_probability * (1 - adjusted_angle / 90)
            
            return adjusted_collision_probability
    else:
        return 0.0


# 示例参数
d_sense_max = 1000  # 最大感知距离（米）
epsilon = 50        # 航线规划误差（米）
t_react = 10        # 注意力反应时间（秒）
v_ship = 10         # 船只速度（米/秒）
v_obj = 5           # 动态物体速度（米/秒）
d_init = 2000       # 初始距离（米）
N_samples = 1000    # 采样次数
bias_angle = 0     # 偏向角（°）
time_interval = 5   # 时间间隔（秒）

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
ship_counts = [2, 3]     # 每种船只的数量

# 计算碰撞概率
collision_probability = calculate_collision_probability(d_sense_max, weather_factors, weather_probabilities, epsilon, t_react, v_ship, v_obj, d_init, N_samples, ship_shapes, obj_shapes, ship_types, ship_counts, bias_angle, time_interval)

# 输出结果
if collision_probability > 0:
    print(f"船只会发生碰撞，碰撞概率(区域面积)为 {collision_probability:.2f}。")
else:
    print("船只不会发生碰撞。")