CARLA 视觉泊车与路径规划系统
本项目基于 CARLA 自动驾驶模拟器，实现了一套完整的视觉感知与路径规划系统。系统利用车载摄像头采集图像，通过目标检测算法（如 YOLO）识别周围环境与车位，并结合规划算法控制车辆在仿真环境中自动行驶与泊车。
项目演示
系统运行界面预览
左侧：控制台日志，实时显示 FPS、车速、检测目标数量及车辆状态（如“车辆已重置到新位置”）。
中间：第一人称视角与规划路径显示（蓝色引导线）。
右侧：第三人称追踪视角，展示车辆整体运动姿态。
小窗：目标检测视图，实时标注检测到的障碍物或车位。
功能特性
高保真仿真：基于 CARLA 模拟器，提供逼真的城市环境与物理反馈。
视觉感知：集成目标检测算法（如 YOLO），实时处理摄像头数据，识别车位、车辆及交通标志。
智能规划：实现基于视觉反馈的路径规划算法，引导车辆完成泊车或巡航任务。
实时控制：通过 Python API 与 CARLA 交互，发送油门、刹车及转向指令。
文件结构
carla_vision_parking/
├── main_planner.py           # 主程序：连接CARLA服务器，协调感知与控制循环
├── detector.py               # 视觉模块：封装YOLO或其他检测算法
├── controller.py             # 控制模块：PID控制器或纯追踪算法
├── config.yaml               # 配置文件：CARLA连接参数、车辆参数、检测阈值
└── utils.py                  # 工具库：坐标转换、图像绘制辅助函数
环境依赖
在运行项目之前，请确保您的系统满足以下要求：
CARLA 模拟器：版本 0.9.13 或更高版本（下载地址）。
Python：版本 3.7 或更高。
Python 库：
opencv-python：用于图像处理。
numpy：用于数学计算。
pygame：用于简单的可视化（可选）。
torch / ultralytics：如果使用 YOLOv8 进行检测。
carla：CARLA 的 Python API（通常在 PythonAPI/carla/dist/ 目录下）。
安装依赖库：
pip install opencv-python numpy pygame torch ultralytics
pip install opencv-python numpy pygame torch ultralytics
运行步骤
启动 CARLA 服务器：
首先，启动 CARLA 模拟器。您可以使用以下命令启动服务器（Windows）：
# 在 CARLA 根目录下运行
CarlaUE4.exe -windowed -ResX=800 -ResY=600
或者在 Linux 上：
./CarlaUE4.sh -windowed -ResX=800 -ResY=600
运行主程序：
打开一个新的终端窗口，导航到项目目录并运行主程序：
python main_planner.py
观察仿真：
程序启动后，您将看到 CARLA 模拟器窗口中出现车辆，并且控制台会输出实时的日志信息。您可以通过调整 config.yaml 中的参数来优化车辆的行为。
配置说明
您可以在 config.yaml 文件中调整以下参数：
carla_host: CARLA 服务器的 IP 地址（默认为 localhost）。
carla_port: CARLA 服务器的端口号（默认为 2000）。
vehicle_speed: 车辆的最大行驶速度。
parking_threshold: 判断车辆是否到达停车位的阈值。
