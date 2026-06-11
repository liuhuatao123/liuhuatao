"""
奖励函数可视化模块

提供专业的奖励函数曲线绘制功能，支持：
- 单函数详细分析图
- 多函数对比分析图
- 批量参数对比图
"""

import os
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # 无GUI后端，适合服务器运行
import matplotlib.pyplot as plt
import numpy as np


def setup_chinese_font():
    """配置中文字体支持"""
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False


def plot_reward_analysis(rewards, config, output_path):
    """绘制奖励函数综合分析图
    
    生成与示例图片类似的三子图布局：
    - 上：速度跟踪奖励
    - 中：距离控制奖励
    - 下：舒适性奖励
    
    Args:
        rewards: dict，包含 'speed', 'distance', 'comfort' 三个奖励函数实例
        config: 配置字典
        output_path: 输出图片路径
    """
    setup_chinese_font()
    
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), dpi=150)
    fig.patch.set_facecolor('white')
    
    # ===== 子图1：速度跟踪奖励 =====
    ax1 = axes[0]
    speed_range = rewards['speed'].get_range()
    speed_reward = rewards['speed'].compute(speed_range)
    
    ax1.plot(speed_range, speed_reward, 'b-', linewidth=1.5, label='Speed Reward')
    target_speed = config['speed_reward']['target_speed']
    ax1.axvline(x=target_speed, color='r', linestyle='--', linewidth=1.5, 
                label=f'Target Speed ({target_speed} m/s)')
    ax1.set_title('Speed Tracking Reward', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Speed (m/s)', fontsize=11)
    ax1.set_ylabel('Reward', fontsize=11)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 35)
    
    # ===== 子图2：距离控制奖励 =====
    ax2 = axes[1]
    distance_range = rewards['distance'].get_range()
    distance_reward = rewards['distance'].compute(distance_range)
    
    ax2.plot(distance_range, distance_reward, 'b-', linewidth=1.5, label='Distance Reward')
    safe_distance = config['distance_reward']['safe_distance']
    ax2.axvline(x=safe_distance, color='r', linestyle='--', linewidth=1.5,
                label=f'Min Safe Distance ({safe_distance} m)')
    ax2.set_title('Distance Control Reward', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Distance (m)', fontsize=11)
    ax2.set_ylabel('Reward', fontsize=11)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 100)
    
    # ===== 子图3：舒适性奖励 =====
    ax3 = axes[2]
    accel_range = rewards['comfort'].get_range()
    comfort_reward = rewards['comfort'].compute(accel_range)
    
    ax3.plot(accel_range, comfort_reward, 'b-', linewidth=1.5, label='Comfort Reward')
    ax3.axvline(x=0, color='r', linestyle='--', linewidth=1.5,
                label='Zero Acceleration')
    ax3.set_title('Comfort Reward', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Acceleration (m/s²)', fontsize=11)
    ax3.set_ylabel('Reward', fontsize=11)
    ax3.legend(loc='upper right', fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(-3, 2)
    
    plt.tight_layout(pad=2.0)
    
    # 保存图片
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    
    print(f"  已保存: {output_path}")


def plot_parameter_comparison(reward_class, param_name, param_values, 
                               fixed_params, output_path, xlabel='X'):
    """绘制不同参数下的奖励函数对比图
    
    Args:
        reward_class: 奖励函数类
        param_name: 要变化的参数名
        param_values: 参数取值列表
        fixed_params: 固定参数字典
        output_path: 输出图片路径
        xlabel: X轴标签
    """
    setup_chinese_font()
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    fig.patch.set_facecolor('white')
    
    colors = plt.cm.viridis(np.linspace(0, 0.8, len(param_values)))
    
    for i, val in enumerate(param_values):
        params = fixed_params.copy()
        params[param_name] = val
        reward = reward_class(**params)
        x_range = reward.get_range()
        y_values = reward.compute(x_range)
        ax.plot(x_range, y_values, color=colors[i], linewidth=1.5,
                label=f'{param_name}={val}')
    
    ax.set_title(f'{reward_class.__name__} - Parameter Comparison', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel('Reward', fontsize=11)
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    
    print(f"  已保存: {output_path}")
