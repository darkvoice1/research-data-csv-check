FROM python:3.9-slim
WORKDIR /app
# 安装系统依赖（这一步日志显示已成功，保留）
RUN apt update -y && apt install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/*
# 复制依赖文件
COPY requirements.txt .
# 关键修改：去掉pip升级，改用阿里云源安装依赖（稳定不报错）
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
# 复制代码
COPY . .
EXPOSE 5000
# 启动Flask（确认你的app.py路径是backend/app.py，不是的话改这里）
CMD ["python", "-u", "backend/app.py"]
