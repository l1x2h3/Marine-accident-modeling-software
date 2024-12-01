import streamlit as st
import textwrap

def use_page_markdown():
    # 使用 textwrap.dedent 去除多行字符串的缩进
    markdown_content = textwrap.dedent("""
    #### 航行条件分析与碰撞模拟

    本模型主要利用物理数学方法进行航行条件分析与碰撞模拟。以下是模型的主要原理和相关数学公式：

    ##### 1. 质心轨迹的切线距离
    质心轨迹的切线距离可以通过以下公式计算：

    $$
    d = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}
    $$

    其中，$(x_1, y_1)$ 和 $(x_2, y_2)$ 分别是质心轨迹上两个点的坐标。

    ###### 2. 刚体旋转方程
    刚体旋转方程描述了物体在旋转过程中的运动状态。旋转后的坐标可以通过以下公式计算：

    $$
    \\begin{pmatrix} x' \\\\ y' \\end{pmatrix} = \\begin{pmatrix} \\cos(\\theta) & -\\sin(\\theta) \\\\ \\sin(\\theta) & \\cos(\\theta) \\end{pmatrix} \\begin{pmatrix} x \\\\ y \\end{pmatrix}
    $$

    其中，$(x, y)$ 是旋转前的坐标，$(x', y')$ 是旋转后的坐标，$\\theta$ 是旋转角度。

    ##### 3. 旋转后的抛物线方程
    旋转后的抛物线方程可以通过以下公式表示：

    $$
    y' = a(x')^2 + bx' + c
    $$

    其中，$a$, $b$, $c$ 是抛物线方程的系数，$(x', y')$ 是旋转后的坐标。
    将旋转后的坐标代入抛物线方程，得到：

    $$
    y = a(x \\cos(\\theta) - y \\sin(\\theta))^2 + b(x \\cos(\\theta) - y \\sin(\\theta)) + c
    $$

    $$
    y = a(x^2 \\cos^2(\\theta) - 2xy \\cos(\\theta) \\sin(\\theta) + y^2 \\sin^2(\\theta)) + b(x \\cos(\\theta) - y \\sin(\\theta)) + c
    $$

    ##### 4. 多边形面积公式
    多边形的面积可以通过以下公式计算：

    $$
    A = \\frac{1}{2} \\left| \\sum_{i=1}^{n-1} (x_i y_{i+1} - y_i x_{i+1}) + (x_n y_1 - y_n x_1) \\right|
    $$

    其中，$(x_i, y_i)$ 是多边形的顶点坐标，$n$ 是顶点的数量。

    ---
    """)


    markdown_content2 = textwrap.dedent("""
    ---
    ##### 5. 质心坐标公式
    多边形的质心坐标可以通过以下公式计算：

    $$
    \\bar{x} = \\frac{1}{6A} \\sum_{i=1}^{n-1} (x_i + x_{i+1})(x_i y_{i+1} - x_{i+1} y_i)
    $$

    $$
    \\bar{y} = \\frac{1}{6A} \\sum_{i=1}^{n-1} (y_i + y_{i+1})(x_i y_{i+1} - x_{i+1} y_i)
    $$

    其中，$A$ 是多边形的面积，$(\\bar{x}, \\bar{y})$ 是质心坐标。

    ##### 6. 蒙特卡罗算法
    蒙特卡罗方法也可以用于估计概率。假设我们要估计事件 $A$ 发生的概率 $P(A)$，可以通过以下公式进行估计：

    $$
    P(A) \\approx \\frac{\\text{事件 } A \\text{ 发生的次数}}{N}
    $$

    其中，$N$ 是总的试验次数。
    蒙特卡罗方法还可以用于估计随机变量的期望值。假设我们要估计随机变量 $X$ 的期望值 $E[X]$，可以通过以下公式进行估计：

    $$
    E[X] \\approx \\frac{1}{N} \\sum_{i=1}^N X_i
    $$

    其中，$X_i$ 是随机变量 $X$ 的样本，$N$ 是样本数量。
    蒙特卡罗方法还可以用于估计随机变量的方差。假设我们要估计随机变量 $X$ 的方差 $\\text{Var}[X]$，可以通过以下公式进行估计：

    $$
    \\text{Var}[X] \\approx \\frac{1}{N} \\sum_{i=1}^N (X_i - \\bar{X})^2
    $$

    其中，$\\bar{X}$ 是样本均值，$N$ 是样本数量。

    通过以上数学方法和公式，本模型能够有效地进行航行条件分析与碰撞模拟。
                                        
    ---
    """)

    # 使用 st.markdown 显示内容
    st.markdown(markdown_content)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("fig/mk1.png", caption="碰撞的物理-数学方程图形", use_column_width=True)
  
    st.markdown(markdown_content2)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("fig/mk2.png", caption="碰撞的蒙特卡诺区域", use_column_width=True)
    st.markdown(
        """
        ---
        """
    )
   

