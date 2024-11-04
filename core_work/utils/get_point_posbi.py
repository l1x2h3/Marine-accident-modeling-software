import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def classify_colors(image, num_clusters=5):
    # 将图像转换为 numpy 数组
    image_array = np.array(image)
    
    # 将图像展平为二维数组
    pixels = image_array.reshape(-1, 3)
    
    # 使用 K-means 进行颜色分类
    kmeans = KMeans(n_clusters=num_clusters, n_init=10)
    kmeans.fit(pixels)
    
    # 获取每个像素的分类标签
    labels = kmeans.labels_
    
    # 将标签映射回图像
    classified_image = labels.reshape(image_array.shape[:2])
    
    return classified_image, kmeans.cluster_centers_

def calculate_depth(pb_matrix, classified_image, color_index):
    # 获取颜色分类的像素坐标
    indices = np.where(classified_image == color_index)
    
    # 计算该颜色分类的平均深度
    depths = pb_matrix[indices]
    average_depth = np.mean(depths)
    
    return average_depth, depths

def plot_depth_distribution(classified_image, depths, color_index):
    # 获取颜色分类的像素坐标
    indices = np.where(classified_image == color_index)
    
    # 绘制深度分布图
    plt.figure(figsize=(10, 10))
    plt.scatter(indices[1], indices[0], c=depths, cmap='viridis', s=50)
    plt.colorbar(label='Depth')
    plt.title(f'Depth Distribution for Color Index {color_index}')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.show()