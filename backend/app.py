# 原有的导入保持不变，新增这两行
from flask import send_from_directory
import os

# 原有的CORS(app)、检测接口等代码保持不变

# 新增：前端页面路由（访问根域名时加载index.html）
@app.route('/')
def serve_frontend():
    frontend_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),  # 获取app.py的绝对路径（backend目录）
        '../frontend'  # 向上一级，找到同级的frontend文件夹
    )
    # 确保路径存在（避免部署时因路径问题报错）
    if not os.path.exists(frontend_path):
        return "前端文件夹不存在", 404
    return send_from_directory(frontend_path, 'index.html')

# 新增：前端静态文件路由（加载css、js等文件）
@app.route('/<path:path>')
def serve_static_files(path):
    frontend_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../frontend'
    )
    if not os.path.exists(os.path.join(frontend_path, path)):
        return "静态文件不存在", 404
    return send_from_directory(frontend_path, path)

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from compliance_check import detect_csv_compliance

# 初始化Flask应用
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# ---------------------- 上传功能 ----------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': '未选择上传文件'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': '文件名不能为空'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            file_path = f"{UPLOAD_FOLDER}/{unique_filename}"
            file.save(file_path)

            return jsonify({
                'status': 'success',
                'message': 'CSV文件上传成功',
                'filename': unique_filename,
                'file_path': file_path
            }), 200
        else:
            return jsonify({'status': 'error', 'message': '仅支持CSV格式文件上传'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'上传失败：{str(e)}'}), 500

# ---------------------- 检测接口 ----------------------
@app.route('/detect', methods=['POST'])
def detect_file():
    try:
        data = request.get_json()
        if not data or 'filename' not in data:
            return jsonify({'status': 'error', 'message': '缺少必要参数：filename'}), 400

        filename = data['filename']
        detect_result = detect_csv_compliance(filename)
        return jsonify(detect_result), 200 if detect_result['status'] == 'success' else 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'检测接口异常：{str(e)}'}), 500

# ---------------------- 健康检查 ----------------------
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'success',
        'message': '后端服务正常运行',
        'upload_path': UPLOAD_FOLDER
    }), 200

# 启动服务
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
