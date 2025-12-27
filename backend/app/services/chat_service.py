import pandas as pd
import json
import traceback
from app.core.llm import client, DEFAULT_MODEL
from app.models.file import UploadedFile

class ChatService:
    @staticmethod
    async def analyze(file_record: UploadedFile, query: str):
        """
        核心分析逻辑：
        1. 读取数据文件
        2. 构建 Prompt
        3. 调用 LLM 生成代码
        4. 执行代码
        5. 返回结果
        """
        
        # 1. 读取数据 (只读前几行用于 Prompt，执行时读全量)
        try:
            # 这里的 filepath 已经是绝对路径了
            if file_record.filename.endswith('.csv'):
                df_preview = pd.read_csv(file_record.filepath, nrows=5)
            else:
                df_preview = pd.read_excel(file_record.filepath, nrows=5)
        except Exception as e:
            return {"type": "error", "content": f"无法读取数据文件: {str(e)}"}

        columns_info = "\n".join([f"- {col}: {dtype}" for col, dtype in df_preview.dtypes.items()])
        preview_data = df_preview.to_string()

        # 2. 构建 Prompt
        system_prompt = f"""
你是一个 Python 数据分析专家。你的任务是根据用户的问题和给定的数据结构，生成可执行的 Python 代码。

【数据上下文】
- 变量名: `df` (pandas DataFrame)
- 列信息:
{columns_info}
- 数据样例:
{preview_data}

【任务要求】
1. 编写 Python 代码来回答用户的问题。
2. **必须**将最终结果赋值给变量 `result`。
3. `result` 的格式要求：
    - 如果是统计数值（如总和、平均值），`result` 应为数字或字符串。
    - 如果需要画图，`result` 必须是一个字典，包含 ECharts 的配置项 (title, tooltip, xAxis, yAxis, series)。
      - 例如: {{ "title": {{ "text": "..." }}, "xAxis": {{ "data": [...] }}, "series": [{{ "type": "bar", "data": [...] }}] }}
      - 注意：ECharts 数据中的 numpy 类型需要转换为原生 Python 类型 (如 int, float, list)。
4. 不要读取文件，假设 `df` 已经存在。
5. 只输出 Python 代码，不要包含 ```python ``` 标记，不要包含解释性文字。
6. 尽量使用中文字体或不依赖特定字体，避免乱码。
"""

        user_prompt = f"用户问题：{query}"

        # 3. 调用 LLM
        try:
            response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1 # 代码生成需要低随机性
            )
            code = response.choices[0].message.content
            # 清理可能的 markdown 标记
            code = code.replace("```python", "").replace("```", "").strip()
            
        except Exception as e:
            return {"type": "error", "content": f"AI 生成失败: {str(e)}"}

        # 4. 执行代码
        try:
            # 重新读取全量数据用于计算
            if file_record.filename.endswith('.csv'):
                df = pd.read_csv(file_record.filepath)
            else:
                df = pd.read_excel(file_record.filepath)
            
            # 执行环境
            local_vars = {"df": df, "pd": pd}
            
            print(f"Executing Code:\n{code}") # Debug log
            
            exec(code, {}, local_vars)
            
            result = local_vars.get("result")
            
            if result is None:
                return {"type": "text", "content": "分析完成，但没有生成结果 (result 变量为空)。"}
            
            # 判断结果类型
            if isinstance(result, dict) and "series" in result:
                return {"type": "chart", "options": result, "content": "已为您生成图表。"}
            else:
                return {"type": "text", "content": str(result)}

        except Exception as e:
            error_msg = f"代码执行出错: {str(e)}\n生成代码:\n{code}"
            print(error_msg)
            return {"type": "error", "content": error_msg}

