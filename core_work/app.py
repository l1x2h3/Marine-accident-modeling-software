import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from streamlit_authenticator import Authenticate
from database.db_config import db_config
from page.page_box_leaking import main_box_leaking
from page.page_single_step import use_single_step
from page.page_doc import page_doc_part
from page.page_ship_collision import ship_collision_part
from page.page_map_simulation import map_simu_part
from database.log_reg import register_user, check_user
from page.page_enter import page_enter_part
from data.ship.predict import predict_collision_probability
from page.page_deepseek_api import use_api_part
import os

# 加载图片
coast_image = Image.open("../fig/coast.png")
island_image = Image.open("../fig/island1.png")
ship_image = Image.open("../fig/ship.png")

# 缩放海岸线图片
coast_image = coast_image.resize((100, 100))

# Streamlit应用
st.set_page_config(layout="wide", page_title="航行模拟器", page_icon="fig/logo.png")

# 添加网站名称和Logo
st.markdown(
        """
        <h1 style="text-align: center;">航行模拟器</h1>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <style>
    .stApp {
        background-color: white; /* 自定义背景颜色 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 自定义CSS样式
st.markdown(
    """
    <style>
        .stHeading > div > h1 {
            font-size: 45px;
        }
        .stRadio > label > div > p {
            font-size: 18px;
        }
        .stRadio > div > label > div:nth-of-type(2) > div > p {
            font-size: 22px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 导航栏
st.sidebar.title("导航栏")
page = st.sidebar.radio("选择页面", ["主页","注册", "登录", "航行条件分析与碰撞模拟", "地图模拟","漏水检测" , "单步模拟","文档页面"])


if page == "主页":
    page_enter_part()

elif page == "注册":
    st.markdown(
        """
        <h3>用户注册</h3>
        """,
        unsafe_allow_html=True
    )

    st.write("")  # 右侧空白列
    # 创建三列，中间一列放置图片
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.write("")  # 右侧空白列
    with col2: 
        current_directory = os.getcwd()
        relative_path1 = os.path.join(current_directory, '..', 'fig', 'logo.png')
        st.image(relative_path1, caption=" ", use_column_width=True)
    with col3:
        st.write("")  # 右侧空白列
    st.write("")  # 右侧空白列

    # 注册表单
    email = st.text_input("QQ邮箱")
    password = st.text_input("密码", type="password")
    confirm_password = st.text_input("确认密码", type="password")

    if st.button("注册"):
        if password == confirm_password:
            try:
                register_user(email, password)
                st.success("注册成功！请登录")
            except mysql.connector.Error as err:
                st.error(f"注册失败: {err}")
        else:
            st.error("密码不匹配")

elif page == "登录":
    st.markdown(
        """
        <h3>用户登录</h3>
        """,
        unsafe_allow_html=True
    )

    st.write("")  # 右侧空白列
    # 创建三列，中间一列放置图片
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.write("")  # 右侧空白列
    with col2:
        current_directory = os.getcwd()
        relative_path2 = os.path.join(current_directory, '..', 'fig', 'logo.png')
        st.image(relative_path2, caption=" ", use_column_width=True)
    with col3:
        st.write("")  # 右侧空白列
    st.write("")  # 右侧空白列

    # 登录表单
    email = st.text_input("QQ邮箱")
    password = st.text_input("密码", type="password")

    if st.button("登录"):
        if check_user(email, password):
            st.success("登录成功！")
            st.session_state['logged_in'] = True
        else:
            st.error("登录失败，请检查邮箱和密码")

st.session_state['logged_in'] = True
if 'logged_in' in st.session_state and st.session_state['logged_in']:
    if page == "航行条件分析与碰撞模拟":
        ship_collision_part()

        # 智能分析模块
        # 定义输入参数的列名
        input_columns = ['d_sense_max', 'epsilon', 't_react', 'v_ship', 'v_obj', 'd_init', 'N_samples', 'bias_angle', 'time_interval']

        # 输入框
        params = {}

        # 创建三列
        col1, col2, col3 = st.columns(3)

        # 每行三个输入框，总共三行
        with col1:
            params['d_sense_max'] = st.number_input("最大感知距离:", value=100.0, step=0.1, format="%.2f")
            params['v_ship'] = st.number_input("船体速度:", value=15.0, step=0.1, format="%.2f")
            params['N_samples'] = st.number_input("样本数量:", value=1000.0, step=0.1, format="%.2f")

        with col2:
            params['epsilon'] = st.number_input("感知误差限:", value=50.0, step=0.1, format="%.2f")
            params['v_obj'] = st.number_input("对方物体速度:", value=15.0, step=0.1, format="%.2f")
            params['bias_angle'] = st.number_input("船只偏向角（0°径直碰撞）:", value=0.0, step=0.1, format="%.2f")

        with col3:
            params['t_react'] = st.number_input("人体反映时间:", value=2.0, step=0.1, format="%.2f")
            params['d_init'] = st.number_input("距离初始值:", value=300.0, step=0.1, format="%.2f")
            params['time_interval'] = st.number_input("时间误差限度:", value=0.2, step=0.1, format="%.2f")

        if st.button("确认输入"):
            st.write("输入参数已确认")
        
        collision_probability = predict_collision_probability(params)
        # 输出按钮
        if st.button("输出预测结果"):
            st.write(f"预测的碰撞概率: {collision_probability:.4f}")
            # use api
            analysis_result = use_api_part(params,collision_probability)

            if analysis_result:
                st.markdown("### DeepSeek 分析结果")
                st.markdown(analysis_result)
            else:
                st.markdown("### DeepSeek API 调用失败") 
                
        # 默认显示的 Markdown 文本框
        st.markdown("### 智能回答输出")
        st.markdown("请点击“输出预测结果”按钮以获取分析结果。")
        
    elif page == "漏水检测":
        main_box_leaking()

    elif page == "单步模拟":
        use_single_step()
    
    elif page == "文档页面":
        page_doc_part()

    elif page == "地图模拟":
        map_simu_part()