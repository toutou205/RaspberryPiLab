# Sense HAT Web Dashboard 项目需求

## V1.0 核心功能

- [x] **Web 仪表盘**: 使用 Flask 和 Socket.IO 创建一个实时网页，展示传感器数据。
- [x] **环境数据显示**:
    - [x] 温度 (Temperature)
    - [x] 湿度 (Humidity)
    - [x] 气压 (Pressure)
    - [x] 海拔高度 (Altitude) - *新功能*
- [x] **IMU 姿态数据显示**:
    - [x] 俯仰角 (Pitch)
    - [x] 横滚角 (Roll)
    - [x] 航向角 (Yaw)
- [x] **LED 矩阵多模式控制**:
    - [x] 模式切换功能 (通过摇杆和 Web UI)。
    - [x] 实现多种动态效果 (监控、水平仪、彩虹、火焰)。
    - [x] LED 矩阵开关控制。
- [x] **数据记录**:
    - [x] 在网页上提供“开始/停止记录”按钮。
    - [x] 将传感器数据实时记录到服务器端的 CSV 文件中。