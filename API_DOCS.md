# API 接口文档 - Mini Chat BI

## 1. 基础说明 (General)
*   **Base URL**: `/api/v1`
*   **Content-Type**: `application/json` (文件上传除外)
*   **响应通用格式**:
    ```json
    {
      "code": 200,      // 200: 成功, 4xx: 客户端错误, 5xx: 服务端错误
      "message": "success",
      "data": { ... }   // 具体业务数据
    }
    ```

## 2. 接口定义 (Endpoints)

### 2.1 上传数据文件
将用户拖拽的 Excel/CSV 文件上传至服务器，并解析表头和预览数据。

*   **URL**: `POST /upload`
*   **Content-Type**: `multipart/form-data`
*   **请求参数 (Form Data)**:

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| file | File | 是 | 支持 .csv, .xlsx 文件，最大 20MB |

*   **响应数据 (Success Response)**:

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| id | Integer | 文件 ID，后续建会话用 |
| filename | String | 原始文件名 |
| columns | Array[String] | 解析出的表头/字段名列表 |
| preview | Array[Object] | 前 5 行数据预览 |

*   **Mock Example**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 101,
    "filename": "2023_sales_report.xlsx",
    "columns": ["日期", "城市", "产品类型", "销售额", "利润"],
    "preview": [
      { "日期": "2023-01-01", "城市": "北京", "产品类型": "电子", "销售额": 12000, "利润": 3000 },
      { "日期": "2023-01-02", "城市": "上海", "产品类型": "家居", "销售额": 8000, "利润": 1500 }
    ]
  }
}
```

---

### 2.2 创建分析会话
基于上传的文件，开启一个新的对话窗口。

*   **URL**: `POST /sessions`
*   **请求参数 (Body)**:

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| file_id | Integer | 是 | 关联的文件 ID |

*   **响应数据**:

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| session_id | String | 会话唯一标识 (UUID) |
| title | String | 会话标题 (默认文件名) |
| created_at | String | 创建时间 (ISO 8601) |

*   **Mock Example**:
```json
{
  "code": 200,
  "message": "Session created",
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "2023_sales_report.xlsx 的分析",
    "created_at": "2023-12-27T10:00:00Z"
  }
}
```

---

### 2.3 发送对话/提问
用户输入问题，后端进行分析并返回结果（文本或图表）。

*   **URL**: `POST /chat`
*   **请求参数 (Body)**:

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| session_id | String | 是 | 当前会话 ID |
| query | String | 是 | 用户的问题，例如"按月统计销售额" |

*   **响应数据**:

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| message_id | Integer | 消息 ID |
| answer_type | String | 回复类型: `text` (纯文本), `chart` (图表), `error` (错误提示) |
| content | String | 文字结论或解释 |
| chart_options | Object | (可选) ECharts 的配置项 JSON，仅在 type='chart' 时存在 |

*   **Mock Example 1: 纯文本回答**:
```json
{
  "code": 200,
  "data": {
    "message_id": 501,
    "answer_type": "text",
    "content": "根据数据统计，2023 年的总销售额为 5,200,000 元。",
    "chart_options": null
  }
}
```

*   **Mock Example 2: 图表回答**:
```json
{
  "code": 200,
  "data": {
    "message_id": 502,
    "answer_type": "chart",
    "content": "这是各城市的销售额分布情况，北京地区遥遥领先。",
    "chart_options": {
      "title": { "text": "各城市销售额统计" },
      "tooltip": { "trigger": "axis" },
      "xAxis": { "type": "category", "data": ["北京", "上海", "广州", "深圳"] },
      "yAxis": { "type": "value" },
      "series": [
        {
          "type": "bar",
          "data": [120000, 98000, 85000, 92000]
        }
      ]
    }
  }
}
```

---

### 2.4 获取历史消息 (可选)
用于页面刷新后恢复聊天记录。

*   **URL**: `GET /sessions/{session_id}/messages`
*   **响应数据**:
    *   返回一个列表，包含上述 `POST /chat` 响应结构中的消息对象，按时间顺序排列。

## 3. 错误码定义 (Error Codes)

| Code | Message | 说明 |
| :--- | :--- | :--- |
| 400 | Bad Request | 参数缺失或格式错误 |
| 404 | Not Found | 文件或会话不存在 |
| 422 | Unprocessable Entity | 文件解析失败或无法生成图表 |
| 500 | Internal Server Error | 服务器内部错误 |
