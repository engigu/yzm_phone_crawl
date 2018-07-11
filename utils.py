import os
import functools

import defaults


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
    elif raw == '-8' or '不足' in raw:  # 余额不足
        return True, '余额不足'
    else:
        return False, ''


def save_pid(full_PID_file_name):
    pid = os.getpid()
    with open(full_PID_file_name, 'w') as f:
        f.write(str(pid))


def remove_pid_file(full_PID_file_name):
    try:
        os.remove(full_PID_file_name)
        return True, '成功删除pid文件'
    except:
        return False, '删除pid文件失败'


def downloader():  # 下载器
    pass


def need_save_pid_files(pid_files_path, need=defaults.SAVE_PID_FILES):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if need:
                save_pid(pid_files_path)
            func(*args, **kwargs)
        return wrapper
    return decorator


def need_remove_pid_files(pid_files_path, need=defaults.SAVE_PID_FILES):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if need:
                print(remove_pid_file(pid_files_path))
            func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == '__main__':
    print(defaults.SAVE_PID_FILES)
