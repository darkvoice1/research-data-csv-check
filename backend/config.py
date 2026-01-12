import os

# 上传配置
UPLOAD_FOLDER = '../temp_uploads'
ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# 通用合规检测配置（扩充到10条规则的配置）
DETECT_CONFIG = {
    # 规则1：必填列
    "required_columns": ["sample_id"],
    # 规则2：日期列
    "date_columns": ["detect_date", "create_date", "采集日期", "检测日期"],
    # 规则3：数值列
    "numeric_columns": ["value", "数值", "结果", "数量", "浓度"],
    # 规则4：重复值列
    "duplicate_check_columns": ["sample_id"],
    # 规则5：列名规范
    "column_name_illegal_chars": r'[^\u4e00-\u9fa5a-zA-Z0-9_]+',

    # 新增规则配置
    # 规则6：枚举值列（格式：{"列名": ["允许值1", "允许值2"]}）
    "enum_columns": {
        "样本类型": ["血液", "尿液", "组织", "唾液"],
        "检测状态": ["已完成", "未完成", "异常"],
        "是否合格": ["是", "否", "合格", "不合格"]
    },
    # 规则7：数据长度限制（格式：{"列名": 最大长度}）
    "max_length_columns": {
        "sample_id": 20,    # 样本编号最长20位
        "备注": 200,        # 备注最长200字
        "检测人员": 10      # 检测人员最长10字
    },
    # 规则8：特殊字符检测列（检测敏感特殊字符）
    "special_char_columns": ["备注", "样本描述", "检测说明"],
    # 规则9：全角字符检测列（数字/字母需为半角）
    "full_width_columns": ["sample_id", "数值", "检测编号"],
    # 规则10：手机号检测列（通用字段）
    "phone_columns": ["联系人电话", "手机号"]
}

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
