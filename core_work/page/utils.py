import numpy as np

# 模拟时间步长
dt = 0.1  # 时间步长 (单位：s)

# 定义船体参数
length = 10  # 船体长度
width = 5    # 船体宽度
height = 3   # 船体高度

# 定义漏水点参数
leak_points = [(5, 2.5, 0)]  # 漏水点位置 (x, y, z)
leak_rate = 5.0  # 漏水速度 (单位：m^3/s)

# 定义水面高度阈值
water_threshold = 2.5  # 水面高度超过这个值时，人会被淹没

# 定义逃离速度
escape_speeds = [0.5, 1.0, 2.0]  # 逃离速度 (单位：m/s)

# 初始化水面高度
water_height = 0

# 初始化时间
time = 0

# 初始化逃离时间
escape_times = {speed: None for speed in escape_speeds}

# 初始化淹没时间
submerged_time = None


# 计算斜线段的斜率和长度
def calculate_slope_and_length(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    length = np.sqrt(dx**2 + dy**2 + dz**2)
    return (dx, dy, dz), length

# 计算投影到斜线上的速度
def calculate_projected_speed(speed, slope):
    res = speed / np.sqrt(slope[0]**2 + slope[1]**2 + slope[2]**2)
    if res < 0.2:
        res = 0.2
    elif res > 5:
        res = 5
    return res

# 计算斜线段上的时间
def calculate_time_on_segment(length, projected_speed):
    return length / projected_speed

# 计算斜线段上的点
def calculate_points_on_segment(p1, p2, speed):
    slope, length = calculate_slope_and_length(p1, p2)
    projected_speed = calculate_projected_speed(speed, slope)
    segment_time = calculate_time_on_segment(length, projected_speed)
    num_points = int(segment_time / dt)
    points = []
    for i in range(num_points + 1):
        t = i * dt
        x = p1[0] + slope[0] * t / segment_time
        y = p1[1] + slope[1] * t / segment_time
        z = p1[2] + slope[2] * t / segment_time
        points.append((x, y, z))
    return points

# 计算直线方程参数
def calculate_line_parameters(p1, p2, speed, start_time):
    slope, length = calculate_slope_and_length(p1, p2)
    projected_speed = calculate_projected_speed(speed, slope)
    segment_time = calculate_time_on_segment(length, projected_speed)
    
    t1 = start_time
    t2 = start_time + segment_time
    
    k1 = (p2[0] - p1[0]) / (t2 - t1)
    k2 = (p2[1] - p1[1]) / (t2 - t1)
    k3 = (p2[2] - p1[2]) / (t2 - t1)
    
    b1 = (p1[0] * t2 - p2[0] * t1) / (t2 - t1)
    b2 = (p1[1] * t2 - p2[1] * t1) / (t2 - t1)
    b3 = (p1[2] * t2 - p2[2] * t1) / (t2 - t1)
    
    return k1, k2, k3, b1, b2, b3, segment_time, t1, t2