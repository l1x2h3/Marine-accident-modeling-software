import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# 定义船体参数
length = 30  # 船体长度
width = 20    # 船体宽度
height = 15   # 船体高度

# 定义漏水点参数
leak_points = [(5, 2.5, 0)]  # 漏水点位置 (x, y, z)
leak_rate = 0.1  # 漏水速度 (单位：m^3/s)

# 定义水面高度阈值
water_threshold = 2.5  # 水面高度超过这个值时，人会被淹没

# 定义逃离速度
escape_speeds = [0.5, 1.0, 2.0]  # 逃离速度 (单位：m/s)

# 模拟时间步长
dt = 0.1  # 时间步长 (单位：s)

# 初始化水面高度
water_height = 0

# 初始化时间
time = 0

# 初始化逃离时间
escape_times = {speed: None for speed in escape_speeds}

# 初始化淹没时间
submerged_time = None

# 模拟漏水过程
def simulate_leak(length, width, height, leak_points, leak_rate, water_threshold, escape_speeds, dt):
    water_height = 0
    time = 0
    escape_times = {speed: None for speed in escape_speeds}
    submerged_time = None

    water_volume = 0
    water_heights = []
    times = []

    while water_height < height:
        # 计算漏水量
        leak_volume = leak_rate * dt
        water_volume += leak_volume

        # 计算水面高度
        water_height = water_volume / (length * width)

        # 记录时间
        time += dt

        # 记录水面高度和时间
        water_heights.append(water_height)
        times.append(time)

        # 检查是否达到淹没阈值
        if water_height >= water_threshold and submerged_time is None:
            submerged_time = time

        # 检查逃离时间
        for speed in escape_speeds:
            if escape_times[speed] is None and water_height >= height - speed * time:
                escape_times[speed] = time

    return water_heights, times, escape_times, submerged_time

# 可视化结果
def visualize_results(water_heights, times, escape_times, submerged_time, stair_segments, stair_height):
    # 创建三列
    col1, col2, col3 = st.columns(3)

    # 绘制水面上升随时间的关系
    with col1:
        fig, ax = plt.subplots()
        ax.plot(times, water_heights, label='Water Height')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Water Height (m)')
        ax.legend()
        st.pyplot(fig)

    # 绘制人逃跑的高度随时间上升的关系
    with col2:
        fig, ax = plt.subplots()
        for speed, escape_time in escape_times.items():
            if escape_time is not None:
                escape_heights = []
                for t in times:
                    if t <= escape_time:
                        escape_heights.append(min(height, speed * t))
                    else:
                        escape_heights.append(height)
                ax.plot(times, escape_heights, label=f'Escape Speed: {speed} m/s')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Escape Height (m)')
        ax.legend()
        st.pyplot(fig)

    # 绘制人与水面的距离随时间的关系
    with col3:
        fig, ax = plt.subplots()
        for speed, escape_time in escape_times.items():
            if escape_time is not None:
                distance = []
                for t in times:
                    if t <= escape_time:
                        distance.append(min(height, speed * t) - water_heights[int(t / dt)])
                    else:
                        distance.append(height - water_heights[int(t / dt)])
                ax.plot(times, distance, label=f'Escape Speed: {speed} m/s')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Distance (m)')
        ax.legend()
        st.pyplot(fig)

    # 绘制三维动图
    with col2:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # 绘制楼梯
        stair_x = np.linspace(0, length, stair_segments + 1)
        stair_y = np.linspace(0, width, stair_segments + 1)
        stair_z = np.linspace(0, height, stair_segments + 1)

        for i in range(stair_segments):
            ax.plot([stair_x[i], stair_x[i+1]], [stair_y[i], stair_y[i]], [stair_z[i], stair_z[i]], color='g', linewidth=2)
            ax.plot([stair_x[i+1], stair_x[i+1]], [stair_y[i], stair_y[i+1]], [stair_z[i], stair_z[i]], color='g', linewidth=2)
            ax.plot([stair_x[i+1], stair_x[i+1]], [stair_y[i+1], stair_y[i+1]], [stair_z[i], stair_z[i+1]], color='g', linewidth=2)

        # 绘制水面
        water_x = np.linspace(0, length, 10)
        water_y = np.linspace(0, width, 10)
        water_X, water_Y = np.meshgrid(water_x, water_y)
        water_Z = np.full_like(water_X, water_heights[-1])
        ax.plot_surface(water_X, water_Y, water_Z, color='blue', alpha=0.5)

        # 初始化人的位置
        people_positions = {speed: [0, 0, 0] for speed in escape_speeds}
        people_colors = ['r', 'g', 'b']

        # 更新函数
        def update(frame):
            # ax.clear()

            # 绘制楼梯
            for i in range(stair_segments):
                ax.plot([stair_x[i], stair_x[i+1]], [stair_y[i], stair_y[i]], [stair_z[i], stair_z[i]], color='g', linewidth=2)
                ax.plot([stair_x[i+1], stair_x[i+1]], [stair_y[i], stair_y[i+1]], [stair_z[i], stair_z[i]], color='g', linewidth=2)
                ax.plot([stair_x[i+1], stair_x[i+1]], [stair_y[i+1], stair_y[i+1]], [stair_z[i], stair_z[i+1]], color='g', linewidth=2)

            # 绘制水面
            ax.plot_surface(water_X, water_Y, water_Z, color='blue', alpha=0.5)

            # 更新人的位置
            for i, (speed, escape_time) in enumerate(escape_times.items()):
                if escape_time is not None:
                    if frame * dt <= escape_time:
                        people_positions[speed][2] = min(height, speed * frame * dt)
                    ax.scatter(people_positions[speed][0], people_positions[speed][1], people_positions[speed][2], color=people_colors[i], s=50, label=f'Escape Speed: {speed} m/s')

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title('漏水演示')
            ax.legend()

        # 创建动画
        st.pyplot(fig)
        if st.button("Run"):
            ani = FuncAnimation(fig, update, frames=len(times), interval=100)
            

# Streamlit前端界面
def main_box_leaking():
    st.markdown(
        """
        <h3>船体漏水模型可视化</h3>
        """,
        unsafe_allow_html=True
    )
    st.write("### 船体参数")
    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.slider("船体长度 (m)", 1, 40, 30)
    with col2:
        width = st.slider("船体宽度 (m)", 1, 30, 20)
    with col3:
        height = st.slider("船体高度 (m)", 1, 20, 15)

    st.write("### 漏水点参数")
    col1, col2, col3 = st.columns(3)
    with col1:
        leak_rate = st.slider("漏水速度 (m^3/s)", 0.01, 1.0, 0.1)

    st.write("### 逃离速度")
    col1, col2, col3 = st.columns(3)

    escape_speeds = []
    with col1:
        escape_speeds.append(st.slider(f"逃离速度 1 (m/s)", 0.1, 5.0, 0.5))
    with col2:
        escape_speeds.append(st.slider(f"逃离速度 2 (m/s)", 0.1, 5.0, 1.0))
    with col3:
        escape_speeds.append(st.slider(f"逃离速度 3 (m/s)", 0.1, 5.0, 2.0))

    st.write("### 楼梯参数")
    col1, col2 = st.columns(2)
    with col1:
        stair_segments = st.slider("楼梯段数", 4, 8, 4)
    with col2:
        stair_height = st.slider("每段楼梯高度 (m)", 0.1, 1.0, 0.5)

    if st.button("更新模拟"):
        st.write("### 模拟结果")
        water_heights, times, escape_times, submerged_time = simulate_leak(length, width, height, leak_points, leak_rate, water_threshold, escape_speeds, dt)
        visualize_results(water_heights, times, escape_times, submerged_time, stair_segments, stair_height)

        st.write(f"淹没时间: {submerged_time:.2f} s")
        for speed, escape_time in escape_times.items():
            st.write(f"逃离速度 {speed} m/s 的逃离时间: {escape_time:.2f} s")

if __name__ == "__main__":
    main_box_leaking()

# 这算法出了大问题，同时图片也不对，整个逻辑需要修改