import streamlit as st
import numpy as np
import plotly.graph_objects as go
from PIL import Image
import pandas as pd

coast_image = Image.open("fig/coast.png")
island_image = Image.open("fig/island1.png")
ship_image = Image.open("fig/ship.png")

# 缩放海岸线图片
coast_image = coast_image.resize((100, 100))

# 模拟地图
def simulate_map(num_ships, weather, ship_type, speed):
    # 初始化地图
    map_size = 100
    map_data = np.zeros((map_size, map_size))

    # 生成岛礁
    num_islands = 5
    islands = []
    for _ in range(num_islands):
        x, y = np.random.randint(10, 90, 2)
        islands.append((x, y))

    # 初始化船只位置和速度
    positions = np.random.rand(num_ships, 2) * 80 + 10
    velocities = np.random.rand(num_ships, 2) * speed

    # 设置目的地
    destinations = np.random.rand(num_ships, 2) * 80 + 10

    # 模拟时间步长
    dt = 0.1
    num_steps = 50  # 调整为 50 步，每步 0.1 秒，总共 5 秒

    # 存储轨迹
    trajectories = [positions]

    # 存储出发时间和到达时间
    start_times = np.zeros(num_ships)
    end_times = np.zeros(num_ships)

    for step in range(num_steps):
        # 更新位置
        for i in range(num_ships):
            if step == 0:
                start_times[i] = step * dt

            # 计算到目的地的方向
            direction = destinations[i] - positions[i]
            direction /= np.linalg.norm(direction)
            velocities[i] = direction * speed

            # 绕开障碍物
            for island in islands:
                obstacle_pos = np.array(island)
                dist = np.linalg.norm(positions[i] - obstacle_pos)
                if dist < 10:  # 假设障碍物距离为10
                    # 绕开障碍物
                    velocities[i] += (positions[i] - obstacle_pos) / dist

        positions += velocities * dt

        # 简单的碰撞检测和处理
        for i in range(num_ships):
            for j in range(i + 1, num_ships):
                dist = np.linalg.norm(positions[i] - positions[j])
                if dist < 10:  # 假设碰撞距离为10
                    # 简单的反弹处理
                    velocities[i] = -velocities[i]
                    velocities[j] = -velocities[j]

        # 存储轨迹
        trajectories.append(positions.copy())

        # 更新到达时间
        for i in range(num_ships):
            if np.linalg.norm(positions[i] - destinations[i]) < 1:
                end_times[i] = step * dt

    return map_data, np.array(trajectories), destinations, start_times, end_times, islands

def map_simu_part():
    st.markdown(
        """
        <h3>地图模拟</h3>
        """,
        unsafe_allow_html=True
    )

    # 输入参数
    st.sidebar.header("输入参数")
    weather = st.sidebar.selectbox("天气条件", ["sunny", "cloudy", "rainy", "stormy"])
    ship_type = st.sidebar.selectbox("船舶类型", ["cargo", "passenger", "fishing", "military"])
    speed = st.sidebar.slider("航行速度 (节)", min_value=0.0, max_value=50.0, step=0.1)
    num_ships = st.sidebar.slider("船只数量", min_value=2, max_value=20, step=1)
    # 设置过大可能会卡

    # 模拟按钮
    if st.sidebar.button("模拟"):
        # 模拟地图和船只运动
        map_data, trajectories, destinations, start_times, end_times, islands = simulate_map(num_ships, weather, ship_type, speed)

        # 绘制动态图
        fig = go.Figure()

        # 添加海岸线
        fig.add_layout_image(
            dict(
                source=coast_image,
                xref="x",
                yref="y",
                x=0,
                y=0,
                sizex=100,
                sizey=100,
                xanchor="left",
                yanchor="bottom",
                sizing="stretch",
                opacity=1,
                layer="below"
            )
        )

        # 添加岛礁
        for island in islands:
            fig.add_layout_image(
                dict(
                    source=island_image,
                    xref="x",
                    yref="y",
                    x=island[0],
                    y=island[1],
                    sizex=1,
                    sizey=1,
                    xanchor="center",
                    yanchor="middle",
                    sizing="stretch",
                    opacity=1,
                    layer="below"
                )
            )

        # 添加船只轨迹
        for i in range(trajectories.shape[1]):
            x_coords = trajectories[:, i, 0]
            y_coords = trajectories[:, i, 1]
            fig.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='lines+markers', name=f'Ship {i+1}', marker=dict(size=5)))

        # 添加目的地
        for i in range(destinations.shape[0]):
            fig.add_trace(go.Scatter(x=[destinations[i, 0]], y=[destinations[i, 1]], mode='markers', name=f'Destination {i+1}', marker=dict(size=10, color='red')))

        fig.update_layout(title="地图与船只航行模拟", xaxis_title="X坐标", yaxis_title="Y坐标", xaxis=dict(range=[0, 100]), yaxis=dict(range=[0, 100]))

        # 生成动态图
        frames = []
        for step in range(trajectories.shape[0]):
            frame = go.Frame(
                data=[
                    go.Scatter(
                        x=trajectories[step, :, 0],
                        y=trajectories[step, :, 1],
                        mode='markers',
                        marker=dict(size=10, color='blue')
                    )
                ]
            )
            frames.append(frame)

        fig.frames = frames

        # 添加动画控制
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}]
                        ),
                        dict(
                            label="Pause",
                            method="animate",
                            args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]
                        )
                    ]
                )
            ]
        )

        st.plotly_chart(fig)

        # 添加标注信息
        st.write("标注信息：")
        cols = st.columns(5)  # 创建5列
        cols[0].write("- 黑色区域：海岸线")
        cols[1].write("- 灰色区域：岛礁")
        cols[2].write("- 浅灰色区域：浅水区")
        cols[3].write("- 蓝色线条：船只轨迹")
        cols[4].write("- 红色点：船只目的地")

        # 显示出发时间和到达时间
        st.write("船只出发时间和到达时间：")
        cols1 = st.columns(num_ships)
        for i in range(num_ships):
            cols1[i].write(f"船只 {i+1}: 出发时间 {start_times[i]:.2f} 秒, 到达时间 {end_times[i]:.2f} 秒")
            # st.write(f"船只 {i+1}: 出发时间 {start_times[i]:.2f} 秒, 到达时间 {end_times[i]:.2f} 秒")

        # 显示出发点和目的地的坐标
        st.write("出发点和目的地的坐标：")
        data = {
            "船只编号": [f"船只 {i+1}" for i in range(num_ships)],
            "出发点 X坐标": [trajectories[0, i, 0] for i in range(num_ships)],
            "出发点 Y坐标": [trajectories[0, i, 1] for i in range(num_ships)],
            "目的地 X坐标": [destinations[i, 0] for i in range(num_ships)],
            "目的地 Y坐标": [destinations[i, 1] for i in range(num_ships)]
        }
        df = pd.DataFrame(data)
        st.table(df)