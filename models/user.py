from datetime import datetime
from sqlalchemy import Boolean, Integer, Column, String
from db.base import Base


class User(Base):
    __tablename__ = 'user'  # 数据表的表名
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(Integer, default=lambda: int(datetime.timestamp(datetime.utcnow())), index=True)
    username = Column(String(16), unique=True)
    password = Column(String(254))
