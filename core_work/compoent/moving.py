import pyvista as pv
import numpy as np
from ship import mesh
# 创建一个立方体
# mesh = pv.Cube()
# mesh为创建的对象，后面需要对mesh进行操作
# 创建 Plotter 对象
plotter = pv.Plotter()

# 添加网格到 Plotter
plotter.add_mesh(mesh, show_edges=True, color='blue')

# 设置背景颜色
plotter.background_color = 'white'

# 打开交互式窗口
plotter.show(auto_close=False, interactive=False)

# 动画循环
for scale in np.linspace(1, 2, 100):
    # 更新网格的顶点坐标
    mesh.points = mesh.points * scale
    
    # 重新渲染
    plotter.render()

# 关闭窗口
plotter.close()