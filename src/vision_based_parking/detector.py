import cv2
import numpy as np

class ParkingDetector:
    def __init__(self, config=None):
        self.config = config or {}

    def capture_frame(self, world, vehicle):
        # TODO: 使用 CARLA 摄像头传感器获取实际图像
        width = self.config.get('simulation', {}).get('width', 800)
        height = self.config.get('simulation', {}).get('height', 600)
        return np.zeros((height, width, 3), dtype=np.uint8)

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(
            gray,
            self.config.get('vision', {}).get('canny_thresh1', 50),
            self.config.get('vision', {}).get('canny_thresh2', 150)
        )
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi / 180,
            threshold=50,
            minLineLength=50,
            maxLineGap=10
        )

        target_x = None
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            target_x = frame.shape[1] // 2
            cv2.circle(frame, (target_x, frame.shape[0] // 2), 8, (0, 0, 255), -1)
            cv2.putText(frame, '目标车位', (target_x - 60, frame.shape[0] // 2 - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        return frame, target_x
