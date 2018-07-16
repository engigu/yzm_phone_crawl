import logging  # 引入logging模块
import os
import time

import defaults

#
# import configparser
#
# cf  = configparser.ConfigParser().read('defaults.py')

SAVE_LOG = defaults.SAVE_LOG
LEVEL = defaults.LOG_LEVEL

maps = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'CRITICAL': logging.CRITICAL,
}

# def set_name(name):
#     return name

if not SAVE_LOG:
    def Logger(set_name=None):
        logging.basicConfig(level=maps.get(LEVEL),
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        logger = logging
        return logger

else:
    def Logger(set_name=None):
        # 第一步，创建一个logger
        logger = logging.getLogger()
        logger.setLevel(maps.get(LEVEL))  # Log等级总开关
        # 第二步，创建一个handler，用于写入日志文件
        tm = time.strftime('%Y_%m_%d__%H_%M', time.localtime(time.time()))
        log_path = defaults.LOG_PATH
        log_name = defaults.LOG_NAME % {'name': set_name, 'time': tm}
        logfile = os.path.join(log_path, log_name)
        print(logfile)
        fh = logging.FileHandler(logfile, mode='w')
        fh.setLevel(maps.get(LEVEL))  # 输出到file的log等级的开关
        # 第三步，定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        # 第四步，将logger添加到handler里面
        logger.addHandler(fh)
        return logger

# class Logger(object):
#
#     def __init__(self):
#
#         self.level = defaults.LOG_LEVEL
#         self.save_log =defaults.SAVE_LOG
#
#     def __new__(cls, *args, **kwargs):
#
#         return super(Logger,cls).__new__(cls, *args, **kwargs)

if __name__ == '__main__':
    logger = Logger()
    logger.info('fasdddfa')
