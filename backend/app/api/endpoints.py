from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.file_service import FileService
from app.services.chat_service import ChatService
from app.models.file import UploadedFile as UploadedFileModel
from app.schemas.file import FileResponse
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    上传 Excel/CSV 文件，返回文件 ID 和数据预览。
    """
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported")
    
    return await FileService.save_upload_file(db, file)

@router.post("/chat", response_model=ChatResponse)
async def chat_analysis(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    对话分析接口
    """
    # 1. 查找文件记录
    file_record = db.query(UploadedFileModel).filter(UploadedFileModel.id == request.file_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
        
    # 2. 调用分析服务
    result = await ChatService.analyze(file_record, request.query)
    
    return result
