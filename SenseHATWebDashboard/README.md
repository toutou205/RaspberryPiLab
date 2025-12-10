
# Sense HAT Web Dashboard

## 描述

该项目是一个基于 Raspberry Pi 和 Sense HAT 的实时环境监控系统。它通过一个 Web 仪表盘展示来自 Sense HAT 的传感器数据，包括温度、湿度、压力和计算出的海拔高度。用户可以通过网页实时查看数据，并控制是否将这些数据记录到本地 CSV 文件中。

## 主要功能

- **实时数据监控**: 通过 WebSockets 将传感器数据实时推送到前端仪表盘。
- **环境数据显示**:
  - 温度 (Temperature)
  - 湿度 (Humidity)
  - 气压 (Pressure)
  - 海拔高度 (Altitude) - 根据实时气压计算得出。
- **数据记录**: 用户可以通过网页上的开关控制数据的记录，数据以 CSV 格式保存在 `logs` 目录下。
- **LED 反馈**: Sense HAT 上的 8x8 LED 矩阵会根据当前数据显示不同的颜色模式（例如，温度越高，颜色越偏暖色调）。
- **Web 界面**: 使用 Flask 和 Socket.IO 构建后端，前端采用 HTML、CSS 和 JavaScript 实现，界面简洁直观。

## 技术栈

- **硬件**:
  - Raspberry Pi (3B or newer recommended)
  - Sense HAT
- **后端**:
  - Python
  - Flask
  - Flask-SocketIO
  - eventlet
- **前端**:
  - HTML5
  - JavaScript
  - Socket.IO Client
- **Python 库**:
  - `sense-hat` (或 `sense-emu` 用于模拟)

## 如何运行

1. **克隆仓库**:
   ```bash
   git clone <repository-url>
   cd sense_project
   ```

2. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

3. **运行应用**:
   ```bash
   python run.py
   ```

4. **访问仪表盘**:
   在浏览器中打开 `http://<your-raspberry-pi-ip>:5000` 即可看到实时数据。

