# main_parking_ctrl.py

class PIDController:
    def __init__(self, kp, kd):
        self.kp = kp
        self.kd = kd
        self.prev_error = 0

    def update(self, error):
        """
        根据误差计算控制量
        """
        # 简单的 PD 控制
        derivative = error - self.prev_error
        output = self.kp * error + self.kd * derivative
        self.prev_error = error
        return output

class ParkingController:
    def __init__(self, config):
        self.steering_pid = PIDController(config['controller']['kp'], config['controller']['kd'])
        self.max_steering = config['controller']['max_steering_angle']

    def compute_action(self, car_x, target_x):
        """
        输入: 车辆当前x坐标, 目标x坐标
        输出: 转向角 (-45 到 45)
        """
        if target_x is None:
            return 0 # 没看到车位就不动

        error = target_x - car_x
        
        # 使用 PID 计算转向
        steering = self.steering_pid.update(error)
        
        # 限制最大角度
        steering = max(-self.max_steering, min(self.max_steering, steering))
        
        return steering