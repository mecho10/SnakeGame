import json
import os
import hashlib
import secrets

USER_FILE = "users.json"

def hash_password(password, salt=None):
    """使用 SHA-256 和鹽值對密碼進行哈希"""
    if salt is None:
        salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${password_hash}"

def verify_password(password, hashed_password):
    try:
        salt, stored_hash = hashed_password.split('$')
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return password_hash == stored_hash
    except ValueError:
        return False

def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w", encoding='utf-8') as f:
            json.dump({}, f)
        return {}
    
    try:
        with open(USER_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_users(users):
    try:
        with open(USER_FILE, "w", encoding='utf-8') as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"保存用戶資料時發生錯誤: {e}")
        return False

def validate_input(username, password):
    if not username or not password:
        return False, "用戶名和密碼不能為空"
    
    if len(username) < 3:
        return False, "用戶名至少需要3個字符"
    
    if len(password) < 6:
        return False, "密碼至少需要6個字符"
    
    # 檢查用戶名是否包含非法字符
    if not username.replace('_', '').replace('-', '').isalnum():
        return False, "用戶名只能包含字母、數字、下劃線和連字符"
    
    return True, ""

def register_user(username, password):
    """註冊新用戶"""
    is_valid, error_msg = validate_input(username, password)
    if not is_valid:
        return False, error_msg
    
    users = load_users()
    
    if username in users:
        return False, "用戶名稱已存在"
    
    # 創建新用戶
    hashed_pwd = hash_password(password)
    users[username] = {
        "password": hashed_pwd,
        "high_score": 0
    }
    
    if save_users(users):
        return True, "註冊成功"
    else:
        return False, "註冊失敗，請稍後再試"

def login_user(username, password):
    """用戶登入"""
    if not username or not password:
        return False, "用戶名和密碼不能為空"
    
    users = load_users()
    
    if username not in users:
        return False, "用戶不存在"
    
    stored_password = users[username]["password"]
    

    if '$' not in stored_password:
        if stored_password == hashlib.sha256(password.encode()).hexdigest():
            users[username]["password"] = hash_password(password)
            save_users(users)
            return True, "登入成功"
        else:
            return False, "密碼錯誤"
    else:
        if verify_password(password, stored_password):
            return True, "登入成功"
        else:
            return False, "密碼錯誤"

def update_high_score(username, score):
    """更新用戶最高分數"""
    if not isinstance(score, (int, float)) or score < 0:
        return False
    
    users = load_users()
    if username in users:
        current_high_score = users[username].get("high_score", 0)
        if score > current_high_score:
            users[username]["high_score"] = score
            return save_users(users)
    
    return False

def get_high_score(username):
    """獲取用戶最高分數"""
    users = load_users()
    if username in users:
        return users[username].get("high_score", 0)
    return 0

def get_user_info(username):
    """獲取用戶信息（不包含密碼）"""
    users = load_users()
    if username in users:
        user_info = users[username].copy()
        user_info.pop("password", None)  # 移除密碼信息
        return user_info
    return None
