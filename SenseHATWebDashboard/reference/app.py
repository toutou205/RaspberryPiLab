import time
import threading
import math
import random
from flask import Flask, render_template
from flask_socketio import SocketIO
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD

# --- 初始化 ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sense_secret'
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')
sense = SenseHat()

# --- 全局状态变量 ---
current_mode = 0  # 0: Monitor, 1: Spirit Level, 2: Rainbow, 3: Fire
last_mode = 0
brightness = 255  # 亮度 0-255 (Sense HAT底层通常支持低光和高光)
is_on = True      # 开关状态

MODES = [
    {"id": 0, "name": "Monitor Mode", "desc": "显示静态状态指示灯"},
    {"id": 1, "name": "Spirit Level", "desc": "水平仪 (姿态可视化)"},
    {"id": 2, "name": "Rainbow Wave", "desc": "动态彩虹波浪"},
    {"id": 3, "name": "Fire Effect", "desc": "随机火焰粒子"}
]

# --- 辅助函数：限制数值范围 ---
def clamp(value, min_value=0, max_value=7):
    return max(min_value, min(value, max_value))

# --- LED 模式逻辑 ---
def draw_leds(pitch, roll, yaw):
    global current_mode, is_on, last_mode
    
    if current_mode != last_mode:
        time.sleep(0.5)
        last_mode = current_mode
        
    
    if not is_on:
        sense.clear()
        return

    # 模式 0: 监控模式 (简单的呼吸灯)
    if current_mode == 0:
        t = time.time()
        # 绿色呼吸效果
        intensity = int(150 + 100 * math.sin(t * 3))
        color = (0, intensity, 0)
        
        # 清屏并设置中心 2x2 为呼吸色
        sense.clear()
        sense.set_pixel(3, 3, color)
        sense.set_pixel(3, 4, color)
        sense.set_pixel(4, 3, color)
        sense.set_pixel(4, 4, color)

    # 模式 1: 水平仪 (利用 Pitch/Roll 移动光点)
    elif current_mode == 1:
        sense.clear()
        # 将角度映射到 0-7 的坐标
        # 假设 +/- 20度 为满量程
        y = int(3.5 + (roll / 20.0) * 3.5)
        x = int(3.5 + (-pitch / 20.0) * 3.5)
        
        target_x = clamp(x)
        target_y = clamp(y)
        
        # 如果平稳，显示绿色；倾斜显示红色
        col = (0, 255, 0) if (3 <= target_x <= 4 and 3 <= target_y <= 4) else (255, 0, 0)
        sense.set_pixel(target_x, target_y, col)

    # 模式 2: 彩虹波浪 (动态算法)
    elif current_mode == 2:
        pixels = []
        t = time.time() * 2
        for i in range(64):
            x = i % 8
            y = i // 8
            # 根据坐标和时间生成颜色
            r = int(128 + 127 * math.sin(x/2.0 + t))
            g = int(128 + 127 * math.sin(y/2.0 + t))
            b = int(128 + 127 * math.sin((x+y)/2.0 + t))
            pixels.append((r, g, b))
        sense.set_pixels(pixels)

    # 模式 3: 火焰效果 (随机动态)
    elif current_mode == 3:
        pixels = []
        for i in range(64):
            # 随机生成红橙色调
            r = random.randint(150, 255)
            g = random.randint(0, 100)
            pixels.append((r, g, 0))
        sense.set_pixels(pixels)

# --- 背景任务：主循环 (读取传感器 + 更新LED) ---
def background_thread():
    print("后台传感器线程已启动...")
    while True:
        # 1. 读取环境数据
        temp = sense.get_temperature()
        humidity = sense.get_humidity()
        pressure = sense.get_pressure()
        
        # 2. 读取 IMU 数据
        orientation = sense.get_orientation()
        pitch = orientation['pitch']
        roll = orientation['roll']
        yaw = orientation['yaw']
        
        # 修正 Pitch/Roll (SenseHAT 的范围是 0-360，我们需要 -180 到 180 便于计算)
        if pitch > 180: pitch -= 360
        if roll > 180: roll -= 360

        # 3. 更新 LED 显示
        draw_leds(pitch, roll, yaw)

        # 4. 打包数据发送给网页
        data_packet = {
            'env': {
                'temp': round(temp, 1),
                'humidity': round(humidity, 1),
                'pressure': round(pressure, 1)
            },
            'imu': {
                'pitch': round(pitch, 1),
                'roll': round(roll, 1),
                'yaw': round(yaw, 1)
            },
            'sys': {
                'mode_id': current_mode,
                'mode_name': MODES[current_mode]['name'],
                'is_on': is_on
            }
        }
        socketio.emit('sensor_update', data_packet)

        # 控制频率 20Hz
        time.sleep(0.05)

# --- 摇杆事件处理 ---
def joystick_listener():
    while True:
        for event in sense.stick.get_events():
            if event.action in (ACTION_PRESSED, ACTION_HELD):
                global current_mode, is_on, brightness
                
                if event.direction == "left":
                    current_mode = (current_mode - 1) % len(MODES)
                    sense.show_letter(str(current_mode), text_colour=[0,0,255]) # 临时显示模式号
                    time.sleep(0.5)
                
                elif event.direction == "right":
                    current_mode = (current_mode + 1) % len(MODES)
                    sense.show_letter(str(current_mode), text_colour=[0,0,255])
                    time.sleep(0.5)
                
                elif event.direction == "up":
                    sense.low_light = False
                
                elif event.direction == "down":
                    sense.low_light = True
                
                elif event.direction == "middle":
                    is_on = not is_on
                    
        time.sleep(0.1)

# --- 启动线程 ---
t_bg = threading.Thread(target=background_thread)
t_bg.daemon = True
t_bg.start()

t_joy = threading.Thread(target=joystick_listener)
t_joy.daemon = True
t_joy.start()

# --- 路由 ---
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # 确保 Sense HAT 初始化
    sense.clear()
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)