# main_parking_sim.py
import cv2
import numpy as np
import yaml
from main_parking_detector import ParkingDetector
from main_parking_ctrl import ParkingController
from utils import draw_car

# 1. 加载配置
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def main():
    # 2. 初始化模块
    detector = ParkingDetector()
    controller = ParkingController(config)

    # 3. 初始化车辆状态 (x, y, 角度)
    car_x, car_y, car_angle = 100, 500, -10 # 初始在左下角，稍微偏一点

    # 创建一个黑色的画布作为仿真环境
    simulation_window = "Vision Based Parking Sim"
    cv2.namedWindow(simulation_window)

    print("🚗 泊车仿真启动! 按 'q' 退出")

    while True:
        # --- 仿真环境渲染 ---
        # 创建一个空白图像 (黑色背景)
        frame = np.zeros((config['simulation']['height'], config['simulation']['width'], 3), dtype=np.uint8)
        
        # 画出简单的地面标线 (模拟摄像头看到的画面)
        cv2.rectangle(frame, (300, 0), (500, 200), (255, 255, 255), 2) # 车位框

        # --- 1. 感知 (视觉) ---
        # 将当前帧传给检测器，获取目标点
        processed_frame, target_x = detector.detect(frame)

        # --- 2. 控制 (大脑) ---
        # 计算应该打多少方向盘
        # 假设车辆中心就是 car_x
        steering_angle = controller.compute_action(car_x, target_x)

        # --- 3. 运动学更新 (物理) ---
        # 简单的运动模型：车一直向前开，根据转向角改变横向位置
        # 这里为了演示简化了物理公式
        speed = 2
        car_x += speed