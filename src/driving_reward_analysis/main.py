"""
自动驾驶奖励函数分析系统 - 主入口

整合奖励函数建模、批量仿真与可视化输出的完整流水线。

使用示例:
    python main.py              # 运行完整分析
    python main.py --config custom_config.yaml  # 使用自定义配置
"""

import argparse
import os
import sys
from pathlib import Path

# 将当前脚本目录加入 Python 路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from rewards import create_rewards_from_config
from utils import load_config, ensure_output_dir, generate_scenario_data, compute_total_reward
from visualizer import plot_reward_analysis, plot_parameter_comparison


def cmd_analyze(args, config):
    """执行奖励函数分析"""
    print("\n>>> 执行奖励函数分析...")
    
    # 创建奖励函数实例
    rewards = create_rewards_from_config(config)
    
    # 设置输出目录
    viz_cfg = config.get('visualization', {})
    output_dir = viz_cfg.get('output_dir', 'outputs')
    output_dir = ensure_output_dir(SCRIPT_DIR / output_dir)
    
    # 绘制综合分析图
    print("  绘制奖励函数综合分析图...")
    plot_reward_analysis(
        rewards, 
        config, 
        str(output_dir / 'reward_func_analysis.png')
    )
    
    # 绘制参数对比图
    print("  绘制参数对比图...")
    from rewards import SpeedReward, DistanceReward
    
    plot_parameter_comparison(
        SpeedReward, 'target_speed', [20.0, 25.0, 30.0],
        {'tolerance': 5.0},
        str(output_dir / 'speed_reward_comparison.png'),
        xlabel='Speed (m/s)'
    )
    
    plot_parameter_comparison(
        DistanceReward, 'safe_distance', [10.0, 15.0, 20.0],
        {'critical_distance': 5.0},
        str(output_dir / 'distance_reward_comparison.png'),
        xlabel='Distance (m)'
    )
    
    print(f"\n  分析完成！输出目录: {output_dir}")


def cmd_simulate(args, config):
    """执行批量仿真"""
    print("\n>>> 执行批量仿真...")
    
    rewards = create_rewards_from_config(config)
    
    # 生成场景数据
    print("  生成模拟场景数据...")
    scenario_data = generate_scenario_data(num_samples=1000)
    
    # 计算奖励
    print("  计算奖励...")
    reward_results = compute_total_reward(rewards, scenario_data)
    
    # 输出统计信息
    print("\n  奖励统计:")
    print(f"    速度奖励:   mean={reward_results['speed_reward'].mean():.3f}, "
          f"std={reward_results['speed_reward'].std():.3f}")
    print(f"    距离奖励:   mean={reward_results['distance_reward'].mean():.3f}, "
          f"std={reward_results['distance_reward'].std():.3f}")
    print(f"    舒适性奖励: mean={reward_results['comfort_reward'].mean():.3f}, "
          f"std={reward_results['comfort_reward'].std():.3f}")
    print(f"    总奖励:     mean={reward_results['total_reward'].mean():.3f}, "
          f"std={reward_results['total_reward'].std():.3f}")


def cmd_all(args, config):
    """运行完整流水线"""
    print("\n" + "=" * 60)
    print("  自动驾驶奖励函数分析 - 完整流水线")
    print("=" * 60)
    
    cmd_analyze(args, config)
    cmd_simulate(args, config)
    
    print("\n" + "=" * 60)
    print("  全部流程已完成!")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="自动驾驶奖励函数分析系统 - 主入口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
命令列表:
  analyze    绘制奖励函数分析图
  simulate   执行批量仿真并输出统计
  all        完整流水线（默认）

示例:
  python main.py
  python main.py analyze
  python main.py simulate
        """,
    )
    
    parser.add_argument("command", nargs="?", default="all",
                        choices=["analyze", "simulate", "all"],
                        help="要执行的命令")
    parser.add_argument("--config", type=str, default="config.yaml",
                        help="配置文件路径")
    
    args = parser.parse_args()
    
    # 切换工作目录
    os.chdir(SCRIPT_DIR)
    
    # 加载配置
    config = load_config(args.config)
    
    # 分发命令
    commands = {
        "analyze": cmd_analyze,
        "simulate": cmd_simulate,
        "all": cmd_all,
    }
    
    commands[args.command](args, config)


if __name__ == "__main__":
    main()
