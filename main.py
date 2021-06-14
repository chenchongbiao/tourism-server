# -*-coding:utf-8-*-
# fix to ModuleNotFound
import os
import sys
import time
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.api_v1.api import api_router
from core.config import settings

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
# sys.path.append("/home/bluesky/PycharmProjects/tourism-Server/venv/lib/python3.7/site-packages")
app = FastAPI(
    title='旅游app的API接口文档',
    description='旅游app的API接口文档',
    version='1.0.0',
    docs_url='/docs', # docs文档地址
    redoc_url='/redocs', # redocs文档地址
)
# CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        # 允许使用证书
        allow_credentials=True,
        # 允许跨域的方法
        allow_methods=["*"],
        # 允许的请求头
        allow_headers=["*"],
)

# mount frontend static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    # reload代码有更改自动启动 debug模式 workers进程数量
    # dev
    uvicorn.run(f'{__name__}:app', port=5000, host='127.0.0.1', reload=True)
    # prod
    # uvicorn.run(app, port=80, host='0.0.0.0', log_config=settings.LOGGING)

