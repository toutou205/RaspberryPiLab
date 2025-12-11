# Project TODOs

## High Priority

- [ ] **Log Format Enhancement**
  - **Objective**: Include system state context in data logs.
  - **Files to Modify**: `src/core/logger.py`, `src/core/background_thread.py`.
  - **Status**:
    - [x] Hardware Driver Support (`sense_driver.py`: `last_joystick_event`)
    - [x] Display Support (`display.py`: `current_mode`)
    - [x] Logger Implementation (CSV Header & Row Data)
    - [x] Background Thread Integration (Passing data to logger)
  - **Requirements**:
    - Add **Joystick Action Status** (Direction, Action Type) to the CSV/Log output.
    - Add **Current LED Display Mode** (Mode ID/Name) to the CSV/Log output.
  - **Dependencies**: Use `SenseHatWrapper.last_joystick_event` and `LEDDisplay.current_mode`.