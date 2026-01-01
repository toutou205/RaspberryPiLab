# 🌉 跨系统协作机制：Local Server 与 Raspberry Pi 的协同

本文档详细解析 **Local MCP Server** (`mcp-weather-air-info-server`) 如何指挥 **Legacy Pi Code** (`project_root_mcp_old`) 完成远程显示任务。

---

## 1. 宏观框架图 (System Context)

整个系统由 "控制端" (PC) 和 "执行端" (Pi) 组成，通过 SSH 隧道连接。

```mermaid
graph LR
    subgraph "Local PC (Windows)"
        User[用户/Cursor]
        LocalServer[MCP Weather Server]
        TempFile[temp_payload.json]
    end

    subgraph "Connection"
        SSH[SSH Tunnel]
        SCP[SCP File Transfer]
    end

    subgraph "Raspberry Pi (Zero 2W)"
        ShellScript[run_mcp_server.sh]
        LegacyMCP[Legacy MCP Server (Python)]
        Driver[E-Ink Driver (epd2in7b)]
        Hardware[2.64inch E-ink Screen]
    end

    User -->|Call Tool| LocalServer
    LocalServer -->|Generate| TempFile
    TempFile -->|Upload| SCP
    LocalServer -->|Execute cmd| SSH
    SSH -->|Trigger| ShellScript
    SCP -->|File| ShellScript
    ShellScript -->|Pipe Input| LegacyMCP
    LegacyMCP -->|Draw| Driver
    Driver -->|SPI| Hardware
```

---

## 2. 详细泳道图 (Swimlane Flowchart)

展示数据如何在两个系统间流转。**关键点**在于 Local Server 将复杂的数据获取任务全部承包，只给 Pi 发送**最终结果**。

```mermaid
sequenceDiagram
    participant User as 👤 用户 (Cursor)
    participant PC as 💻 Local Server (PC)
    participant Pi as 🍓 Raspberry Pi
    participant Screen as 📺 E-ink Screen

    User->>PC: update_remote_display("Dali")
    
    rect rgb(200, 220, 250)
    Note over PC: 1. 数据聚合阶段
    PC->>PC: Fetch Weather (OpenMeteo)
    PC->>PC: Fetch AQI (AQICN)
    PC->>PC: Generate Advice (Gemini)
    PC->>PC: 组装 JSON Payload ("3-Step Handshake")
    end

    rect rgb(220, 250, 220)
    Note over PC, Pi: 2. 传输与执行阶段
    PC->>Pi: SCP 上传 JSON 文件 (mcp_request.json)
    PC->>Pi: SSH 执行 "pkill python; cat json | run.sh"
    end

    rect rgb(250, 220, 200)
    Note over Pi: 3. 渲染阶段
    Pi->>Pi: run_mcp_server.sh 激活环境
    Pi->>Pi: Legacy MCP读取 STDIN (JSON)
    Pi->>Pi: 解析 Tool Call: display_weather_info
    Pi->>Screen: 绘制 UI & 刷新屏幕
    end

    Pi-->>PC: 返回日志 "Successfully displayed"
    PC-->>User: ✅ 操作成功
```

---

## 3. 树莓派端运作机制 (Pi Execution Mechanism)

树莓派端的 `project_root_mcp_old` 虽然被称为 "Old"，但它现在扮演着 **Rendering Engine (渲染引擎)** 的核心角色。

### 3.1 核心脚本: `run_mcp_server.sh`
```bash
#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/home/alex/mcp-server/src
cd /home/alex/mcp-server
# 关键：从标准输入读取数据，喂给 Python 脚本
uv run src/main.py
```
这个脚本确保了 Python 环境正确，并且能够接收通过管道传来的 JSON 数据。

### 3.2 遗留代码的妙用
Local Server 并没有在 Pi 上重新写一套代码，而是直接利用了 Pi 上**已经部署好的、符合 MCP 协议的**旧代码。
*   **输入**: Local Server 伪造了一个标准的 MCP "Call Tool" 请求。
*   **处理**: Pi 上的旧代码以为是 Cursor 发来的请求，于是照常处理。
*   **结果**: 屏幕刷新。

这种设计极其巧妙地复用了现有资源，**无需在 Pi 上安装新的依赖或服务**，真正做到了 "无侵入式" 升级。
