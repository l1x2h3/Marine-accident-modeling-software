from PIL import Image
import numpy as np

def get_pb_matrix(image_path, num_samples_x=1000, num_samples_y=None):
    # 打开图像
    image = Image.open(image_path)
    
    # 将图像转换为 RGB 模式（如果它不是 RGB 模式）
    image = image.convert('RGB')
    
    # 获取图像的宽度和高度
    width, height = image.size
    
    # 如果 num_samples_y 未指定，则默认与 num_samples_x 相同
    if num_samples_y is None:
        num_samples_y = num_samples_x
    
    # 计算每个采样点的步长
    step_x = width / num_samples_x
    step_y = height / num_samples_y
    
    # 初始化 pb 矩阵
    pb_matrix = np.zeros((num_samples_y, num_samples_x))
    
    # 遍历每个采样点
    for i in range(num_samples_y):
        for j in range(num_samples_x):
            # 计算采样点的坐标
            x = int(j * step_x)
            y = int(i * step_y)
            
            # 获取像素的 RGB 值
            r, g, b = image.getpixel((x, y))
            
            # 计算亮度
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            
            # 将亮度归一化到 0.0 到 1.0 之间
            pb_value = luminance / 255.0
            
            # 将 pb 值存入矩阵
            pb_matrix[i, j] = pb_value
    
    return pb_matrix

# 示例用法
image_path = 'fig/water_deep.png'
pb_matrix = get_pb_matrix(image_path)
np.set_printoptions(threshold=np.inf)
print(pb_matrix)