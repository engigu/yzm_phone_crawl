import os

try:
    import defaults
except:
    from . import defaults


def return_phone_error_check(raw):
    """主要解决平台返回信息进行异常检测，如余额不足，号码未正确释放

    :return True: 存在异常
    """
    if raw == '0':  # 没登陆或失败
        return True, '没登陆或失败'
    elif raw == '8':
        return True, '8'
    elif raw == '-1':  # 当前没有合条件号码
        return True, '当前没有合条件号码'
    elif raw == '-8':  # 余额不足
        return True, '余额不足'
    elif '不足' in raw:
        return True, '余额不足'
    else:
        return False, ''


def save_pid(full_PID_file_name):
    pid = os.getpid()
    with open(full_PID_file_name, 'w') as f:
        f.write(str(pid))
        f.flush()


def remove_pid_file(full_PID_file_name):
    try:
        os.remove(full_PID_file_name)
        return True, '成功删除pid文件'
    except:
        return False, '删除pid文件失败'


def downloader():
    pass
