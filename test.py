from mayavi import mlab
import numpy as np

# 创建数据
x, y = np.mgrid[-10:10:100j, -10:10:100j]
z = np.sin(np.sqrt(x**2 + y**2))

# 创建 3D 曲面图
mlab.surf(x, y, z)

# 显示图形
mlab.show()