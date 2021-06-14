from typing import Any
from datetime import timedelta
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

import schemas, mapper, models
from api import deps
from core.config import settings
from core import security


router = APIRouter()

@router.post('/register',)
async def register(
        db: Session = Depends(deps.get_db),
        register_user: schemas.UserCreate = Depends()
):
    msg = mapper.user.create(db=db, obj_in=register_user)
    data = {
        "msg": "注册成功"
    }
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)
