FROM python:3.9-slim
WORKDIR /app
# 安装系统依赖
RUN apt update -y && apt install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/*
# 复制并安装Python依赖
COPY requirements.txt .
RUN pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
# 复制代码
COPY . .
EXPOSE 5000
# 启动Flask（如果你的app.py在根目录，把backend/app.py改成app.py）
CMD ["python", "-u", "backend/app.py"]
