git add .
git commit -m "refactor(core, hardware): Improve code quality and configuration

- **config.py**:
  - Centralized joystick direction strings into `JOYSTICK_DIRECTIONS`.
  - Added `MODE_DISPLAY_COLOR` and `MODE_DISPLAY_DURATION` for LED feedback.

- **core/background_thread.py**:
  - Replaced hardcoded values with constants from `config`.
  - Added comprehensive Google-style docstrings to all methods.

- **hardware/sense_driver.py**:
  - Added complete Google-style docstrings for all public methods.
  - Aligned mock data generation with default values from `config`.

---

重构(core, hardware): 提高代码质量并优化配置

- **config.py**:
  - 将摇杆方向字符串集中到 `JOYSTICK_DIRECTIONS`。
  - 为 LED 反馈添加 `MODE_DISPLAY_COLOR` 和 `MODE_DISPLAY_DURATION`。

- **core/background_thread.py**:
  - 使用 `config` 中的常量替换硬编码值。
  - 为所有方法添加了完整的 Google 风格文档字符串。

- **hardware/sense_driver.py**:
  - 为所有公共方法添加了完整的 Google 风格文档字符串。
  - 使模拟数据生成与 `config` 中的默认值保持一致。
"
# 请用户确认无误后手动执行推送
# git push origin main
