from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class FileBase(BaseModel):
    filename: str

class FileCreate(FileBase):
    filepath: str
    file_hash: str
    columns: List[str]

class FileResponse(FileBase):
    id: int
    columns: List[str]
    created_at: datetime
    # 预览数据不存数据库，只在上传响应时返回，或者单独接口返回
    preview: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes = True
