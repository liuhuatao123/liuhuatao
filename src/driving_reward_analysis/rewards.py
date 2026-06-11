"""
自动驾驶奖励函数定义模块

实现三类核心奖励函数：
- 速度跟踪奖励 (Speed Tracking Reward)
- 距离控制奖励 (Distance Control Reward)
- 舒适性奖励 (Comfort Reward)
"""

import numpy as np


class SpeedReward:
    """速度跟踪奖励函数
    
    基于高斯分布建模，车辆速度越接近目标速度奖励越高。
    当速度等于目标速度时，奖励达到最大值。
    """
    
    def __init__(self, target_speed=25.0, tolerance=5.0):
        self.target_speed = target_speed
        self.tolerance = tolerance
    
    def compute(self, speed):
        """计算速度跟踪奖励
        
        Args:
            speed: 当前速度 (m/s)，标量或数组
            
        Returns:
            奖励值，范围约为 [-0.5, 0.5]
        """
        speed = np.asarray(speed, dtype=float)
        # 高斯型奖励函数，峰值在 target_speed
        reward = np.exp(-0.5 * ((speed - self.target_speed) / self.tolerance) ** 2) * 0.5
        # 添加偏移使低速时有一定负奖励
        reward -= 0.5
        return reward
    
    def get_range(self):
        """返回速度分析范围"""
        return np.linspace(0, 35, 500)


class DistanceReward:
    """距离控制奖励函数
    
    分段线性函数建模：
    - 小于临界距离：最大惩罚 (-1.0)
    - 临界距离到安全距离之间：线性过渡
    - 大于安全距离：零奖励（不额外鼓励过远距离）
    """
    
    def __init__(self, safe_distance=15.0, critical_distance=5.0):
        self.safe_distance = safe_distance
        self.critical_distance = critical_distance
    
    def compute(self, distance):
        """计算距离控制奖励
        
        Args:
            distance: 前车距离 (m)，标量或数组
            
        Returns:
            奖励值，范围 [-1.0, 0.0]
        """
        distance = np.asarray(distance, dtype=float)
        reward = np.zeros_like(distance)
        
        # 小于临界距离：最大惩罚
        mask_critical = distance < self.critical_distance
        reward[mask_critical] = -1.0
        
        # 临界距离到安全距离之间：线性过渡
        mask_transition = (distance >= self.critical_distance) & (distance < self.safe_distance)
        reward[mask_transition] = -1.0 + (distance[mask_transition] - self.critical_distance) / \
                                       (self.safe_distance - self.critical_distance)
        
        # 大于安全距离：零奖励
        mask_safe = distance >= self.safe_distance
        reward[mask_safe] = 0.0
        
        return reward
    
    def get_range(self):
        """返回距离分析范围"""
        return np.linspace(0, 100, 500)


class ComfortReward:
    """舒适性奖励函数
    
    基于加速度的二次函数建模：
    - 零加速度时奖励最高
    - 加速度绝对值越大，惩罚越严重
    """
    
    def __init__(self, max_acceleration=2.0):
        self.max_acceleration = max_acceleration
    
    def compute(self, acceleration):
        """计算舒适性奖励
        
        Args:
            acceleration: 当前加速度 (m/s²)，标量或数组
            
        Returns:
            奖励值，范围约为 [-0.5, 0.5]
        """
        acceleration = np.asarray(acceleration, dtype=float)
        # 二次函数，峰值在 0
        reward = 0.5 - 0.5 * (acceleration / self.max_acceleration) ** 2
        return reward
    
    def get_range(self):
        """返回加速度分析范围"""
        return np.linspace(-3, 2, 500)


def create_rewards_from_config(config):
    """从配置字典创建奖励函数实例
    
    Args:
        config: 配置字典，通常从 config.yaml 加载
        
    Returns:
        dict: 包含三个奖励函数实例的字典
    """
    speed_cfg = config.get('speed_reward', {})
    distance_cfg = config.get('distance_reward', {})
    comfort_cfg = config.get('comfort_reward', {})
    
    return {
        'speed': SpeedReward(
            target_speed=speed_cfg.get('target_speed', 25.0),
            tolerance=speed_cfg.get('tolerance', 5.0)
        ),
        'distance': DistanceReward(
            safe_distance=distance_cfg.get('safe_distance', 15.0),
            critical_distance=distance_cfg.get('critical_distance', 5.0)
        ),
        'comfort': ComfortReward(
            max_acceleration=comfort_cfg.get('max_acceleration', 2.0)
        )
    }
