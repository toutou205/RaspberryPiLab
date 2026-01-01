---
updated: 2025-12-31 15:52
---
# Role
你是一个资深的 Python 后端与嵌入式系统工程师，擅长编写高性能、高可靠性的 MCP Server 工具。

# Task
编写一个名为 mcp-weather-air-info-server 的 MCP Server。该工层的任务是接收城市名称，并行聚合多个气象 API 数据，进行逻辑处理与格式校验，最后输出符合特定 JSON Schema 的数据包。


mcp-weather-air-info-server/
├── .env                # 环境配置 (API_KEY, ADVICE_MODE)
├── config.py           # 配置类：读取环境变量，定义常量映射（如国家代码对照表）
├── main.py             # 入口文件：初始化 FastMCP，注册 Tool，整合各 Service
├── models.py           # 数据定义层：存放 Pydantic BaseModel (Payload & API Response)
├── services/           # 业务逻辑层 (Core Logic)
│   ├── __init__.py
│   ├── aggregator.py   # 数据聚合器：执行并行 I/O 调度 (fetch_all_data)
│   ├── processor.py    # 数据处理器：清洗数据、时区转换、WMO 编码转换
│   └── advisor.py      # 建议策略类：实现 Strategy Pattern (Sampling vs Direct API)
├── clients/            # 通讯层 (Infrastructure)
│   ├── __init__.py
│   ├── open_meteo.py   # 封装 Open-Meteo 的异步请求逻辑
│   └── aqicn.py        # 封装 AQICN 的异步请求逻辑
└── utils/              # 工具类
    ├── datetime_tool.py # 处理时区与格式化时间字符串
    └── validator.py     # Pydantic 校验逻辑封装

|**文件/目录**|**核心作用 (Responsibility)**|**上下文从属关系 (Relationship)**|
|---|---|---|
|**`main.py`**|**系统总线**。负责 MCP 协议对接与最终输出。|调用 `services.aggregator` 获取聚合后的干净数据。|
|**`models.py`**|**唯一事实来源**。定义 Pydantic 模型。|被 `clients` 用于解析原始数据，被 `main` 用于最终校验。|
|**`aggregator.py`**|**并发控制器**。管理 `httpx` 的并发请求。|调用 `clients` 下的所有外部接口。|
|**`advisor.py`**|**策略执行引擎**。处理 `advice_msg` 的生成逻辑。|根据 `config.py` 的模式决定调用 `ctx.sample` 或外部 LLM API。|
|**`processor.py`**|**数学逻辑库**。处理单位换算、时间对齐、WMO 解码。|处理由 `aggregator` 获取的原始报文。|

# Execution Logic (Pipeline)
1. **Parallel Data Acquisition (Asyncio)**:
   - 使用 `httpx` 同时启动三个异步请求：
     - **Open-Meteo Geocoding**: 获取输入城市的 Latitude, Longitude, Country Code.
     - **AQICN API**: 获取该城市的 AQI, PM2.5.
     - **Open-Meteo Weather**: 基于经纬度获取当前 Temperature, Weather Code (WMO), Wind Speed 等。
2. **Data Alignment & Processing**:
   - 提取各接口返回的原始数据，按逻辑优先级合并。
   - 转换时间戳为格式：`YY/MM/DD HH:mm Week` (如 "25/12/30 10:49 Tue")。
3. **Internal Advice Generation**:
   - 构造一个特定的 Prompt 片段发送给 LLM（通过 MCP context），根据获取的温度和 AQI 数据生成 `advice_msg`。
   - 限制：严格遵循世卫组织（WHO）健康建议，风格幽默睿智，总长度不超过 32 个英文字符。
4. **Validation**:
   - 使用 pydantic 库验证输出数据是否符合预定义的 Schema。

# Data Structure (Target JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "E-Ink Weather Display Payload",
  "description": "Schema for the data sent to the Raspberry Pi e-ink display.",
  "type": "object",
  "properties": {
    "country_code": {
      "type": "string",
      "description": "Country code (e.g., 'USA', 'CHN')",
      "maxLength": 3
    },
    "city_name": {
      "type": "string",
      "description": "Name of the city"
    },
    "timestamp": {
      "type": "string",
      "description": "Formatted timestamp: YY/MM/DD HH:mm Week",
      "pattern": "^\\d{2}/\\d{2}/\\d{2} \\d{2}:\\d{2} (Mon|Tue|Wed|Thu|Fri|Sat|Sun)$"
    },
    "weather_code": {
      "type": "integer",
      "description": "WMO weather code",
      "minimum": 0,
      "maximum": 99
    },
    "weather_desc": {
      "type": "string",
      "description": "Weather description in English"
    },
    "temperature": {
      "type": "number",
      "description": "Temperature in Celsius"
    },
    "aqi": {
      "type": "integer",
      "description": "Air Quality Index",
      "minimum": 0,
      "maximum": 1000
    },
    "pm25": {
      "type": "number",
      "description": "PM2.5 concentration",
      "minimum": 0
    },
    "advice_msg": {
      "type": "string",
      "description": "Witty health advice based on WHO standards (Temp & AQI). Style: Humorous but practical. Constraint: Max 32 chars including spaces/punctuation.",
      "maxLength": 32
    }
  },
  "required": [
    "country_code",
    "city_name",
    "timestamp",
    "weather_code",
    "weather_desc",
    "temperature",
    "aqi",
    "pm25",
    "advice_msg"
  ]
}
```

# Data Specification
## advice_msg prompt

**System Role**: You are a wise and witty health consultant specializing in WHO environmental standards.

**Task**: Generate a health advice string based on current Weather and AQI data.

**Rules**:

1. **Core Standard**: Follow WHO Global Air Quality Guidelines.
    
2. **Logic**:
    
    - Low Temp + High AQI: Stay home, keep warm.
        
    - High AQI: Danger! Stay inside.
        
    - Moderate AQI: Sensitive groups mask up.
        
    - Good Weather/AQI: Go out, breathe deep!
        
3. **Tone**: Humorous, practical, and sharp.
    
4. **Constraint**: **MAX 32 English characters** (including spaces/punctuation). No markdown.
    

**Data Context**:

- Temp: {temperature}°C
    
- AQI: {aqi}
    
- Weather: {weather_desc}
    

**Few-Shot Examples**:

- _Input: 25°C, AQI 15_ -> "Perfect day! Open windows now." (28 chars)
    
- _Input: 5°C, AQI 20_ -> "Clean air, cold nose. Wrap up!" (30 chars)
    
- _Input: 22°C, AQI 350_ -> "Toxic air! Stay home, stay safe." (32 chars)
    
- _Input: 20°C, AQI 85_ -> "Sensitive? Mask on or stay in." (30 chars)
    

**Output advice_msg**:


# **Advice Generation Strategy (Dual-Mode)**

> 必须实现**策略模式 (Strategy Pattern)**，通过环境变量 `ADVICE_MODE` 切换 `advice_msg` 的生成路径：
> 
> 1. **SAMPLING 模式 (Flexibility)**:
>     
>     - **触发条件**: `ADVICE_MODE="SAMPLING"`。
>         
>     - **执行逻辑**: 调用 MCP 的 Sampling 特性，通过 `ctx.session.create_message` 向客户端（Cursor）发起反向推理请求。
>         
>     - **优点**: 无需额外 API Key，复用客户端模型额度。
>         
> 2. **DIRECT_API 模式 (Automation & Stability)**:
>     
>     - **触发条件**: `ADVICE_MODE="API"` (默认值)。
>         
>     - **执行逻辑**: 使用 `httpx` 直接异步请求 Google Gemini API (`gemini-2.0-flash`)。
>         
>     - **配置依赖**: 必须从环境变量读取 `GEMINI_API_KEY`。
>         
>     - **优点**: 响应极快 (<1s)，全自动化无需人工确认，适合树莓派定时刷新场景。
>         
> 3. **统一约束**:
>     
>     - 无论采用哪种模式，输入给 LLM 的 Prompt 必须包含：当前温度、AQI、天气现象、WHO 健康标准。
>         
>     - 输出结果必须强制截断至 32 个英文字符以内。
>     - 代码逻辑中必须包含 `final_msg = advice[:32]` 的强制截断兜底方案。
>


## timestamp

1. 指的是所查询地址的当地时间，而不是单纯的指本地PC时间错时间。
2. `search_city` 阶段获取该城市的 `timezone` 字符串，并在处理逻辑中显式进行时区转换。

## country_code

1. 需要通过城市名找到对应的国家名，转换成对应3个字母的国家代码。
2. 要求引入转换逻辑（或使用 `pycountry` 库）将其映射为要求的 3 位代码（如 "ITA"）。


## The mapping relationship between WMO Code and Codeweather_desc

|    **WMO Code**    |  **weather_desc**  |
| :----------------: | :----------------: |
|       **0**        | **Sunny / Clear**  |
|       **1**        |  **Mainly Clear**  |
|       **2**        | **Partly Cloudy**  |
|       **3**        |    **Overcast**    |
|     **80, 81**     |  **Shower Rain**   |
|       **82**       | **Heavy Showers**  |
|       **95**       |  **Thunderstorm**  |
|     **96, 99**     | **T-Storm w/Hail** |
|       **61**       |   **Light Rain**   |
|       **63**       | **Moderate Rain**  |
|       **65**       |   **Heavy Rain**   |
|   **51, 53, 55**   |    **Drizzle**     |
| **56, 57, 66, 67** | **Freezing Rain**  |
|     **71, 77**     | **Lt Snow/Grain**  |
|       **73**       | **Moderate Snow**  |
|       **75**       |   **Heavy Snow**   |
|     **85, 86**     |  **Snow Shower**   |
|       **45**       |      **Fog**       |
|       **48**       |    **Rime Fog**    |
|    Else / None     |    **Unknown**     |


# Required Functions

1.  `search_city(city_name)`: 不论输入的为何种语言城市名，都可以转换成对应的英文，同时返回对应坐标。
	
2. `fetch_all_data(city_name)`: 负责并行网络 I/O。
    
3. `process_logic(raw_data)`: 负责数据清洗、单位转换及时间格式化。
    
4. `generate_advice(weather_data)`: 构造内部 Prompt 并调用 LLM 接口。
    
5. `validate_payload(json_data)`: 执行 Schema 校验。
    
6. `mcp_main()`: MCP 工具入口，注册 `get_full_weather_report` 工具。
    

# Technical Constraints

- 必须使用异步编程模型 (async/await)。
    
- 包含完备的错误处理（如网络超时、API 密钥失效、城市未找到）。
    
- 拒绝任何翻译腔，注释采用中英双语，逻辑清晰。
    