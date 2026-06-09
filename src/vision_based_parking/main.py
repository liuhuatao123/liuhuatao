import os
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import cv2
import yaml

from controller import ParkingController, configure_carla_pythonapi
from detector import ParkingDetector
from utils import draw_text


class DemoVehicle:
    def __init__(self):
        self.current_x = 0.0

    def get_transform(self):
        return SimpleNamespace(location=SimpleNamespace(x=self.current_x))

    def apply_control(self, control):
        self.current_x += float(getattr(control, 'throttle', 0.0)) * 0.01


def load_config(path='config.yaml'):
    config_path = Path(path)
    if not config_path.is_absolute():
        config_path = Path(__file__).resolve().parent / config_path

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def configure_carla_for_run(config):
    custom_path = config.get('carla_pythonapi_path')
    if custom_path:
        configure_carla_pythonapi(custom_path)
        return

    env_path = os.environ.get('CARLA_PYTHONAPI_PATH')
    if env_path:
        configure_carla_pythonapi(env_path)


def connect_carla(host, port, timeout=10.0):
    try:
        import carla
        client = carla.Client(host, port)
        client.set_timeout(timeout)
        return client
    except (ImportError, AttributeError) as exc:
        raise RuntimeError('CARLA Python API 未安装或不完整，请先安装 carla 模块或提供完整的 fake API。') from exc


def run_simulation_loop(config, detector, controller, world, vehicle):
    print('仿真循环已启动，按 q 退出。')
    target_fps = config['simulation'].get('fps', 30)
    frame_duration = 1.0 / target_fps
    prev_time = time.perf_counter()

    while True:
        loop_start = time.perf_counter()
        dt = loop_start - prev_time
        prev_time = loop_start

        frame = detector.capture_frame(world, vehicle)
        result_frame, target_x = detector.detect(frame)
        control = controller.compute_control(vehicle, target_x, dt)

        if vehicle is not None:
            vehicle.apply_control(control)

        draw_text(result_frame, f"目标 X: {target_x}", (20, 30))
        draw_text(result_frame, f"转向: {control.steer:.2f}", (20, 60))
        cv2.imshow('Vision Based Parking', result_frame)

        if cv2.waitKey(1) == ord('q'):
            break

        # 精确帧率控制：扣除本帧已用时间后再休眠
        elapsed = time.perf_counter() - loop_start
        sleep_time = frame_duration - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)


def main():
    config = load_config()
    print(f"加载配置：{config}")

    configure_carla_for_run(config)

    detector = ParkingDetector(config)
    controller = ParkingController(config)

    world = None
    vehicle = None

    try:
        client = connect_carla(config.get('carla_host', 'localhost'), config.get('carla_port', 2000))
        world = client.get_world()

        print('正在生成仿真车辆...')
        blueprint_library = world.get_blueprint_library()
        vehicle_bp = blueprint_library.find(config.get('vehicle_blueprint', 'vehicle.lincoln.mkz_2017'))
        spawn_point = world.get_map().get_spawn_points()[0]
        vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    except RuntimeError as exc:
        print(f"{exc}，进入演示模式。")
        vehicle = DemoVehicle()

    try:
        run_simulation_loop(config, detector, controller, world, vehicle)
    finally:
        print('销毁车辆并关闭窗口。')
        if hasattr(vehicle, 'destroy'):
            vehicle.destroy()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
