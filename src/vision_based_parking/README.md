# Vision Based Parking (基于视觉的自动泊车系统)

本项目实现了一个基于计算机视觉的自动泊车仿真系统。系统通过摄像头获取环境图像，利用图像处理技术识别停车位，并控制车辆自动泊入指定车位。

## 🚀 项目简介

该项目模拟了自动驾驶车辆在停车场环境下的感知与控制流程。主要包含以下模块：
- **感知模块 (`main_parking_detector.py`)**：使用 OpenCV 进行边缘检测和霍夫变换，识别地面车位线。
- **控制模块 (`main_parking_ctrl.py`)**：基于 PID 算法计算转向角度和速度，实现车辆的闭环控制。
- **仿真模块 (`main_parking_sim.py`)**：基于 Pygame/Python 的 2D 仿真环境，可视化车辆运动轨迹。

## 📂 文件结构

- `main_parking_sim.py`: **主程序**，启动仿真循环，整合感知与控制模块。
- `main_parking_detector.py`: 视觉处理脚本，负责从图像中提取车位特征。
- `main_parking_ctrl.py`: 车辆运动控制脚本，负责计算车辆下一步的动作。
- `config.yaml`: 配置文件，包含车辆参数、PID 增益及仿真设置。
- `utils.py`: 工具库，包含坐标转换、绘图辅助函数等。

## 🛠️ 环境依赖

请确保已安装以下 Python 库：

- OpenCV (`cv2`)
- NumPy
- PyYAML
- Pygame (用于仿真显示)

你可以使用以下命令安装依赖：

```bash
pip install opencv-python numpy pyyaml pygame
