# TODO List

- [x] **项目初始化**: 创建文件结构，安装依赖。
- [x] **模块拆分**:
    - [x] 将 `app.py` 中的 Sense HAT 初始化代码移至 `src/hardware/sense_driver.py`。
    - [x] 将 LED 绘制逻辑 (`draw_leds`) 移至 `src/hardware/display.py`。
- [x] **功能升级**:
    - [x] 实现高度计算函数 (`src/core/calculator.py`)。
    - [x] 实现 CSV 记录器类 (`src/core/logger.py`)。
- [x] **Web 重构**:
    - [x] 修改 `web_client/index.html`，增加“录制”开关和高度显示面板。
    - [x] 编写 Flask SocketIO 逻辑以支持前端控制录制开关。
- [ ] **集成测试**: 联调硬件与网页，确保所有功能正常工作。
- [ ] **文档完善**: 更新 `README.md`，说明如何运行项目。