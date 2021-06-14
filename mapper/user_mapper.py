from typing import Optional
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models import User
from mapper import BaseMapper
from schemas import UserCreate, UserUpdate
from core.security import get_password_hash, verify_password


class UserMapper(BaseMapper[User, UserCreate, UserUpdate]):

    # 查找用户名
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        # 相同数据中的第一个数据对象,
        return db.query(User).filter(User.username == username).first()

    # 创建一个用户
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            password=get_password_hash(obj_in.password)
        )
        db.add(db_obj)
        db.commit()
        # 会强制发送select语句，以使session缓存中对象的状态和数据表中对应的记录保持一致。
        db.refresh(db_obj)
        return db_obj

    # 更新用户信息
    def update(
            self, db: Session, *, db_obj: User, obj_in: UserUpdate
    ) -> User:
        # 判断obj_in是否为dict类型
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # 创建模型时未显式设置的字段是否应从返回的字典中排除；默认值为False。
            update_data = obj_in.dict(exclude_unset=True)
        # 获取密码
        if update_data.get('password'):
            # 对密码进行加码
            hashed_password = get_password_hash(update_data["password"])
            # 把密码修改为加密后的密码
            update_data.update({"password": hashed_password})
            # # 删除
            # del update_data["password"]
            # update_data["password"] = hashed_password

        # obj_data = jsonable_encoder(db_obj)
        # as_dict将分区作为字典返回。在此字典中，键是分区整数。值是该整数的倍数。
        obj_data = db_obj.as_dict()

        for field in obj_data:
            if field in update_data:
                # hasattr(object,name)：检查 object 对象是否包含名为 name 的属性或方法。
                # getattr(object,name,default=None)：获取 object 对象中名为 name 的属性的属性值(属性和函数都叫做属性)。
                # setattr(object,name,value)：将 object 对象的 name 属性设为 value。
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        # 会强制发送select语句，以使session缓存中对象的状态和数据表中对应的记录保持一致。
        db.refresh(db_obj)
        return db_obj

    # 验证用户是否授权
    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        auth_user = self.get_by_username(db, username=username)
        if not auth_user:
            return None
        if not verify_password(password, auth_user.password):
            return None
        return auth_user


user = UserMapper(User)
