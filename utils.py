import functools
import os
import time

import defaults
from ext_funcs.smpt_mail import smtp_sendmail


def return_phone_error_check(raw):
    """主要解决平台返回信息进行异常检测，如余额不足，号码未正确释放

    :return True: 存在异常
    """
    if raw == '0':  # 没登陆或失败
        return True, '没登陆或失败'
    elif '释放号码' in raw:
        return True, '请先释放号码请先释放号码'
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


def record_low_run_time(server, spider_name):  # 记录低于运行时长阈值的次数
    print('record_low_run_time')
    redis_name = defaults.REDIS_RECORD_NAME

    res_exists = server.hget(name=redis_name, key=spider_name)
    if not res_exists:  # 第一次运行spider，设置初始值 1
        server.hset(name=redis_name, key=spider_name, value=1)
        print('does not exists')
    else:
        curr_num = int(res_exists)
        print('current times is', curr_num)
        if curr_num >= defaults.WARNING_TIMES:
            print('over the warning')
            title = 'yangmao phone crawler[%s] waring' % spider_name
            content = '%s<br /><br />0.0' % spider_name
            smtp_sendmail(
                defaults.MAIL_USER,
                defaults.MAIL_PASS,
                defaults.TO_USERS_LIST,
                title,
                content
            )  # 预警邮件发送

            # 重置次数
            server.hset(name=redis_name, key=spider_name, value=1)
            print('redis reset')
        else:
            curr_num += 1  # 添加一次新的记录
            server.hset(name=redis_name, key=spider_name, value=curr_num)


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


def account_band_judge(server, spider_name, need=defaults.NEED_ACCOUNT_BAND_JUDGE):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if need:
                st = time.time()
                func(*args, **kwargs)
                #  增加账号被封预警，采用run运行时长判断
                dur_time = time.time() - st
                if dur_time < defaults.DUR_TIME:
                    record_low_run_time(server, spider_name)
            else:
                func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == '__main__':
    print(defaults.SAVE_PID_FILES)
    print(defaults.REDIS_RECORD_NAME)
