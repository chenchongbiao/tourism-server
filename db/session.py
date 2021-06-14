from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


engine = create_engine(
    # echo=True表示引擎将用repr()函数记录所有语句及其参数列表到日志 由于SQLAlchemy是多线程，指定check_same_thread=False来让建立的对象任意线程都可使用。这个参数只在用SQLite
    # 数据库时设置 connect_args={"check_same_thread": False}
    settings.SQLALCHEMY_DATABASE_URL, encoding='utf-8', echo=True
)

# 在SQLAlchemy中，CRUD都是通过会话(session)进行的，所以我们必须要先创建会话，每一个SessionLocal实例就是一个数据库session
# flush()是指发送数据库语句到数据库，但数据库不一定执行写入磁盘；commit()是指提交事务，将变更保存到数据库文件
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=True)

