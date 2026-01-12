import re
import pandas as pd
from config import DETECT_CONFIG

# ========== 原有5条规则（保留不变） ==========
def validate_required_columns(df):
    """规则1：必填列存在性+非空检测"""
    errors = []
    missing_columns = [col for col in DETECT_CONFIG["required_columns"] if col not in df.columns]
    if missing_columns:
        errors.append(f'缺少必填列：{",".join(missing_columns)}')

    for col in DETECT_CONFIG["required_columns"]:
        if col in df.columns:
            empty_rows = df[df[col].isna() | (df[col] == '')].index + 1
            if len(empty_rows) > 0:
                errors.append(f'必填列「{col}」空值行：{list(empty_rows)}')
    return errors

def validate_date_format(df):
    """规则2：日期列格式校验"""
    errors = []
    date_patterns = [r'^\d{4}-\d{2}-\d{2}$', r'^\d{8}$']
    for col in DETECT_CONFIG["date_columns"]:
        if col in df.columns:
            non_empty_date = df[df[col].notna() & (df[col] != '')][col].astype(str)
            invalid_rows = []
            for idx, date_str in non_empty_date.items():
                if not any(re.match(pattern, date_str) for pattern in date_patterns):
                    invalid_rows.append(idx + 1)
            if invalid_rows:
                errors.append(f'日期列「{col}」格式错误行（需YYYY-MM-DD/YYYYMMDD）：{invalid_rows}')
    return errors

def validate_numeric_columns(df):
    """规则3：数值列合法性校验"""
    errors = []
    for col in DETECT_CONFIG["numeric_columns"]:
        if col in df.columns:
            non_empty_vals = df[df[col].notna() & (df[col] != '')][col]
            non_numeric_rows = []
            negative_rows = []
            for idx, val in non_empty_vals.items():
                try:
                    num_val = float(val)
                    if num_val < 0:
                        negative_rows.append(idx + 1)
                except (ValueError, TypeError):
                    non_numeric_rows.append(idx + 1)
            if non_numeric_rows:
                errors.append(f'数值列「{col}」非数字行：{non_numeric_rows}')
            if negative_rows:
                errors.append(f'数值列「{col}」负数行：{negative_rows}')
    return errors

def validate_duplicate_values(df):
    """规则4：唯一标识列重复值检测"""
    errors = []
    for col in DETECT_CONFIG["duplicate_check_columns"]:
        if col in df.columns:
            non_empty_vals = df[df[col].notna() & (df[col] != '')][col]
            duplicate_vals = non_empty_vals.value_counts()[non_empty_vals.value_counts() > 1].index
            for val in duplicate_vals:
                duplicate_rows = non_empty_vals[non_empty_vals == val].index + 1
                errors.append(f'唯一标识列「{col}」值「{val}」重复行：{list(duplicate_rows)}')
    return errors

def validate_column_name_format(df):
    """规则5：列名格式规范检测"""
    errors = []
    pattern = DETECT_CONFIG["column_name_illegal_chars"]
    for col in df.columns:
        if re.search(pattern, col):
            errors.append(f'列名「{col}」包含非法字符（仅允许中文/字母/数字/下划线）')
        if '　' in col:
            errors.append(f'列名「{col}」包含全角空格，建议替换为半角/下划线')
    return errors

# ========== 新增5条规则（凑够10条） ==========
def validate_empty_rows(df):
    """规则6：空行检测（无任何数据的行）"""
    errors = []
    # 检测全空行（所有列都是空值）
    empty_rows = df[df.isna().all(axis=1)].index + 1
    if len(empty_rows) > 0:
        errors.append(f'CSV中存在纯空行：{list(empty_rows)}')
    return errors

def validate_enum_values(df):
    """规则7：枚举值合法性检测"""
    errors = []
    for col, allowed_vals in DETECT_CONFIG["enum_columns"].items():
        if col in df.columns:
            non_empty_vals = df[df[col].notna() & (df[col] != '')][col].astype(str)
            invalid_rows = []
            for idx, val in non_empty_vals.items():
                if val not in allowed_vals:
                    invalid_rows.append(idx + 1)
            if invalid_rows:
                errors.append(f'枚举列「{col}」取值错误行（仅允许：{allowed_vals}）：{invalid_rows}')
    return errors

def validate_data_length(df):
    """规则8：数据长度检测（不超过最大长度）"""
    errors = []
    for col, max_len in DETECT_CONFIG["max_length_columns"].items():
        if col in df.columns:
            non_empty_vals = df[df[col].notna() & (df[col] != '')][col].astype(str)
            over_length_rows = []
            for idx, val in non_empty_vals.items():
                if len(val) > max_len:
                    over_length_rows.append(idx + 1)
            if over_length_rows:
                errors.append(f'列「{col}」字符长度超过{max_len}位，违规行：{over_length_rows}')
    return errors

def validate_special_chars(df):
    """规则9：特殊字符检测（禁止敏感特殊字符）"""
    errors = []
    # 敏感特殊字符：\ / : * ? " < > |
    special_char_pattern = r'[\\/:*?"<>|]'
    for col in DETECT_CONFIG["special_char_columns"]:
        if col in df.columns:
            non_empty_vals = df[df[col].notna() & (df[col] != '')][col].astype(str)
            invalid_rows = []
            for idx, val in non_empty_vals.items():
                if re.search(special_char_pattern, val):
                    invalid_rows.append(idx + 1)
            if invalid_rows:
                errors.append(f'文本列「{col}」包含敏感特殊字符（\\/:*?"<>|），违规行：{invalid_rows}')
    return errors

def validate_full_width_chars(df):
    """规则10：全角数字/字母检测（需为半角）"""
    errors = []
    # 匹配全角数字/字母
    full_width_pattern = r'[０-９ａ-ｚＡ-Ｚ]'
    for col in DETECT_CONFIG["full_width_columns"]:
        if col in df.columns:
            non_empty_vals = df[df[col].notna() & (df[col] != '')][col].astype(str)
            invalid_rows = []
            for idx, val in non_empty_vals.items():
                if re.search(full_width_pattern, val):
                    invalid_rows.append(idx + 1)
            if invalid_rows:
                errors.append(f'列「{col}」包含全角数字/字母，需改为半角，违规行：{invalid_rows}')
    return errors

# ========== 核心检测函数（整合10条规则） ==========
def detect_csv_compliance(filename):
    """核心检测函数：整合所有10条规则"""
    from csv_parser import read_csv_file
    try:
        df = read_csv_file(filename)
        total_rows = len(df)
        all_errors = []

        # 执行10条检测规则
        all_errors.extend(validate_required_columns(df))      # 1
        all_errors.extend(validate_date_format(df))           # 2
        all_errors.extend(validate_numeric_columns(df))       # 3
        all_errors.extend(validate_duplicate_values(df))      # 4
        all_errors.extend(validate_column_name_format(df))    # 5
        all_errors.extend(validate_empty_rows(df))            # 6
        all_errors.extend(validate_enum_values(df))           # 7
        all_errors.extend(validate_data_length(df))           # 8
        all_errors.extend(validate_special_chars(df))         # 9
        all_errors.extend(validate_full_width_chars(df))      # 10

        return {
            'status': 'success',
            'total_rows': total_rows,
            'compliant': len(all_errors) == 0,
            'error_count': len(all_errors),
            'error_details': all_errors,
            'summary': f'共检测{total_rows}条数据，发现{len(all_errors)}个合规问题' if all_errors else f'共检测{total_rows}条数据，全部合规'
        }
    except Exception as e:
        return {'status': 'error', 'message': f'检测失败：{str(e)}'}
