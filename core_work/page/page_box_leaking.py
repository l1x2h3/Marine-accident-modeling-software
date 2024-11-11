import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import base64
import tempfile


def main_box_leaking():
    # 初始化参数
    # st.title("Leak Escape Simulation")
    # st.sidebar.header("Parameter Settings")

    # 输入参数
    stair_length = st.sidebar.number_input("Stair Length (m)", value=5.0, step=0.1)
    stair_count = st.sidebar.number_input("Number of Stairs", value=10, step=1)
    flat_length = st.sidebar.number_input("Flat Length Between Stairs (m)", value=2.0, step=0.1)
    escape_speed = st.sidebar.number_input("Escape Speed (m/s)", value=2.0, step=0.1)
    water_rise_speed = st.sidebar.number_input("Water Rise Speed (m/s)", value=0.1, step=0.01)

    # 确认模拟按钮
    if st.sidebar.button("Confirm Simulation"):
        # 计算总路径长度
        total_path_length = stair_count * stair_length + (stair_count - 1) * flat_length

        # 计算总时间
        total_time = total_path_length / escape_speed

        # 初始化图形
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(0, total_path_length + 1)
        ax.set_ylim(0, stair_count * stair_length + 1)
        ax.set_zlim(0, total_time + 1)
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("Height (m)")
        ax.set_zlabel("Time (s)")
        ax.set_title("Leak Escape Simulation")

        # 初始化水面和人位置
        water_line, = ax.plot([], [], [], 'b-', label="Water Level")
        person_dot, = ax.plot([], [], [], 'ro', label="Person")

        # 初始化数据
        xdata, ydata, zdata = [], [], []
        water_height = 0
        person_position = 0
        person_height = 0
        time_elapsed = 0

        # 动画更新函数
        def update(frame):
            global water_height, person_position, person_height, time_elapsed

            # 更新水面高度
            water_height += water_rise_speed * frame
            xdata.append(0)
            ydata.append(water_height)
            zdata.append(time_elapsed)
            water_line.set_data(xdata, ydata)
            water_line.set_3d_properties(zdata)

            # 更新人位置
            if person_position < total_path_length:
                person_position += escape_speed * frame
                time_elapsed += frame
                if person_position <= stair_length:
                    person_height = person_position
                elif person_position <= stair_length + flat_length:
                    person_height = stair_length
                else:
                    person_height = stair_length - (person_position - stair_length - flat_length)

                person_dot.set_data([person_position], [person_height])
                person_dot.set_3d_properties([time_elapsed])

            return water_line, person_dot

        # 创建动画
        ani = FuncAnimation(fig, update, frames=np.arange(0, total_time, 0.1), repeat=False)

        # 保存动画为临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.gif') as tmp_file:
            ani.save(tmp_file.name, writer='pillow')
            with open(tmp_file.name, "rb") as f:
                base64_gif = base64.b64encode(f.read()).decode('ascii')
                st.image(f"data:image/gif;base64,{base64_gif}", use_column_width=True)

        # 绘制水面高度随时间的变化曲线
        fig2, ax2 = plt.subplots()
        water_heights = np.arange(0, total_time, 0.1) * water_rise_speed
        ax2.plot(np.arange(0, total_time, 0.1), water_heights)
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Water Height (m)")
        ax2.set_title("Water Height Over Time")

        # 绘制人的高度随时间的变化曲线
        fig3, ax3 = plt.subplots()
        person_heights = []
        time_points = []
        current_time = 0
        for i in range(stair_count):
            person_heights.extend([i * stair_length] * int(flat_length / escape_speed / 0.1))
            time_points.extend(np.arange(current_time, current_time + flat_length / escape_speed, 0.1))
            current_time += flat_length / escape_speed
            person_heights.extend(np.arange(i * stair_length, (i + 1) * stair_length, 0.1 * escape_speed))
            time_points.extend(np.arange(current_time, current_time + stair_length / escape_speed, 0.1))
            current_time += stair_length / escape_speed
        ax3.step(time_points, person_heights, where='post')
        ax3.set_xlabel("Time (s)")
        ax3.set_ylabel("Person Height (m)")
        ax3.set_title("Person Height Over Time")

        # 绘制人与水面高度差随时间的变化曲线
        fig4, ax4 = plt.subplots()
        # 确保 person_heights 和 water_heights 的长度一致
        min_length = min(len(person_heights), len(water_heights))
        height_diff = np.array(person_heights[:min_length]) - water_heights[:min_length]
        ax4.plot(time_points[:min_length], height_diff)
        ax4.set_xlabel("Time (s)")
        ax4.set_ylabel("Height Difference (m)")
        ax4.set_title("Height Difference Between Person and Water Over Time")

        # 并列显示三张图
        col1, col2, col3 = st.columns(3)
        with col1:
            st.pyplot(fig2)
        with col2:
            st.pyplot(fig3)
        with col3:
            st.pyplot(fig4)


if __name__ == "__main__":
    main_box_leaking()
