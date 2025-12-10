import csv
import os
from datetime import datetime

class DataRecorder:
    """处理传感器数据到 CSV 文件的记录。"""
    def __init__(self, folder='recordings'):
        self.is_recording = False
        self.file_path = None
        self.csv_writer = None
        self.file = None
        self.recordings_folder = folder
        if not os.path.exists(self.recordings_folder):
            os.makedirs(self.recordings_folder)

    def start(self):
        """开始记录，创建一个带时间戳的新文件。"""
        if self.is_recording:
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file_path = os.path.join(self.recordings_folder, f"sensordata_{timestamp}.csv")
        self.file = open(self.file_path, 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.file)
        # 写入表头
        self.csv_writer.writerow(['timestamp', 'temp', 'humidity', 'pressure', 'altitude', 'pitch', 'roll', 'yaw'])
        self.is_recording = True

    def stop(self):
        """停止记录并关闭文件。"""
        if self.file:
            self.file.close()
        self.is_recording = False
        self.file = None
        self.csv_writer = None

    def record(self, data_packet):
        """将一个数据包写入 CSV 文件。"""
        if not self.is_recording or not self.csv_writer:
            return
        
        env = data_packet['env']
        imu = data_packet['imu']
        timestamp = datetime.now().isoformat()
        
        self.csv_writer.writerow([
            timestamp,
            env.get('temp', ''),
            env.get('humidity', ''),
            env.get('pressure', ''),
            env.get('altitude', ''),
            imu.get('pitch', ''),
            imu.get('roll', ''),
            imu.get('yaw', '')
        ])