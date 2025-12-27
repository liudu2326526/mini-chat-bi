# 技术设计文档 - Mini Chat BI

## 1. 系统架构 (System Architecture)

本系统采用经典的**前后端分离 (Client-Server)** 架构。前端负责交互与图表渲染，后端负责数据处理与 LLM 交互。

### 架构图示
```mermaid
graph TD
    Client[前端 (Vue 3)] <-->|RESTful API| Server[后端 (FastAPI)]
    Server <-->|SQLAlchemy| DB[(SQLite 数据库)]
    Server <-->|Pandas I/O| FileStorage[本地文件存储 (Excel/CSV)]
    Server <-->|API Call| LLM_Service[大语言模型服务]
```

## 2. 技术栈选型 (Tech Stack)

### 2.1 前端 (Frontend)
*   **核心框架**: Vue 3 (Composition API, `<script setup>`)
*   **构建工具**: Vite 5
*   **语言**: TypeScript / JavaScript (混合开发)
*   **状态管理**: Pinia (轻量级状态管理)
*   **UI 组件库**: Naive UI 或 Element Plus (推荐 Naive UI，风格更极简)
*   **图表库**: ECharts (强大的可视化能力)
*   **HTTP 客户端**: Axios
*   **Markdown 渲染**: markdown-it (用于渲染 AI 回复)

### 2.2 后端 (Backend)
*   **Web 框架**: FastAPI (高性能，原生支持异步)
*   **语言**: Python 3.10+
*   **数据分析**: Pandas (核心数据处理引擎，负责读取 Excel/CSV 并执行查询)
*   **ORM**: SQLAlchemy (虽然用 SQLite，但 ORM 便于管理模型)
*   **Schema 验证**: Pydantic
*   **AI 交互**: LangChain 或 原生 OpenAI SDK (用于构建 Prompt 和调用 LLM)

### 2.3 数据库与存储 (Data & Storage)
*   **元数据存储**: SQLite (`chat_bi.db`) - 存储文件记录、会话历史。
*   **文件存储**: 本地文件系统 (`/data/uploads/`) - 存储用户上传的原始 Excel/CSV 文件。

## 3. 项目结构规划 (Directory Structure)

```bash
chat_bi/
├── docs/                   # 产品与技术文档
│   ├── PRODUCT_DOCS.md
│   └── TECHNICAL_DOCS.md
├── data/                   # 数据存储目录 (需在 .gitignore 中忽略内容)
│   ├── uploads/            # 用户上传的文件
│   └── chat_bi.db          # SQLite 数据库文件
├── frontend/               # 前端项目 (Vue + Vite)
│   ├── public/
│   ├── src/
│   │   ├── api/            # Axios 请求封装
│   │   ├── assets/         # 静态资源
│   │   ├── components/     # 通用组件 (如 ChatBubble, ChartRenderer)
│   │   ├── hooks/          # 自定义 Composable 函数 (useChat, useUpload)
│   │   ├── types/          # TS 类型定义
│   │   ├── views/          # 页面视图 (HomeView, ChatView)
│   │   ├── App.vue
│   │   └── main.ts
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── backend/                # 后端项目 (FastAPI)
│   ├── app/
│   │   ├── api/            # API 路由定义 (endpoints)
│   │   ├── core/           # 核心配置 (config, exceptions)
│   │   ├── db/             # 数据库连接与 Session 管理
│   │   ├── models/         # SQLAlchemy 数据库模型
│   │   ├── schemas/        # Pydantic 数据交互模型
│   │   ├── services/       # 业务逻辑 (DataService, LLMService)
│   │   └── main.py         # FastAPI 应用入口
│   ├── requirements.txt
│   └── .env                # 环境变量 (LLM Key 等)
└── README.md
```

## 4. 数据库对象设计 (Database Schema)

尽管是 MVP，为了支持多轮对话和文件管理，我们需要以下三个核心实体。

### 4.1 实体关系图 (ER Diagram)
*   **UploadedFile** (1) ---- (N) **ChatSession**
*   **ChatSession** (1) ---- (N) **ChatMessage**

### 4.2 表结构定义

#### 1. uploaded_files (上传文件表)
记录用户上传的文件元数据。
| 字段名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| id | Integer | YES | 主键, 自增 |
| filename | String | YES | 原始文件名 (e.g., "sales_2023.xlsx") |
| filepath | String | YES | 存储在服务器的物理路径 |
| file_hash | String | YES | 文件哈希 (MD5)，防止重复处理 |
| columns | JSON | NO | 存储文件的表头信息 (Schema)，便于 LLM 理解 |
| created_at | DateTime | YES | 上传时间 |

#### 2. chat_sessions (会话表)
每一次分析过程作为一个会话。
| 字段名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| id | String | YES | UUID, 主键 |
| file_id | Integer | YES | 外键，关联 uploaded_files.id |
| title | String | NO | 会话标题 (可以是用户第一个问题) |
| created_at | DateTime | YES | 创建时间 |

#### 3. chat_messages (消息记录表)
存储对话历史。
| 字段名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| id | Integer | YES | 主键, 自增 |
| session_id | String | YES | 外键，关联 chat_sessions.id |
| role | String | YES | 'user' 或 'assistant' |
| content | Text | YES | 文本内容 |
| message_type | String | YES | 'text', 'chart', 'error' |
| meta_data | JSON | NO | 存储图表配置、生成的代码或调试信息 |
| created_at | DateTime | YES | 发送时间 |

## 5. 关键交互流程与数据流

### 5.1 数据上传流程
1.  **Frontend**: 用户选择文件 -> 调用 `POST /api/upload`。
2.  **Backend**:
    *   接收文件流。
    *   计算 Hash，检查是否已存在 (可选优化)。
    *   保存文件到 `data/uploads/`。
    *   使用 `Pandas` 读取前 N 行，提取 columns (表头) 和 dtypes (数据类型)。
    *   存入 `uploaded_files` 表。
    *   返回 `file_id` 和 `columns` 预览数据给前端。

### 5.2 问答分析流程 (Text-to-Insight)
1.  **Frontend**: 用户输入 "按月统计销售额" -> 调用 `POST /api/chat` (附带 `session_id`, `query`)。
2.  **Backend**:
    *   根据 `session_id` 找到对应的 `file_path` 和 `columns`。
    *   **Prompt 构建**: 将 `columns`、数据样例和用户 `query` 组装成 Prompt。
    *   **LLM 推理**: 要求 LLM 生成 Python (Pandas) 代码 或 SQL 查询，并返回 JSON 格式的图表配置。
    *   **代码执行 (Code Execution)**: *安全沙箱内* 执行生成的 Pandas 代码，得到结果 DataFrame。
    *   **结果格式化**: 将结果转换为前端 ECharts 可用的 JSON 格式。
    *   存入 `chat_messages`。
    *   返回 Response。
3.  **Frontend**: 解析 Response，如果是图表类型，调用 ECharts 渲染；如果是文本，直接显示。

## 6. 开发注意事项
*   **安全性**: 由于涉及代码执行 (Pandas Code Generation)，需严格限制 LLM 生成的代码范围，或者仅使用 Pandas 的安全子集。MVP 阶段可暂不考虑复杂的沙箱，但需注意防范 `os.system` 等恶意调用。
*   **大文件处理**: Pandas 读取大文件会消耗内存，MVP 限制上传文件大小 (e.g., < 20MB)。
*   **Token 限制**: 如果 CSV 列非常多，Prompt 可能会超长，需要对 Columns 信息进行摘要或截断。
