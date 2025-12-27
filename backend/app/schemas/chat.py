from pydantic import BaseModel
from typing import Optional, Dict, Any

class ChatRequest(BaseModel):
    file_id: int
    query: str

class ChatResponse(BaseModel):
    type: str # 'text', 'chart', 'error'
    content: str
    options: Optional[Dict[str, Any]] = None # ECharts options
