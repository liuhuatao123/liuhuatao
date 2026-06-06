# CARLA 视觉泊车与路径规划系统

## 1. 项目简介
本项目基于 CARLA 自动驾驶模拟器，实现了一套完整的视觉感知与路径规划系统。系统利用车载摄像头采集图像，通过计算机视觉算法识别周围环境与车位，并结合 PID 控制算法控制车辆在仿真环境中自动行驶与泊车。

## 2. 选题说明
- **技术方案**: 基于 CARLA 模拟器的视觉泊车系统，采用 Canny 边缘检测 + Hough 直线检测进行车位识别，PID 控制器进行车辆转向控制。
- **设计思路**: 将感知、规划、控制三个模块解耦，通过配置文件统一管理参数，支持 CARLA 真机模式和本地演示模式的无缝切换。

## 3. 开发运行环境
- **操作系统**: Windows 10/11, Ubuntu 20.04/22.04
- **仿真平台**: CARLA 0.9.13+
- **编程语言**: Python 3.7+
- **核心框架**: OpenCV, NumPy, PyTorch (可选), CARLA Python API
- **开发工具**: Visual Studio Code / PyCharm

## 4. 模块结构与入口
- 本模块的所有核心代码存放于 `src/vision_based_parking` 目录下。
- 模块的主程序入口为 `main.py`。

---

# [第1次提交] vision_based_parking: CARLA 视觉泊车与路径规划系统

## 1. 模块功能
本模块实现了 CARLA 自动驾驶场景中视觉泊车的完整闭环：

- **视觉感知**: 通过 Canny 边缘检测和 Hough 直线变换，实时检测图像中的车道线和车位目标，支持未来扩展 YOLO 等深度学习检测器。
- **路径规划**: 基于检测到的目标位置（target_x），计算车辆的目标转向角度，生成泊车引导路径。
- **PID 控制**: 实现经典 PID 控制器，根据位置误差实时计算转向指令，控制车辆平稳驶向目标车位。
- **多模式运行**: 支持连接 CARLA 服务器的真机模式，以及无需 CARLA 的本地演示模式（DemoVehicle）。
- **灵活配置**: 通过 `config.yaml` 统一管理 CARLA 连接参数、车辆参数、PID 控制参数和视觉检测阈值。

## 2. 运行指南

### 步骤 1：启动 CARLA 模拟器
首先，启动 CARLA 模拟器：

**Windows:**
```bash
cd CARLA根目录
CarlaUE4.exe -windowed -ResX=800 -ResY=600
```

**Linux:**
```bash
cd CARLA根目录
./CarlaUE4.sh -windowed -ResX=800 -ResY=600
```

### 步骤 2：配置 Python 环境
```bash
pip install opencv-python numpy pyyaml -i https://pypi.tuna.tsinghua.edu.cn/simple
```

如需使用深度学习检测器（如 YOLOv8），还需安装：
```bash
pip install torch ultralytics -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 步骤 3：配置 CARLA Python API
在 `config.yaml` 中设置 CARLA Python API 路径：
```yaml
carla_pythonapi_path: "../../hutb/PythonAPI/carla/dist"
```
或设置环境变量：
```bash
set CARLA_PYTHONAPI_PATH=D:\hutb\PythonAPI\carla\dist    # Windows
export CARLA_PYTHONAPI_PATH=/opt/carla/PythonAPI/carla/dist  # Linux
```

### 步骤 4：运行程序
在项目根目录下执行：
```bash
python src/vision_based_parking/main.py
```

如果未安装 CARLA 或 CARLA 服务器未启动，程序会自动进入演示模式，使用虚拟车辆进行仿真。

### 步骤 5：操作说明
- 程序启动后将打开 `Vision Based Parking` 窗口，显示检测结果和路径规划信息。
- 左上角显示目标 X 坐标和当前转向角度。
- 按 `q` 键退出程序。

## 3. 配置说明
`config.yaml` 主要参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `carla_host` | CARLA 服务器 IP | localhost |
| `carla_port` | CARLA 服务器端口 | 2000 |
| `carla_pythonapi_path` | CARLA Python API 路径 | ../../hutb/PythonAPI/carla/dist |
| `vehicle_blueprint` | 车辆蓝图名称 | vehicle.lincoln.mkz_2017 |
| `simulation.fps` | 仿真帧率 | 30 |
| `controller.kp` | PID 比例系数 | 0.8 |
| `controller.ki` | PID 积分系数 | 0.0 |
| `controller.kd` | PID 微分系数 | 0.1 |
| `controller.max_steering_angle` | 最大转向角度 | 45 |
| `controller.default_throttle` | 默认油门 | 0.3 |
| `vision.canny_thresh1` | Canny 阈值1 | 50 |
| `vision.canny_thresh2` | Canny 阈值2 | 150 |

## 4. 模块文件说明
| 文件 | 功能 |
|------|------|
| `main.py` | 主入口，连接 CARLA、协调感知与控制循环 |
| `detector.py` | 视觉感知模块：Canny + Hough 车位检测 |
| `controller.py` | 控制模块：PID 控制器 + CARLA API 路径配置 |
| `utils.py` | 工具库：图像绘制、数值钳位辅助函数 |
| `config.yaml` | 配置文件：CARLA 连接参数、车辆参数、检测阈值 |

## 5. 参考
- [CARLA 官方文档](https://carla.readthedocs.io/)
- [CARLA Python API 参考](https://carla.readthedocs.io/en/latest/python_api/)
- [OpenCV Canny 边缘检测](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)
- [Hough 直线变换](https://docs.opencv.org/4.x/d9/db0/tutorial_hough_lines.html)
