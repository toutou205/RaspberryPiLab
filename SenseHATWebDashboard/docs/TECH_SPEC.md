# Technical Specification

## 1. 系统架构
采用分层架构：
- **Hardware Layer (`src/hardware`)**: 封装 `sense_hat` 库，提供线程安全的 `get_readings()` 和 `set_pixels()` 方法。
- **Core Layer (`src/core`)**:
    - `DataManager`: 聚合原始数据，调用 `calculate_altitude`，管理 `CsvLogger` 的状态。
    - `CsvLogger`: 负责文件 I/O，使用 Python `csv` 模块，追加写入模式。
- **Web Layer (`src/web`)**: Flask 提供静态页面，SocketIO 负责双向通信（推数据，收录制指令）。

## 2. 数据结构

### 2.1 WebSocket Payload (Server -> Client)
```json
{
  "env": {
    "temp": 25.4,
    "humidity": 45.2,
    "pressure": 1013.2,
    "altitude": 45.0  // [New]
  },
  "imu": { "pitch": 10.1, "roll": -2.3, "yaw": 180.0 },
  "sys": {
    "mode_id": 1,
    "mode_name": "Spirit Level",
    "is_on": true,
    "is_recording": false // [New] 录制状态回显
  }
}