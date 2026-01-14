# 基础镜像：Python3.9-slim（兼容pandas2.1.4，稳定）
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 第一步：提前装pandas编译需要的系统库（避免后续安装失败）
RUN apt update && apt install -y gcc python3-dev && rm -rf /var/lib/apt/lists/*

# 第二步：复制依赖文件，用国内源装依赖（和本地一致）
COPY requirements.txt .
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 第三步：复制所有代码到容器
COPY . .

# 暴露Flask端口（必须和代码里的5000一致）
EXPOSE 5000

# 启动Flask服务（加-u实时输出日志，方便排查）
CMD ["python", "-u", "backend/app.py"]
