
# Sense HAT Web Dashboard

## 描述

该项目是一个基于 Raspberry Pi 和 Sense HAT 的实时环境与姿态监控系统。它通过一个 Web 仪表盘展示来自 Sense HAT 的传感器数据，包括温度、湿度、气压、姿态角以及计算出的海拔高度。用户可以通过网页实时查看数据，并控制是否将这些数据记录到本地 CSV 文件中。同时，它也支持通过物理摇杆切换 LED 矩阵的显示模式。

## 主要功能

- **实时数据监控**: 通过 WebSockets 将传感器数据实时推送到前端仪表盘。
- **环境数据显示**:
  - 温度 (Temperature), 湿度 (Humidity), 气压 (Pressure), 海拔高度 (Altitude)。
- **姿态数据显示 (IMU)**: 俯仰角 (Pitch), 横滚角 (Roll), 航向角 (Yaw)。
- **数据记录**: 用户可以通过网页上的开关控制数据的记录，数据以 CSV 格式保存在 `recordings` 目录下。
- **多模式 LED 反馈**: Sense HAT 上的 8x8 LED 矩阵可通过物理摇杆切换多种显示模式（如监控、水平仪、彩虹、火焰等）。
- **Web 界面**: 使用 Flask 和 Socket.IO 构建后端，前端采用 HTML, Bootstrap 5, 和 JavaScript 实现。
- **模拟模式**: 在没有 Sense HAT 硬件的环境下也能运行，并生成模拟数据用于调试。

## 文件结构

```
SenseHATWebDashboard/
├── .cursorrules            # AI 编码规则
├── .gitignore              # Git 忽略文件配置
├── README.md               # 项目说明文档
├── requirements.txt        # Python 依赖库列表
├── run.py                  # 应用主入口 (初始化并运行 Flask)
│
├─docs/                     # 项目文档 (PRD, 技术规格等)
│  ├── PRD.md
│  └── TECH_SPEC.md
│
├─logs/                     # 存放 CSV 数据记录文件 (运行时生成)
│
├─reference/                # 原始参考代码 (已重构)
│  └── templates/
│
├─src/                      # 核心源代码
│  ├── config.py            # 配置文件
│  ├─core/
│  │  ├── calculator.py     # 业务逻辑计算 (如海拔)
│  │  └── logger.py         # 数据记录核心模块
│  ├─hardware/
│  │  ├── sense_driver.py   # Sense HAT 硬件驱动封装
│  │  └── display.py        # LED 矩阵显示逻辑
│  └─web/
│     ├── routes.py         # Flask 路由定义
│     └── socket_handler.py # Socket.IO 事件处理
│
└─web_client/               # Flask 前端文件
    ├─static/
    │  └─css/               # 自定义样式表
    └─templates/
        └── index.html      # 主页面模板
```

## 技术栈

- **硬件**:
  - Raspberry Pi (3B or newer recommended)
  - Sense HAT
- **后端**:
  - Python
  - Flask
  - Flask-SocketIO
- **前端**:
  - HTML5
  - Bootstrap 5
  - JavaScript
  - Socket.IO Client
- **Python 库**:
  - `sense-hat`

## 如何运行

1. **准备文件**:
   将项目文件放置在树莓派的某个目录下。

2. **安装依赖**:
   在项目根目录下，使用 `pip` 安装所有必要的库。
   ```bash
   pip install -r requirements.txt
   ```

3. **运行应用**:
   确保您在项目根目录下，然后运行 `app.py`。
   ```bash
   python3 app.py
   ```

4. **访问仪表盘**:
   在同一局域网下的任何设备上，打开浏览器并访问 `http://<你的树莓派IP地址>:5000` 即可看到实时数据。
   您可以在树莓派终端中使用 `hostname -I` 命令来查找其 IP 地址。
