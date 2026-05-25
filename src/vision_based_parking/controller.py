import os
import sys
from pathlib import Path
from types import SimpleNamespace

MODULE_DIR = Path(__file__).resolve().parent


def configure_carla_pythonapi(path=None):
    """Add a CARLA PythonAPI location to sys.path when provided."""
    if path is None:
        path = os.environ.get('CARLA_PYTHONAPI_PATH')

    if not path:
        return

    resolved = Path(path).expanduser()
    if not resolved.is_absolute():
        resolved = (MODULE_DIR / resolved).resolve()

    if not resolved.exists():
        return

    if resolved.is_file():
        candidate_paths = [resolved.parent]
    else:
        candidate_paths = [resolved]
        if resolved.is_dir():
            candidate_paths.extend([
                resolved / 'dist',
                resolved / 'PythonAPI',
                resolved / 'PythonAPI' / 'carla',
                resolved / 'PythonAPI' / 'carla' / 'dist',
                resolved / 'carla',
                resolved / 'carla' / 'dist',
            ])

    for candidate in candidate_paths:
        if candidate.exists() and str(candidate) not in sys.path:
            sys.path.insert(0, str(candidate))


def load_carla_module():
    try:
        import carla
        return carla
    except ImportError:
        configure_carla_pythonapi()
        try:
            import carla
            return carla
        except ImportError:
            return None


class PIDController:
    def __init__(self, kp=0.8, ki=0.0, kd=0.1):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0.0
        self.integral = 0.0

    def update(self, error, dt=1.0):
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt != 0 else 0.0
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative


class ParkingController:
    _carla_module = None  # 缓存 carla 模块，避免重复导入

    def __init__(self, config):
        ctrl = config.get('controller', {})
        self.pid = PIDController(ctrl.get('kp', 0.8), ctrl.get('ki', 0.0), ctrl.get('kd', 0.1))
        self.max_steer = ctrl.get('max_steering_angle', 45)
        self.default_throttle = ctrl.get('default_throttle', 0.3)

    def _get_carla(self):
        """获取 carla 模块，缓存以便复用。"""
        if ParkingController._carla_module is None:
            ParkingController._carla_module = load_carla_module()
        return ParkingController._carla_module

    def compute_control(self, vehicle, target_x, dt=1.0):
        carla = self._get_carla()
        if carla is None:
            return SimpleNamespace(
                throttle=self.default_throttle,
                steer=0.0,
                brake=0.0,
            )

        control = carla.VehicleControl()
        if target_x is None:
            control.throttle = 0.0
            control.steer = 0.0
            control.brake = 0.0
            return control

        current_x = vehicle.get_transform().location.x
        error = target_x - current_x
        steer_value = self.pid.update(error, dt)

        # 防止 max_steer 为 0 导致除零
        divisor = max(abs(self.max_steer), 1e-6)
        steer_value = max(-divisor, min(divisor, steer_value)) / divisor

        control.throttle = self.default_throttle
        control.steer = steer_value
        control.brake = 0.0
        return control
