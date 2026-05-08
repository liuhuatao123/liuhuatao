# main_parking_detector.py
import cv2
import numpy as np

class ParkingDetector:
    def __init__(self):
        self.parking_spot_center = None

    def detect(self, frame):
        """
        输入: 原始图像
        输出: 处理后的图像, (车位中心x, 车位中心y) 或 None
        """
        # 1. 灰度化
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 2. 边缘检测 (Canny)
        edges = cv2.Canny(gray, 50, 150)

        # 3. 霍夫变换检测直线
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

        parking_x = None

        if lines is not None:
            # 简单逻辑：假设我们要找两条垂直的线作为车位边界
            # 这里为了演示，我们简化为：如果检测到线，就在图像中心画个目标点
            # 实际逻辑应解析 lines 数组找到两条平行线的中间
            
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2) # 画出检测到的蓝线

            # 模拟：假设车位就在屏幕正中央 (400, 300)
            # 真实项目中，这里需要计算两条白线的几何中心
            parking_x = frame.shape[1] // 2 
            
            # 在图像上标记目标中心
            cv2.circle(frame, (parking_x, 100), 5, (0, 0, 255), -1)

        return frame, parking_x