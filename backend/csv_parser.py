import pandas as pd
from config import UPLOAD_FOLDER
import os

def read_csv_file(filename):
    """读取CSV文件，兼容utf-8/gbk编码"""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件{filename}不存在")

    try:
        # 优先用utf-8编码读取
        return pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        # 失败则用gbk编码
        return pd.read_csv(file_path, encoding='gbk')
