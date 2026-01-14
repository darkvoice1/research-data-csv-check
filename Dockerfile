# 基础镜像：Python3.9-slim（兼容pandas2.1.4）
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 第一步：装pandas编译需要的系统库（加-y避免交互确认）
RUN apt update -y && apt install -y gcc python3-dev && rm -rf /var/lib/apt/lists/*

# 第二步：复制依赖文件，用清华源装依赖（不升级pip，避免403）
COPY requirements.txt .
# 直接装依赖，跳过pip升级（自带的pip23.0.1足够用）
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 第三步：复制所有代码到容器
COPY . .

# 暴露Flask端口
EXPOSE 5000

# 启动Flask服务（加-u实时输出日志）
CMD ["python", "-u", "backend/app.py"]
