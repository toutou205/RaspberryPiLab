import time
import math
import random

# --- Constants ---
MODES = [
    {"id": 0, "name": "Monitor Mode", "desc": "显示静态状态指示灯"},
    {"id": 1, "name": "Spirit Level", "desc": "水平仪 (姿态可视化)"},
    {"id": 2, "name": "Rainbow Wave", "desc": "动态彩虹波浪"},
    {"id": 3, "name": "Fire Effect", "desc": "随机火焰粒子"}
]

# --- Helper Function ---
def clamp(value, min_value=0, max_value=7):
    """
    将数值限制在指定的范围内
    """
    return max(min_value, min(value, max_value))

class LEDDisplay:
    """
    管理Sense HAT 8x8 LED矩阵的显示。
    """
    def __init__(self, sense, initial_mode=0):
        self.sense = sense
        self.current_mode = initial_mode
        self.last_mode = initial_mode
        self.is_on = True
        self.sense.clear()

    def set_mode(self, mode_id):
        """
        设置当前的显示模式。
        """
        self.last_mode = self.current_mode
        self.current_mode = mode_id
        if self.current_mode != self.last_mode:
            time.sleep(0.5)

    def toggle_power(self):
        """
        切换LED显示屏的开关状态。
        """
        self.is_on = not self.is_on

    def draw_leds(self, pitch, roll, yaw):
        """
        根据当前模式更新 LED 矩阵的显示。
        """
        if self.current_mode != self.last_mode:
            self.sense.clear()
            self.last_mode = self.current_mode
            
        if not self.is_on:
            self.sense.clear()
            return

        # 模式 0: 监控模式 (简单的呼吸灯)
        if self.current_mode == 0:
            t = time.time()
            intensity = int(150 + 100 * math.sin(t * 3))
            color = (0, intensity, 0)
            self.sense.clear()
            self.sense.set_pixel(3, 3, color)
            self.sense.set_pixel(3, 4, color)
            self.sense.set_pixel(4, 3, color)
            self.sense.set_pixel(4, 4, color)

        # 模式 1: 水平仪
        elif self.current_mode == 1:
            self.sense.clear()
            y = int(3.5 + (roll / 20.0) * 3.5)
            x = int(3.5 + (-pitch / 20.0) * 3.5)
            target_x, target_y = clamp(x), clamp(y)
            col = (0, 255, 0) if (3 <= target_x <= 4 and 3 <= target_y <= 4) else (255, 0, 0)
            self.sense.set_pixel(target_x, target_y, col)

        # 模式 2: 彩虹波浪
        elif self.current_mode == 2:
            pixels = []
            t = time.time() * 2
            for i in range(64):
                x = i % 8
                y = i // 8
                r = int(128 + 127 * math.sin(x/2.0 + t))
                g = int(128 + 127 * math.sin(y/2.0 + t))
                b = int(128 + 127 * math.sin((x+y)/2.0 + t))
                pixels.append((r, g, b))
            self.sense.set_pixels(pixels)

        # 模式 3: 火焰效果
        elif self.current_mode == 3:
            pixels = []
            for i in range(64):
                r = random.randint(150, 255)
                g = random.randint(0, 100)
                pixels.append((r, g, 0))
            self.sense.set_pixels(pixels)
