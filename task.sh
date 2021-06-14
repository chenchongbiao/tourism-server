source /home/bluesky/PycharmProjects/tourism-Server/venv/bin/activate
#python3 /home/bluesky/PycharmProjects/tourism-Server/main.py
gunicorn main:app -b 0.0.0.0:5000 -w 4 -k uvicorn.workers.UvicornWorker
echo "success"

# 启动命令
# gunicorn main:app -b 0.0.0.0:8001 -w 4 -k uvicorn.workers.UvicornWorker  # -D 守护启动 -c 配置文件

