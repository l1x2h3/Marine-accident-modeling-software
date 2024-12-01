import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from mpl_toolkits.mplot3d import Axes3D
from page.utils import calculate_line_parameters,calculate_points_on_segment,dt
# constants
from page.utils import length,width,height,leak_points,leak_rate,water_height,water_threshold,escape_speeds,escape_times,submerged_time
import json
import pandas as pd

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
        # 这里可以变换水的流速--普通直线，指数，对数形式
        if time <= 40:
            leak_volume = leak_rate * dt
        elif time > 40 and time <=80:
            leak_volume = 2 * leak_rate * dt
        else:
            leak_volume = 0.5 * leak_rate * dt
        # 下面这个直接计算会崩了
        # leak_volume = leak_rate * np.exp(-time / 10) * dt
        # 后续如果有可能，则实现不同的漏水速度对最终结果的影响
        # 这个调试确实挺困难的，因为开始的参数设置的不好，会导致结果很难看
        # 或者增加对点的扩增
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
def visualize_results(water_heights, times, escape_times, submerged_time, escape_points):
    # 创建三列
    col1, col2, col3 = st.columns(3)

    # 绘制船体和水面的图表
    with col2:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # 绘制水面
        water_x = np.linspace(0, length, 10)
        water_y = np.linspace(0, width, 10)
        water_X, water_Y = np.meshgrid(water_x, water_y)
        water_Z = np.full_like(water_X, water_heights[-1])
        ax.plot_surface(water_X, water_Y, water_Z, color='blue', alpha=0.5, label='water face')

        # 绘制逃离路径
        for speed, escape_time in escape_times.items():
            if escape_time is not None:
                points = []
                for i in range(len(escape_points) - 1):
                    segment_points = calculate_points_on_segment(escape_points[i], escape_points[i + 1], speed)
                    points.extend(segment_points)
                points = np.array(points)
                ax.plot(points[:, 0], points[:, 1], points[:, 2], label=f'escape speed: {speed} m/s')

        # 标出关键点
        for i, point in enumerate(escape_points):
            ax.scatter(point[0], point[1], point[2], color='red', s=100, label=f'Point {i+1}')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))

        st.pyplot(fig)

    col1, col2, col3 = st.columns(3)
    # 绘制水面高度随时间变化
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(times, water_heights, label='Water Height')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Height (m)')
        ax.legend()
        st.pyplot(fig)

    # 绘制三种速度下人上升的高度z随时间变化
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        for speed, escape_time in escape_times.items():
            if escape_time is not None:
                cumulative_time = 0
                print("len(escape_points) = ", len(escape_points))
                # print(len(escape_points))
                for i in range(len(escape_points) - 1):
                    k1, k2, k3, b1, b2, b3, segment_time, t1, t2 = calculate_line_parameters(escape_points[i], escape_points[i + 1], speed, cumulative_time)
                    t_array = np.linspace(t1, t2, 100)
                    z_array = k3 * t_array + b3
                    ax.plot(t_array, z_array, label=f'Escape Speed: {speed} m/s')
                    cumulative_time += segment_time
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Height (m)')
        ax.legend()
        st.pyplot(fig)

    # 绘制三种速度下人距离水面的高度
    with col3:
        fig, ax = plt.subplots(figsize=(10, 6))
        for speed, escape_time in escape_times.items():
            if escape_time is not None:
                cumulative_time = 0
                for i in range(len(escape_points) - 1):
                    k1, k2, k3, b1, b2, b3, segment_time, t1, t2 = calculate_line_parameters(escape_points[i], escape_points[i + 1], speed, cumulative_time)
                    t_array = np.linspace(t1, t2, 100)
                    z_array = k3 * t_array + b3
                    water_height_at_escape = np.interp(t_array, times, water_heights) 
                    # print("water_height_at_escape:",water_height_at_escape)
                    distance_to_water = z_array - water_height_at_escape
                    print("z_array",z_array, "water_height_at_escape", water_height_at_escape)
                    ax.plot(t_array, distance_to_water, label=f'Escape Speed: {speed} m/s')
                    cumulative_time += segment_time
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Distance to Water (m)')
        ax.legend()
        st.pyplot(fig)

# Streamlit前端界面
def main_box_leaking():
    st.title("船体漏水模型可视化")

    st.write("### 船体参数")
    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.slider("船体长度 (m)", 1.0, 20.0, 10.0)
    with col2:
        width = st.slider("船体宽度 (m)", 1.0, 10.0, 5.0)
    with col3:
        height = st.slider("船体高度 (m)", 1.0, 5.0, 3.0)

    st.write("### 漏水点参数")
    col1, col2, col3 = st.columns(3)
    with col1:
        leak_rate = st.slider("漏水速度 (m^3/s)", 0.01, 10.0, 5.0)

    st.write("### 逃离速度")
    col1, col2, col3 = st.columns(3)

    escape_speeds = []
    with col1:
        escape_speeds.append(st.slider(f"逃离速度 1 (m/s)", 0.1, 5.0, 0.5))
    with col2:
        escape_speeds.append(st.slider(f"逃离速度 2 (m/s)", 0.1, 5.0, 1.0))
    with col3:
        escape_speeds.append(st.slider(f"逃离速度 3 (m/s)", 0.1, 5.0, 2.0))
    
    st.write("### 逃离路径关键点")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        point1_x = st.number_input("Point 1 X", value=0.0, min_value=0.0, max_value=float(length))
        point1_y = st.number_input("Point 1 Y", value=0.0, min_value=0.0, max_value=float(width))
        point1_z = st.number_input("Point 1 Z", value=0.0, min_value=0.0, max_value=float(height))
    with col2:
        point2_x = st.number_input("Point 2 X", value=length / 3, min_value=0.0, max_value=float(length))
        point2_y = st.number_input("Point 2 Y", value=width / 3, min_value=0.0, max_value=float(width))
        point2_z = st.number_input("Point 2 Z", value=height / 3, min_value=0.0, max_value=float(height))
    with col3:
        point3_x = st.number_input("Point 3 X", value=length / 2, min_value=0.0, max_value=float(length))
        point3_y = st.number_input("Point 3 Y", value=width / 2, min_value=0.0, max_value=float(width))
        point3_z = st.number_input("Point 3 Z", value=height / 2, min_value=0.0, max_value=float(height))
    with col4:
        point4_x = st.number_input("Point 4 X", value=3 * length / 4, min_value=0.0, max_value=float(length))
        point4_y = st.number_input("Point 4 Y", value=width / 2, min_value=0.0, max_value=float(width))
        point4_z = st.number_input("Point 4 Z", value=height, min_value=0.0, max_value=float(height))

    escape_points = [(point1_x, point1_y, point1_z), (point2_x, point2_y, point2_z), (point3_x, point3_y, point3_z), (point4_x, point4_y, point4_z)]

    
    
    # 添加一个按钮用于添加新的点
    if st.button("添加新的点"):
        with st.form(key="add_point_form"):
            new_point_x = st.number_input("新点 X", value=0.0, min_value=0.0, max_value=float(length))
            new_point_y = st.number_input("新点 Y", value=0.0, min_value=0.0, max_value=float(width))
            new_point_z = st.number_input("新点 Z", value=0.0, min_value=0.0, max_value=float(height))
            submitted = st.form_submit_button("确认添加")
            if submitted:
                escape_points.append((new_point_x, new_point_y, new_point_z))
                st.write("当前所有点的坐标信息:")
                for i, point in enumerate(escape_points):
                    st.write(f"Point {i + 1}: X={point[0]}, Y={point[1]}, Z={point[2]}")

    # 设计一个导出参数信息的按钮
    if st.button("导出参数信息"):
        params = {
            "length": length,
            "width": width,
            "height": height,
            "leak_rate": leak_rate,
            "water_threshold": water_threshold,
            "escape_speeds": escape_speeds,
            "escape_points": escape_points
        }
        json_params = json.dumps(params, indent=4)
        st.download_button(label="下载参数信息", data=json_params, file_name="params.json", mime="application/json")

    if st.button("更新模拟"):
        st.write("### 模拟结果")
        water_heights, times, escape_times, submerged_time = simulate_leak(length, width, height, leak_points, leak_rate, water_threshold, escape_speeds, dt)
        visualize_results(water_heights, times, escape_times, submerged_time, escape_points)

        '''
        for speed, escape_time in escape_times.items():
            st.write(f"逃离速度 {speed} m/s 的逃离时间: {escape_time:.2f} s")
        '''

        data = {
            '逃离速度 (m/s)': list(escape_times.keys()),
            '逃离时间 (s)': [f"{value:.2f}" for value in escape_times.values()]
        }
        st.markdown(
        """
        <style>
            .col_heading {
                color: red;
                text-align: left;
            }
        </style>
        """,
        unsafe_allow_html=True,
        )
        df = pd.DataFrame(data)
        st.table(df)
        st.write(f"淹没时间: {submerged_time:.2f} s")

if __name__ == "__main__":
    main_box_leaking()