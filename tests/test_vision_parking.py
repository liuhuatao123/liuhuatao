import importlib.util
import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
vision_root = project_root / 'src' / 'vision_based_parking'
sys.path.insert(0, str(vision_root))

from controller import ParkingController, configure_carla_pythonapi, load_carla_module


def test_controller_falls_back_without_carla():
    controller = ParkingController({
        'controller': {
            'kp': 1.0,
            'ki': 0.0,
            'kd': 0.0,
            'max_steering_angle': 45,
            'default_throttle': 0.25,
        }
    })

    control = controller.compute_control(vehicle=None, target_x=120)

    assert control.throttle == 0.25
    assert control.steer == 0.0
    assert control.brake == 0.0


def test_load_config_resolves_relative_to_module_dir(tmp_path):
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        spec = importlib.util.spec_from_file_location(
            'main',
            vision_root / 'main.py',
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        config = module.load_config()
    finally:
        os.chdir(original_cwd)

    assert config['carla_host'] == 'localhost'
    assert config['carla_port'] == 2000


def test_configure_carla_pythonapi_loads_stub_module(tmp_path, monkeypatch):
    stub_root = tmp_path / 'fake_carla_api'
    stub_root.mkdir()
    (stub_root / 'carla.py').write_text('class VehicleControl:\n    pass\n')

    monkeypatch.setenv('CARLA_PYTHONAPI_PATH', str(stub_root))
    sys.modules.pop('carla', None)
    configure_carla_pythonapi()

    module = load_carla_module()

    assert module is not None
    assert module.__name__ == 'carla'
    assert str(stub_root) in sys.path


def test_configure_carla_pythonapi_loads_stub_file_path(tmp_path, monkeypatch):
    stub_root = tmp_path / 'fake_carla_api'
    stub_root.mkdir()
    stub_file = stub_root / 'carla.py'
    stub_file.write_text('class VehicleControl:\n    pass\n')

    monkeypatch.delenv('CARLA_PYTHONAPI_PATH', raising=False)
    sys.modules.pop('carla', None)
    configure_carla_pythonapi(str(stub_file))

    module = load_carla_module()

    assert module is not None
    assert module.__name__ == 'carla'
    assert str(stub_root) in sys.path


def test_connect_carla_raises_runtime_error_for_incomplete_stub(tmp_path, monkeypatch):
    stub_root = tmp_path / 'fake_carla_api'
    stub_root.mkdir()
    (stub_root / 'carla.py').write_text('class VehicleControl:\n    pass\n')

    monkeypatch.delenv('CARLA_PYTHONAPI_PATH', raising=False)
    sys.modules.pop('carla', None)

    spec = importlib.util.spec_from_file_location(
        'main',
        vision_root / 'main.py',
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.configure_carla_for_run({'carla_pythonapi_path': str(stub_root)})

    try:
        module.connect_carla('localhost', 2000)
    except RuntimeError as exc:
        assert 'CARLA Python API' in str(exc)
    else:
        raise AssertionError('Expected RuntimeError when fake API is incomplete')
