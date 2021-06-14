from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

import mapper
import models
import schemas
from core import security
from core.config import settings
from db.session import SessionLocal

"""OAuth2 密码模式和 FastAPI 的 OAuth2PasswordBearer"""

"""
OAuth2PasswordBearer是接收URL作为参数的一个类：客户端会向该URL发送username和password参数，然后得到一个Token值
OAuth2PasswordBearer并不会创建相应的URL路径操作，只是指明客户端用来请求Token的URL地址
当请求到来的时候，FastAPI会检查请求的Authorization头信息，如果没有找到Authorization头信息，或者头信息的内容不是Bearer token，它会返回401状态码(UNAUTHORIZED)
"""
# 请求Token的URL地址 http://127.0.0.1:8000/api/v1/login/access-token
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_V1_STR}/login/access-token'
)


# 返回数据连接
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 获取当前用户
def get_current_user(
        # 注入数据库依赖
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        # 尝试从token解出用户信息
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Could not validate credentials'
        )
    # 从数据库获取用户
    user = mapper.user.get(db, id=token_data.sub)
    # 如果没用用户
    if not user:
        raise HTTPException(
            status_code=404, detail='User not found'
        )
    return user

# 判断是否为超级管理员用户
def get_current_active_admin(
        current_user: models.User = Depends(get_current_user)
) -> models.User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges"
        )
    return current_user
