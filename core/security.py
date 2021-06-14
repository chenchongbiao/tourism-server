from jose import jwt
from datetime import timedelta, datetime
from typing import Union, Any
from passlib.context import CryptContext
from core.config import settings

# 设置加密文本
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
# 算法
ALGORITHM = 'HS256'

# 获取加密厚的密码
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 校验登录的米啊
def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

# 创建token
def create_access_token(
    # Union设置返回类型str或者任意
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    # 如果有过期时间
    if expires_delta:
        # utcnow读取“世界标准时间，重新设置token过期时间
        expire = datetime.utcnow() + expires_delta
    else:
        # 如果没有token设置一个token
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {
        'exp': expire,
        'sub': str(subject)
    }
    encoded_jwt = jwt.encode(
        # claims加密内容，key密码，algorithm算法
        claims=to_encode, key=settings.SECRET_KEY, algorithm=ALGORITHM
    )
    # 返回jwt
    return encoded_jwt

