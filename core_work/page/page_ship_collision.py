import streamlit as st
import plotly.graph_objects as go
import numpy as np
# 模拟模型函数，返回事故发生的可能性及影响
def predict_accident_probability(weather, ship_type, speed):
    weather_impact = {'sunny': 0.1, 'cloudy': 0.2, 'rainy': 0.5, 'stormy': 0.8}
    ship_type_impact = {'cargo': 0.2, 'passenger': 0.3, 'fishing': 0.4, 'military': 0.1}
    speed_impact = speed / 50.0

    probability = weather_impact[weather] + ship_type_impact[ship_type] + speed_impact
    impact = probability * 10  # 假设影响是概率的10倍

    return probability, impact

# 模拟船只运动和碰撞
def simulate_ships(num_ships, weather, ship_type, speed):
    # 初始化船只位置和速度
    positions = np.random.rand(num_ships, 2) * 100
    velocities = np.random.rand(num_ships, 2) * speed

    # 模拟时间步长
    dt = 0.1
    num_steps = 50  # 调整为 50 步，每步 0.1 秒，总共 5 秒

    # 存储轨迹
    trajectories = [positions]

    for _ in range(num_steps):
        # 更新位置
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

    return np.array(trajectories)

def ship_collision_part():
    st.markdown(
        """
        <h3>航行条件分析与碰撞模拟</h3>
        """,
        unsafe_allow_html=True
    )
    # 输入参数
    st.sidebar.header("输入参数")
    weather = st.sidebar.selectbox("天气条件", ["sunny", "cloudy", "rainy", "stormy"])
    ship_type = st.sidebar.selectbox("船舶类型", ["cargo", "passenger", "fishing", "military"])
    speed = st.sidebar.slider("航行速度 (节)", min_value=0.0, max_value=50.0, step=0.1)
    num_ships = st.sidebar.slider("船只数量", min_value=2, max_value=30, step=1)

    # 分析按钮
    if st.sidebar.button("分析"):
        # 调用模型函数
        probability, impact = predict_accident_probability(weather, ship_type, speed)

        # 展示结果
        st.header("分析结果")
        st.write(f"事故发生的可能性: {probability:.2f}")
        st.write(f"事故影响: {impact:.2f}")

        # 模拟船只运动和碰撞
        trajectories = simulate_ships(num_ships, weather, ship_type, speed)

        # 绘制轨迹图
        fig = go.Figure()

        for i in range(num_ships):
            x_coords = trajectories[:, i, 0]
            y_coords = trajectories[:, i, 1]
            fig.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='lines+markers', name=f'Ship {i+1}'))

        fig.update_layout(title="船只轨迹与碰撞模拟", xaxis_title="X坐标", yaxis_title="Y坐标")
        st.plotly_chart(fig)