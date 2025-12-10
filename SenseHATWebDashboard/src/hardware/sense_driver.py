# -*- coding: utf-8 -*-
from sense_hat import SenseHat

class SenseHatWrapper:
    """
    Sense HAT 硬件的封装类，用于简化硬件交互。
    这个版本专注于读取传感器数据。
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SenseHatWrapper, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        初始化 Sense HAT。
        """
        if hasattr(self, '_initialized') and self._initialized:
            return
            
        try:
            self.sense = SenseHat()
            self._initialized = True
            self.sense.clear()
        except OSError as e:
            print(f"无法初始化Sense HAT: {e}. 将使用模拟数据。")
            self.sense = None
            self._initialized = True


    def get_temperature(self):
        if not self.sense:
            return 25.0
        return self.sense.get_temperature()

    def get_pressure(self):
        if not self.sense:
            return 1013.25
        return self.sense.get_pressure()

    def get_humidity(self):
        if not self.sense:
            return 45.0
        return self.sense.get_humidity()

    def get_orientation(self):
        """
        读取IMU数据 (pitch, roll, yaw)。
        返回规范化到-180到180度的值。
        """
        if not self.sense:
            return {'pitch': 0, 'roll': 0, 'yaw': 0}

        orientation = self.sense.get_orientation()
        pitch = orientation['pitch']
        roll = orientation['roll']
        yaw = orientation['yaw']
        
        if pitch > 180: pitch -= 360
        if roll > 180: roll -= 360
        
        return {
            'pitch': round(pitch, 1),
            'roll': round(roll, 1),
            'yaw': round(yaw, 1)
        }

    def set_low_light(self, is_low):
        """
        设置低光模式。
        """
        if self.sense:
            self.sense.low_light = is_low