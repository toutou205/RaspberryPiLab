# 🌦️ MCP Weather & Air Info Server - 系统复盘与知识梳理

`mcp-weather-air-info-server` 是一个功能强大的**数据聚合与远程控制中枢**。它不仅仅是一个天气查询工具，更是一个打通了“公网数据”到“局域网硬件”的完整解决方案。

---

## 1. 核心功能 (Features)
1.  **多源数据聚合**: 并行拉取 OpenMeteo (天气) 和 AQICN (空气质量) 数据。
2.  **智能建议 (AI Advisor)**:
    *   **Direct API 模式 (推荐)**: 调用 Google Gemini API 直接生成健康建议。
    *   **Sampling 模式**: 尝试请求 Claude 客户端生成建议 (Experimental)。
3.  **智能纠错 (Robustness)**: 支持中文输入（如“大理”），自动纠正拼写错误或模糊查询（“smart fallback”机制）。
4.  **远程硬件控制**: 一键通过 MCP 协议唤醒树莓派，即时刷新 E-ink 墨水屏。

---

## 2. 系统架构 (Architecture)
采用了经典的**分层架构 (Layered Architecture)**，各司其职，低耦合。

```mermaid
graph TD
    User[用户/AI] -->|MCP Protocol| Main[Main Entry (main.py)]
    
    subgraph "Application Layer"
        Main --> Tool1[Tool: get_full_weather_report]
        Main --> Tool2[Tool: update_remote_display]
    end

    subgraph "Service Layer (业务逻辑)"
        Tool1 & Tool2 --> Aggregator[Aggregator Service]
        Tool1 & Tool2 --> Processor[Processor Service]
        Tool1 & Tool2 --> Advisor[Advisor Service]
        Tool1 & Tool2 --> Normalizer[Normalizer Service]
    end

    subgraph "Client Layer (外部接口)"
        Aggregator --> ClientOM[OpenMeteo Client]
        Aggregator --> ClientAQI[AQICN Client]
        Advisor --> ClientGemini[Gemini API]
        Normalizer --> ClientGemini
    end
    
    subgraph "Infrastructure (基础设施)"
        Tool2 --> SSH[SSH Subprocess]
        SSH -->|Pipe Payload| RaspberryPi[树莓派 (E-ink Display)]
    end
```

### 关键层级解析：
*   **Clients**: 所有的 HTTP 请求只发生在这里。比如 `open_meteo.py` 负责怎么查坐标，怎么处理重试，怎么调用 Normalizer 纠错。
*   **Services**:
    *   `Aggregator`: “这儿有一个城市名，帮我把它的天气、AQI、地理位置全找齐”。
    *   `Processor`: 数据清洗工。把 API 原始的 `weather_code: 3` 翻译成 `"Overcast"`，处理时区，格式化时间。
    *   `Advisor`: 策略模式 (Strategy Pattern)。决定是问 Google 还是问 Claude 要建议。
    *   `Normalizer`: 翻译官。把 "大理" 变成 "Dali"。
*   **Main**: 对外暴露的窗口。定义了 MCP 工具的接口规范。

---

## 3. 工作流 (Workflow) - 以 `update_remote_display` 为例

当您发送指令 **"Update Dali weather"** 时，内部发生了什么？

1.  **输入接收**: `main.py` 收到 `city_name="Dali"`。
2.  **数据获取 (Fetch)**:
    *   `Aggregator` 启动。
    *   `OpenMeteoClient` 搜索 "Dali"。
    *   *(如果是中文 "大理")* -> 搜索失败 -> **触发 Normalizer** -> Gemini 翻译为 "Dali" -> 重试搜索成功。
    *   并发获取 🌡️天气 和 😷AQI 数据。
3.  **数据处理 (Process)**:
    *   `Processor` 统一格式，计算时间，翻译天气描述。
4.  **建议生成 (Advise)**:
    *   `Advisor` 将当前数据喂给 Gemini，生成："空气不错，去洱海边散步吧！"
5.  **远程部署 (Deploy)**:
    *   `main.py` 将所有清洗好的数据打包成 JSON。
    *   生成符合 MCP 协议的握手包。
    *   **SSH 隧道开启**:
        *   -> `scp` 传输 JSON 文件到树莓派。
        *   -> `ssh` 远程执行命令 (含除僵尸进程逻辑 + 超时保护)。
        *   -> 树莓派上的 `Display Tool` 启动，刷新屏幕。
        *   -> `main.py` 捕获 "Successfully displayed" 日志。
6.  **反馈**: 告知用户 "✅ 成功更新大理天气..."。

---

## 4. 关键文件索引
*   📄 `main.py`: 程序的灵魂，定义了 MCP 工具。
*   📄 `services/advisor.py`: AI 建议生成器。
*   📄 `services/normalizer.py`: 中文城市名纠错器。
*   📄 `clients/open_meteo.py`: 天气数据源 (含回退逻辑)。
*   📄 `.env`: 配置 API Key 和 `ADVICE_MODE` 的地方。
