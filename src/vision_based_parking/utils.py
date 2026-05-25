import cv2

def draw_text(frame, text, position=(20, 30), color=(255, 255, 255), scale=0.7, thickness=2):
    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))
