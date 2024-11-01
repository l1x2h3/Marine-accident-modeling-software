import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import json
# 船只类*****************************************************************************************
class Ship:
    def __init__(self, x, y, vx, vy, shape, turn_rate):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.shape = shape
        self.turn_rate = turn_rate
    def get_vertices(self):
        return [(self.x + x, self.y + y) for x, y in self.shape]
# 船只类*****************************************************************************************

# 碰撞检测***************************************************************************************
def project(vertices, axis):
    projections = [np.dot(vertex, axis) for vertex in vertices]
    return min(projections), max(projections)
def detect_collision(ship1, ship2):
    vertices1 = ship1.get_vertices()
    vertices2 = ship2.get_vertices()

    for vertices in [vertices1, vertices2]:
        for i in range(len(vertices)):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % len(vertices)]
            edge = (p2[0] - p1[0], p2[1] - p1[1])
            axis = (-edge[1], edge[0])

            min1, max1 = project(vertices1, axis)
            min2, max2 = project(vertices2, axis)

            if max1 < min2 or max2 < min1:
                return False
    # TODO：算法错误，需要修改
    return True
# 碰撞检测***************************************************************************************

# 创建船*****************************************************************************************
def create_ship_shape(length, width):
        half_length = length / 2
        half_width = width / 2
        return [
            (-half_length, -half_width),
            (-half_length, half_width),
            (0, half_width + half_width / 2),
            (half_length, half_width),
            (half_length, -half_width),
            (0, -half_width - half_width / 2)
        ]
# 创建船*****************************************************************************************

def use_single_step():
    # 副标题*************************************************************************************
    st.title("Ship Collision Simulation")
    # 副标题*************************************************************************************

    # 侧边栏*************************************************************************************
    st.sidebar.header("Ship Parameters")
    ship1_x = st.sidebar.number_input("Ship 1 Initial X", value=0.0)
    ship1_y = st.sidebar.number_input("Ship 1 Initial Y", value=0.0)
    ship1_vx = st.sidebar.number_input("Ship 1 Velocity X", value=1.0)
    ship1_vy = st.sidebar.number_input("Ship 1 Velocity Y", value=0.0)
    ship1_length = st.sidebar.number_input("Ship 1 Length", value=4.0)
    ship1_width = st.sidebar.number_input("Ship 1 Width", value=2.0)
    ship2_x = st.sidebar.number_input("Ship 2 Initial X", value=10.0)
    ship2_y = st.sidebar.number_input("Ship 2 Initial Y", value=0.0)
    ship2_vx = st.sidebar.number_input("Ship 2 Velocity X", value=-1.0)
    ship2_vy = st.sidebar.number_input("Ship 2 Velocity Y", value=0.0)
    ship2_length = st.sidebar.number_input("Ship 2 Length", value=4.0)
    ship2_width = st.sidebar.number_input("Ship 2 Width", value=2.0)
    turn_distance = st.sidebar.number_input("Turn Distance", value=5.0)
    turn_direction = st.sidebar.selectbox("Turn Direction", ["left", "right"])
    ship1_shape = create_ship_shape(ship1_length, ship1_width)
    ship2_shape = create_ship_shape(ship2_length, ship2_width)
    # 侧边栏*************************************************************************************

    # 初始化*************************************************************************************
    if 'step' not in st.session_state:
        st.session_state.step = 0
    # 初始化*************************************************************************************

    # 四个按钮***********************************************************************************
    button_col1, button_col2, button_col3, button_col4 = st.columns(4)
    with button_col1:
        if st.button("Step", key="StepButton"):
            st.session_state.step += 1
    with button_col2:
        if st.button("Clear", key="ClearButton"):
            st.session_state.step = 0
    with button_col3:
        if st.button("Save", key="SaveButton"):
            st.info("没有办法")
    with button_col4:
        if st.button("Load", key="LoadButton"):
            st.info("没有办法")
    # 四个按钮***********************************************************************************

    # 创建船只对象*******************************************************************************
    ship1 = Ship(ship1_x+st.session_state.step*ship1_vx, 
                 ship1_y+st.session_state.step*ship1_vy, 
                 ship1_vx, ship1_vy, ship1_shape, 0.1)
    ship2 = Ship(ship2_x+st.session_state.step*ship2_vx, 
                 ship2_y+st.session_state.step*ship2_vy, 
                 ship2_vx, ship2_vy, ship2_shape, 0.1)
    # 创建船只对象*******************************************************************************

    # 绘制结果***********************************************************************************
    fig, ax = plt.subplots()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')
    ax.add_patch(Polygon(ship1.get_vertices(), fill=False, color='blue', label="Ship 1"))
    ax.add_patch(Polygon(ship2.get_vertices(), fill=False, color='red', label="Ship 2"))
    if detect_collision(ship1, ship2):
        ax.plot(ship1.get_vertices()[0][0], ship1.get_vertices()[0][1], 'ro', label="Collision")
        ax.plot(ship2.get_vertices()[0][0], ship2.get_vertices()[0][1], 'ro')
    ax.legend()
    st.pyplot(fig)
    if detect_collision(ship1, ship2):
        st.write("Collision detected!")
    else:
        st.write("No collision detected.")
    # 绘制结果***********************************************************************************