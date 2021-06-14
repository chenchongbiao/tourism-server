from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import inspect


# 传递给 as_declarative() 的所有关键字参数都传递给 declarative_base()。
@as_declarative()
class Base:
    id: Any
    __name__: str

    # 自动构建表名
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    # 构造字典
    def as_dict(self) -> dict:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
