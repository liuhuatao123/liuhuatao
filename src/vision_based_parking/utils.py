# utils.py
import cv2
import numpy as np

def draw_car(frame, x, y, angle, color=(0, 255, 0)):
    """
    在图像上绘制代表车辆的矩形
    :param frame: 图像帧
    :param x, y: 中心坐标
    :param angle: 旋转角度
    :param color: 颜色
    """
    # 简单的矩形代表车，实际项目中这里会加载车辆图片
    box = cv2.boxPoints(((x, y), (40, 20), angle)) 
    box = np.int0(box)
    cv2.drawContours(frame, [box], 0, color, 2)

def calculate_error(current_x, target_x):
    """
    计算横向误差
    """
    return target_x - current_x