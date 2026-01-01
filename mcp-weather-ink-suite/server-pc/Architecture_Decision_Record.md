# 🏛️ 架构决策记录 (Architecture Decision Record - ADR)

## 📌 决策背景 (Context)
在项目初期，我们面临两种技术路线的选择：

*   **方案 A (All-in-Pi)**: 将树莓派作为一个独立的、全功能的 MCP Server。它直接连接 OpenMeteo/AQICN，直接调用 Gemini，直接驱动屏幕。PC 端的 Cursor 只是远程连接它。
*   **方案 B (Local Hub / Remote Render)**: 即当前方案。PC 端运行核心 MCP Server，负责所有数据处理；树莓派退化为一个“哑终端”渲染器，只接收最终指令。

---

## 🧐 为什么选择方案 B？(Why we chose this path)

我们选择 **方案 B** 并非偶然，而是基于以下 4 个核心痛点的深思熟虑：

### 1. 网络环境的巨大差异 (Network Constraints)
*   **痛点**: 获取 AQI 数据和调用 Google Gemini API 都需要科学稳定的网络环境。
*   **Pi 的困境**: 在树莓派（尤其是 headless server）上配置和维护稳定的系统级代理（Proxy）非常繁琐，且容易失效。
*   **PC 的优势**: 您的 Windows 开发机拥有成熟、稳定的网络环境和代理工具。
*   **决策**: 让网络好的机器去干联网的事，Pi 只负责局域网通信，稳定性提升 10 倍。

### 2. 算力与响应速度 (Performance)
*   **痛点**: Pi Zero 2W 的单核性能有限。OpenMeteo + AQICN + Gemini 三个并发请求 + JSON 处理 + 墨水屏驱动，虽然能跑，但会显著增加延迟。
*   **决策**: PC 的算力是过剩的。将数据聚合、JSON Schema 校验、AI 推理全部放在毫秒级响应的 PC 上，Pi 拿到数据 0.1秒 解析即刻刷新，用户体验极佳。

### 3. 开发与调试效率 (DevEx)
*   **痛点**: "All-in-Pi" 意味着每次改代码都要：`修改 -> 部署(SCP) -> 重启服务 -> 查看远程日志`。调试周期极长。
*   **决策**: 在 Local Server 模式下，您可以在 Cursor 中直接修改 `main.py`，秒级热重载，打断点调试。只有最后涉及“画图”的那 5% 代码需在 Pi 上，其余 95% 的业务逻辑都在本地闭环。

### 4. 避免 "双重 MCP" 困扰 (Complexity)
*   **背景**: 如果 Pi 是独立 Server，您的 Cursor 就需要同时配置 `Local Weather Server` (可能用于其他) 和 `Remote Pi Server`。这会让 AI 困惑：“我该调用哪个工具去查天气？”
*   **决策**: 将功能合并到一个 Local Server。AI 只需要面对一个工具 `update_remote_display`，逻辑路径最短，出错率最低。

---

## ⚖️ 优缺点总结 (Pros & Cons)

| 特性 | 方案 A (All-in-Pi) | 方案 B (当前方案: Local Hub) |
| :--- | :--- | :--- |
| **网络依赖** | 高 (Pi 必须能访问外网) | **低** (Pi 只需局域网连接 PC) |
| **调试难度** | 困难 (远程调试) | **极低** (本地调试) |
| **部署维护** | 繁琐 (需维护 Pi 上的 Python 环境) | **简单** (Pi 环境几乎冻结，不需常改) |
| **响应速度** | 慢 (受限于 Pi CPU) | **快** (PC 预处理) |
| **自主性** | 高 (Pi 离线也能工作) | 低 (必须依赖 PC 发号施令) |

### 🔍 结论
既然我们的场景是 **"桌面助手" (Desktop Companion)**，PC 始终在线是前提。因此，牺牲一点 Pi 的自主性，换取 **开发效率、网络稳定性、运行速度** 的全面提升，是绝对正确的工程选择。
