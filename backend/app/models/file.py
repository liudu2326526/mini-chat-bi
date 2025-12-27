from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.db.session import Base

class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    file_hash = Column(String, index=True)  # 用于去重检测 (可选)
    columns = Column(JSON, nullable=True)   # 存储表头信息
    created_at = Column(DateTime(timezone=True), server_default=func.now())
