"""
工具函数模块

提供辅助功能：配置加载、数据生成、文件管理等
"""

import os
from pathlib import Path

import yaml


def load_config(config_path='config.yaml'):
    """加载 YAML 配置文件
    
    Args:
        config_path: 配置文件路径，默认为当前目录下的 config.yaml
        
    Returns:
        dict: 配置字典
    """
    config_file = Path(config_path)
    if not config_file.is_absolute():
        config_file = Path(__file__).resolve().parent / config_file
    
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def ensure_output_dir(output_dir):
    """确保输出目录存在
    
    Args:
        output_dir: 输出目录路径
        
    Returns:
        Path: 输出目录的 Path 对象
    """
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def generate_scenario_data(num_samples=1000):
    """生成模拟驾驶场景数据
    
    生成随机的速度、距离、加速度数据，用于批量奖励计算
    
    Args:
        num_samples: 样本数量
        
    Returns:
        dict: 包含 'speed', 'distance', 'acceleration' 三个数组的字典
    """
    np = __import__('numpy')
    
    # 速度：正态分布，均值 20 m/s，标准差 5
    speed = np.random.normal(20, 5, num_samples)
    speed = np.clip(speed, 0, 40)
    
    # 距离：指数分布，模拟不同跟车距离
    distance = np.random.exponential(20, num_samples)
    distance = np.clip(distance, 0, 100)
    
    # 加速度：正态分布，均值 0，标准差 1
    acceleration = np.random.normal(0, 1, num_samples)
    acceleration = np.clip(acceleration, -3, 3)
    
    return {
        'speed': speed,
        'distance': distance,
        'acceleration': acceleration
    }


def compute_total_reward(rewards, scenario_data):
    """计算总奖励
    
    根据场景数据，计算三类奖励的加权和
    
    Args:
        rewards: dict，包含三个奖励函数实例
        scenario_data: dict，包含场景数据
        
    Returns:
        dict: 包含各类奖励和总奖励的字典
    """
    speed_r = rewards['speed'].compute(scenario_data['speed'])
    distance_r = rewards['distance'].compute(scenario_data['distance'])
    comfort_r = rewards['comfort'].compute(scenario_data['acceleration'])
    
    # 简单加权求和（可根据需求调整权重）
    total_r = speed_r + distance_r + comfort_r
    
    return {
        'speed_reward': speed_r,
        'distance_reward': distance_r,
        'comfort_reward': comfort_r,
        'total_reward': total_r
    }
