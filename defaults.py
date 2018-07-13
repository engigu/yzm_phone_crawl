#
#
#
#
import os
import time

# 统一时间戳
TM = time.strftime('%Y_%m_%d__%H_%M', time.localtime(time.time()))
# 根目录绝对路径
ROOT_PATH = os.path.split(__file__)[0]

# 账号密码
USER = 'ztsp123456'
PASS = 'ztsp123456'

# 安全密码
SEC_PASS = 'ztsp123'

# 下载时间间隔
DOWNLOAD_DELAY = 0.8

# pid files path
SAVE_PID_FILES = False  # 开启记录pid文件
PIDS = os.path.join(ROOT_PATH, 'pids/')
PID_FILE_NAME = '%(spider_name)s_%(tm)s.pid'

# fp path
DATA_PATH = os.path.join(ROOT_PATH, 'data/')  # 保存的数据
DATA_FILE_NAME = '%(spider_name)s_%(tm)s.txt'

# bloom filter
BLOOM_REDIS_URL = 'redis://localhost:6379/1'
BLOOM_KEY = 'bloom_yangmao_phone:%(no)s'

# BLOOM_REDIS_HOST = 'localhost'
# BLOOM_REDIS_PORT = 6379
# BLOOM_REDIS_DB = 9

BIT_SIZE = 1 << 30
BLOCK_NUM = 1

# log
SAVE_LOG = True
LOG_LEVEL = 'INFO'
LOG_PATH = os.path.join(ROOT_PATH, 'logs/')
LOG_NAME = '%(name)s_%(time)s.log'

# spiders env config
# 忽略文件list配置，pre.py为新增待上线测试spider，测试完毕后改成其他名字会自动部署(在启动heart_beat的情况下)
SPIDERS_EXCLUDE_LISTS = ['demo.py', 'pre.py', '__init__.py', 'main.py', 'pycharm', '<defunct>',
                         '/opt/pycharm-2018.1.3/helpers/pydev/pydevconsole.py']
PYTHON_INTERPRETER_PATH = '/home/tk/.virtualenvs/sp/bin/python'  # python解释器路径
SPIDERS_PATH = os.path.join(ROOT_PATH, 'spiders/')
HEART_BEAT_TIME = 60 * 10  # 心跳时间，检测已经停止的spider，启动spider，默认为秒
