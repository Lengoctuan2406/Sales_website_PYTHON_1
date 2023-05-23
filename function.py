from flask import *
import re

#session chứa account_name hoặc account_id thì được phép đăng nhập
def check_login():
    if 'account_id' in session:
        return True
    else:
        return False

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False
    
def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search('[a-z]', password):
        return False
    if not re.search('[A-Z]', password):
        return False
    if not re.search('[0-9]', password):
        return False
    if not re.search('[!@#$%^&*()_+=\-{}[\]|:;"\'<>,.?/~`]', password):
        return False
    return True