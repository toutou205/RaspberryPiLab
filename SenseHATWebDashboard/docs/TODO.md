# Project TODOs / 项目待办事项

## High Priority / 高优先级

- [x] **Log Format Enhancement / 日志格式增强**
  - **Objective**: Include system state context in data logs.
  - **目标**: 在数据日志中包含系统状态上下文。
  - **Files to Modify**: `src/core/logger.py`, `src/core/background_thread.py`.
  - **修改文件**: `src/core/logger.py`, `src/core/background_thread.py`.
  - **Status / 状态**:
    - [x] Hardware Driver Support (`sense_driver.py`: `last_joystick_event`) / 硬件驱动支持
    - [x] Display Support (`display.py`: `current_mode`) / 显示支持
    - [x] Logger Implementation (CSV Header & Row Data) / 日志实现（CSV 表头及行数据）
    - [x] Background Thread Integration (Passing data to logger) / 后台线程集成（传递数据至日志）
  - **Requirements / 需求**:
    - Add **Joystick Action Status** (Direction, Action Type) to the CSV/Log output.
    - 在 CSV/日志输出中增加 **摇杆动作状态**（方向、动作类型）。
    - Add **Current LED Display Mode** (Mode ID/Name) to the CSV/Log output.
    - 在 CSV/日志输出中增加 **当前 LED 显示模式**（模式 ID/名称）。
  - **Dependencies / 依赖**: Use `SenseHatWrapper.last_joystick_event` and `LEDDisplay.current_mode`.