import os
from openai import OpenAI

# 初始化火山引擎 Ark 客户端 (兼容 OpenAI 接口)
ARK_API_KEY = os.environ.get("ARK_API_KEY") or "e512c929-afab-46d2-8011-6d4b04ee71db"
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

client = OpenAI(
    api_key=ARK_API_KEY,
    base_url=ARK_BASE_URL,
)

DEFAULT_MODEL = "deepseek-v3-2-251201"

def get_llm_client():
    return client
