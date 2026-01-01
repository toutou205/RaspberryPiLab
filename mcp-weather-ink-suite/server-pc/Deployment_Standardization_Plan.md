# 📦 Deployment & Archival Standardization Plan

为了方便项目的归档、移植和部署，同时严格保护隐私信息，建议将现有工程重构为标准化的发布包结构。

## 1. 📂 推荐目录结构 (Directory Structure)

建议将两个独立的项目归并在一个 `mcp-weather-ink-suite` 根目录下：

```text
mcp-weather-ink-suite/
├── 📁 server-pc/              # 原 mcp-weather-air-info-server (PC端核心)
│   ├── .env.example           # [关键] 隐私信息模板，仅保留Key名
│   ├── main.py                # 需修改: 读取环境变量而非硬编码
│   ├── config.py              # 配置加载逻辑
│   ├── services/              # 核心业务逻辑
│   ├── clients/               # API 客户端
│   ├── utils/                 # 工具类
│   ├── pyproject.toml         # 依赖管理
│   └── README.md              # PC端专用部署指南
│
├── 📁 client-pi/              # 原 project_root_mcp_old (树莓派端渲染器)
│   ├── run_renderer.sh        # 原 run_mcp_server.sh (重命名以明确用途)
│   ├── src/
│   │   ├── main.py            # 遗留的 MCP 入口
│   │   ├── epd2in7b.py        # 屏幕驱动
│   │   └── tools/             # 显示逻辑
│   ├── requirements.txt       # Pi 端依赖
│   └── README.md              # Pi端专用部署指南
│
└── 📄 README.md               # 总项目文档 (含架构图、快速开始)
```

---

## 2. 🛡️ 隐私脱敏方案 (Privacy Cleaning)

在归档前，必须剥离所有硬编码的敏感信息。

### 2.1 PC端 (`server-pc`)
*   **API Keys**: 确保 `.env` 不被提交（添加至 `.gitignore`）。
*   **SSH Credentials**: 目前 `main.py` 中硬编码了 `pi_user="alex"` 和 `pi_host="192.168.3.13"`。
    *   **方案**: 将其移至 `.env`。
    *   **代码修改**:
        ```python
        # Config.py
        PI_HOST = os.getenv("PI_HOST", "raspberrypi.local")
        PI_USER = os.getenv("PI_USER", "pi")
        ```
*   **Proxy Settings**: `clients/*.py` 和 PowerShell 脚本中的代理地址应通过环境变量配置，而非硬编码。

### 2.2 Pi端 (`client-pi`)
*   检查代码中是否包含硬编码的 WiFi 密码或内网穿透 Token。
*   通常作为被动接收端，Pi 端代码较干净，但需检查 `deploy.ps1` 等辅助脚本。

---

## 3. 🚀 部署与移植指南 (Deployment Guide)

### 3.1 步骤一：PC端部署 (Windows/Mac)
1.  **环境准备**: 安装 Python 3.10+ 和 `uv` (推荐)。
2.  **配置隐私文件**:
    ```bash
    cp .env.example .env
    # 编辑 .env 填入:
    # AQICN_API_KEY=...
    # GEMINI_API_KEY=...
    # PI_HOST=192.168.x.x (目标树莓派IP)
    # PI_USER=你的树莓派用户名
    ```
3.  **安装依赖**: `uv sync`
4.  **配置 SSH 免密登录**: 
    *   确保 PC 能通过 `ssh user@ip` 直接连通 Pi，无需密码（使用 `ssh-copy-id`）。

### 3.2 步骤二：树莓派端部署 (Raspberry Pi)
1.  **传输文件**: 将 `client-pi/` 文件夹上传至 Pi (例如 `/home/pi/mcp-renderer`).
2.  **安装依赖**: 
    ```bash
    cd mcp-renderer
    pip install -r requirements.txt
    ```
3.  **开启 SPI**: `sudo raspi-config` -> Interface Options -> SPI -> Enable.
4.  **测试运行**: 运行 `./run_renderer.sh` 确保无报错。

### 3.3 步骤三：客户端连接
*   在 Claude Desktop / Cursor 中配置 MCP Server 指向 PC 端的 `server-pc` 目录。
*   重启客户端，测试指令 "Update remote display"。

---

## 4. 📦 归档操作清单 (Archival Checklist)
- [ ] 创建 `.gitignore` 排除 `__pycache__`, `.env`, `venv/`, `*.log`.
- [ ] 提取 `main.py` 中的 IP/User 到 `config.py`.
- [ ] 创建 `.env.example`.
- [ ] 重命名文件夹结构.
- [ ] 编写上述 Markdown 文档.
