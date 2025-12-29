# AI 编程规范指南 (Mini Chat BI)

本指南旨在规范 Mini Chat BI 项目的代码风格与开发模式。在后续的 AI 辅助编程中，请严格遵守以下约定。

## 1. 技术栈概览 (Tech Stack)

*   **前端**: Vue 3 (Composition API) + TypeScript + Vite + Naive UI + ECharts
*   **后端**: Python 3.10+ + FastAPI + SQLAlchemy (SQLite) + Pandas
*   **AI**: VolcEngine (OpenAI Compatible) + LangChain (Optional)

## 2. 项目结构规范 (Project Structure)

### 2.1 目录职责
*   **frontend/**: 仅包含前端代码。
    *   `src/api/`: 所有 HTTP 请求必须封装在此，禁止在组件内直接调用 `axios.post`。
    *   `src/components/`: 通用组件 (如 `ChartRenderer.vue`)。
    *   `src/views/`: 页面级组件 (本项目为单页应用，主要在 `App.vue` 调度)。
*   **backend/**: 仅包含后端代码。
    *   `app/models/`: SQLAlchemy 数据库模型 (ORM)。
    *   `app/schemas/`: Pydantic 数据验证模型 (Request/Response)。
    *   `app/services/`: 复杂业务逻辑 (如文件处理、AI 对话)，禁止在 API 路由层直接写业务逻辑。
    *   `app/api/`: 仅负责路由分发、参数校验和调用 Service。

## 3. 前端开发规范 (Frontend)

### 3.1 Vue 组件风格
*   **SFC 模式**: 必须使用 `<script setup lang="ts">` 语法糖。
*   **UI 库**: 统一使用 **Naive UI**。
    *   导入方式: 推荐按需导入或全局自动导入 (本项目目前使用手动导入，需保持一致)。
    *   图标库: 使用 `@vicons/ionicons5`。
*   **类型安全**:
    *   `props` 定义必须使用 TypeScript 泛型语法: `defineProps<{ foo: string }>()`。
    *   `emits` 定义必须使用 TypeScript 泛型语法: `defineEmits<{ (e: 'change', val: number): void }>()`。
*   **响应式变量**:
    *   基础数据类型使用 `ref`。
    *   对象/数组推荐使用 `ref` (保持统一)，也可以使用 `reactive`，但需注意解构丢失响应性问题。

### 3.2 异步请求
*   所有 API 必须在 `src/api/index.ts` 中定义类型接口 (Interface)。
*   使用 `async/await` 处理异步，避免回调地狱。
*   必须包含错误处理 (`try...catch`)，并在 UI 层给予用户反馈 (`message.error`)。

## 4. 后端开发规范 (Backend)

### 4.1 代码风格
*   **类型提示**: 所有函数参数和返回值**必须**标注 Type Hints。
    *   Good: `def get_user(user_id: int) -> User:`
*   **命名规范**:
    *   变量/函数: `snake_case` (如 `file_path`)
    *   类名: `PascalCase` (如 `ChatService`)
    *   常量: `UPPER_CASE` (如 `DEFAULT_MODEL`)

### 4.2 数据库与模型
*   **SQLAlchemy**:
    *   模型类继承自 `Base`。
    *   使用 `Session` 依赖注入 (`Depends(get_db)`) 管理数据库连接。
*   **Pydantic**:
    *   Schema 类分为 `Base`, `Create`, `Response` 三层继承结构，避免字段泄露。

### 4.3 错误处理
*   使用 `FastAPI.HTTPException` 抛出 HTTP 错误，不要直接返回 JSON。
    *   Good: `raise HTTPException(status_code=404, detail="File not found")`

## 5. AI 交互与 Prompt 工程

### 5.1 Prompt 设计原则
*   **Role**: 明确指定 AI 的角色 (如 "Python 数据分析专家")。
*   **Context**: 提供足够的数据上下文 (Schema、Sample Data)，但注意不要超出 Token 限制。
*   **Constraints**: 明确约束输出格式 (如 "只输出代码"、"Result 必须是 JSON")。

### 5.2 代码执行安全
*   生成的代码必须在受控环境中执行。
*   **禁止**直接执行包含 `os.system`, `subprocess` 等危险操作的代码 (需在 Prompt 中注入系统级指令防御，或在代码执行层做 AST 检查)。

## 6. Git 提交规范
*   格式: `<Type>: <Subject>`
*   Type 列表:
    *   `feat`: 新功能
    *   `fix`: 修复 Bug
    *   `docs`: 文档变更
    *   `refactor`: 代码重构 (无功能变动)
    *   `chore`: 构建/依赖/配置变动
*   示例: `feat: add chart renderer component`
