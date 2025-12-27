from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router
from app.db.session import engine, Base

# 初始化数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini Chat BI API",
    description="Backend for Mini Chat BI",
    version="0.1.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Mini Chat BI API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
