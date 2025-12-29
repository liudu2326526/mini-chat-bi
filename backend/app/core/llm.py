import os
import sys
from openai import OpenAI

# 初始化火山引擎 Ark 客户端 (兼容 OpenAI 接口)
ARK_API_KEY = os.environ.get("ARK_API_KEY")

if not ARK_API_KEY:
    # 如果没有设置环境变量，打印错误并退出
    print("❌ Error: ARK_API_KEY environment variable is not set.", file=sys.stderr)
    print("Please provide it when starting the application.", file=sys.stderr)
    print("Example: ARK_API_KEY=your_key uvicorn app.main:app", file=sys.stderr)
    sys.exit(1)

ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

client = OpenAI(
    api_key=ARK_API_KEY,
    base_url=ARK_BASE_URL,
)

DEFAULT_MODEL = "deepseek-v3-2-251201"

def get_llm_client():
    return client
