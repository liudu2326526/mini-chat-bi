import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 获取当前文件 (session.py) 的绝对路径
# .../backend/app/db/session.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# .../backend

# 项目根目录 (再往上一层)
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# 数据库文件路径
DB_PATH = os.path.join(PROJECT_ROOT, "data", "chat_bi.db")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# check_same_thread=False is needed only for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
