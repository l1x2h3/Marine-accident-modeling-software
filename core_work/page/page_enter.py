import streamlit as st
import os

def page_enter_part():

    # 设置页面标题
    st.title("航行器碰撞预测系统")

    # 设置页面描述
    st.markdown(
        """
        ## 简介
        """
    )

    with st.container():
        st.markdown(
            """
            <div style="background-color: #D3D3D3; padding: 20px; border-radius: 10px;">
                <!h3 style="color: white;"> </h3>
                <p style="color: white;">本系统旨在通过分析航行器的速度、方向角偏差、质量数量级对比和天气条件，预测航行器之间是否会发生碰撞。系统使用先进的深度学习模型，结合实时数据，提供准确的碰撞预测结果。</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 功能描述
    st.markdown(
        """
        ## 主要功能
        """
    )
    st.markdown(
            """
            <div style="background-color: #D3D3D3; padding: 20px; border-radius: 10px;">
                <!h2 style="color: black;"> </h2>
                <ul>
                    <li><strong>数据输入</strong>：输入航行器的速度、方向角偏差、质量数量级对比和天气条件。</li>
                    <li><strong>碰撞预测</strong>：基于输入数据，使用深度学习模型预测是否会发生碰撞。</li>
                    <li><strong>结果展示</strong>：展示碰撞预测结果，并提供详细的分析报告。</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 插入图片预留位置
    st.markdown(
        """
        ## 图片预留位置
        """
    )

    # 使用深灰色背景方框
    with st.container():
        st.markdown(
            """
            <div style="background-color: #D3D3D3; padding: 20px; border-radius: 10px;">
                <h3 style="color: white;">图片预留位置</h3>
                <!p style="color: white;">在这里插入图片，展示航行器碰撞预测的相关信息。</p>
                <img src="../fig/logo.png" alt="航行器碰撞预测示意图" style="max-width: 100%; height: auto; margin: 0 auto;">
            </div>
            """,
            unsafe_allow_html=True
        )

    # 预留开发区域
    st.markdown(
        """
        ## 开发区域
        以下区域预留给开发者进行进一步的功能扩展和定制。
        """
    )

    # 使用蓝色背景方框
    with st.container():
        st.markdown(
            """
            <div style="background-color: #ADD8E6; padding: 20px; border-radius: 10px;">
                <h3 style="color: white;">开发区域</h3>
                <p style="color: white;">在这里添加你的自定义功能和代码。</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 底部信息
    st.markdown(
        """
        ---
        **© 2023 航行器碰撞预测系统** | **联系我们**：lixuhui123@mail.nwpu.edu.cn
        """
    )