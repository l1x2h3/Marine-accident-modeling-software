import streamlit as st
import os

def page_enter_part():

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
                <!h3 style="color: black;"> </h3>
                <p style="color: black;">   本系统旨在通过分析航行器的速度、方向角偏差、质量数量级对比和天气条件，预测航行器之间是否会发生碰撞。</p>
                <p style="color: black;">   系统使用先进的深度学习模型，结合实时数据，提供准确的碰撞预测结果。</p>
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
            <div style="background-color: #ADD8E6; padding: 20px; border-radius: 10px;">
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
        ## 集中功能展示
        """
    )

    # 使用深灰色背景方框
    with st.container():
        st.markdown(
            """
            <div style="background-color: #D3D3D3; padding: 20px; border-radius: 10px;">
                <!h3 style="color: white;">  </h3>
                <p style="color: black;">这里展示了航行的具体情况</p>
                <!img src="src/page/logo.png" alt="航行器碰撞预测示意图" style="max-width: 100%; height: auto; margin: 0 auto;"></img>
                <li><strong>功能实现</strong>：基于自主设计验证的合成数据进行模型训练，较好的预测碰撞损失率</li>
                <li><strong>结果展示</strong>：展示碰撞预测结果，并提供详细的分析报告。</li>
                <li><strong>单步调试</strong>：逐步分析碰撞的全部过程</li>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")  # 右侧空白列
    # 创建三列，中间一列放置图片
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        current_directory = os.getcwd()
        relative_path1 = os.path.join(current_directory, '..', 'fig', 'coast.png')
        st.image(relative_path1, caption="海上岛礁路径展示", use_column_width=True)
    with col2:
        current_directory = os.getcwd()
        relative_path2 = os.path.join(current_directory, '..', 'fig', 'logo.png')
        st.image(relative_path2, caption="航行器logo", use_column_width=True)
    with col3:
        current_directory = os.getcwd()
        relative_path3 = os.path.join(current_directory, '..', 'fig', 'ship.png')
        st.image(relative_path3, caption="船只展示", use_column_width=True)

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
                <!h3 style="color: white;">核心技术路线: 采用复杂环境标注采样+刚体移动旋转模型+质心轨迹方程模拟+蒙特卡洛算法采样估计预测</h3>
                <!h3 style="color: white;"></h3>
                <p style="color: black;">训练流程包括： 物理算法数据预处理 + 随机森林算法训练 + 预测概率估计 + AI API接口评估</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.write("")  # 右侧空白列
    # 创建三列，中间一列放置图片
    col1, col2= st.columns([1, 1])
    with col1:
        current_directory = os.getcwd()
        relative_path4 = os.path.join(current_directory, '..', 'fig', 'distribution.png')
        st.image(relative_path4, caption="合成数据分布", use_column_width=True)
    with col2:
        current_directory = os.getcwd()
        relative_path5 = os.path.join(current_directory, '..', 'fig', 'workflow.png')
        st.image(relative_path5, caption="工作流程展示", use_column_width=True)


    # 底部信息
    st.markdown(
        """
        ---
        **© 2023 航行器碰撞预测系统** | **联系我们**：lixuhui123@mail.nwpu.edu.cn
        """
    )


if __name__ == "__main__":
    page_enter_part()