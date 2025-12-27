import shutil
import os
import pandas as pd
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.file import UploadedFile as UploadedFileModel
from app.schemas.file import FileResponse

# 获取 backend 目录
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 获取项目根目录
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
# 上传目录
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "data", "uploads")

class FileService:
    @staticmethod
    async def save_upload_file(db: Session, file: UploadFile) -> FileResponse:
        # 1. 确保目录存在
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        # 2. 生成文件路径
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        # 3. 保存文件到磁盘
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
            
        # 4. 使用 Pandas 读取预览和表头
        try:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file_path, nrows=10) # 只读前10行用于预览
            elif file.filename.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path, nrows=10)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file format")
            
            # 处理 NaN 值，替换为 None
            df = df.where(pd.notnull(df), None)
            
            columns = df.columns.tolist()
            preview = df.head(5).to_dict(orient='records')
            
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Failed to parse file: {str(e)}")

        # 5. 存入数据库
        db_file = UploadedFileModel(
            filename=file.filename,
            filepath=file_path,
            file_hash="pending",
            columns=columns
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        
        # 6. 构造返回
        return FileResponse(
            id=db_file.id,
            filename=db_file.filename,
            columns=columns,
            created_at=db_file.created_at,
            preview=preview
        )
