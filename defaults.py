#
#
#
#
import os
import time

# 统一时间戳
TM = time.strftime('%Y_%m_%d__%H_%M', time.localtime(time.time()))
# 根目录绝对路径
# ROOT_PATH = os.path.split(__file__)[0]
ROOT_PATH = '/home/workspace/DATA/yangmao_phone'

# 默认账号密码
USER = 'ztsp123456'
PASS = 'ztsp123456'

# 安全密码
SEC_PASS = 'ztsp123'

# 时间间隔
GET_PHONE_DELAY = 0.8
RELEASE_DELAY = 0.8

# pid files path
SAVE_PID_FILES = False  # 暂时不开启记录pid文件
PIDS = os.path.join(ROOT_PATH, 'pids/')
PID_FILE_NAME = '%(spider_name)s_%(tm)s.pid'

# fp path
DATA_PATH = os.path.join(ROOT_PATH, 'data/')  # 保存的数据
DATA_FILE_NAME = '%(spider_name)s_%(tm)s.txt'

# bloom filter
BLOOM_REDIS_URL = 'redis://localhost:6379/1'
BLOOM_KEY = 'bloom_yangmao_phone:%(no)s'
# option config
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
SPIDERS_EXCLUDE_LISTS = ['demo.py', 'pre.py', '__init__.py', 'main.py', 'pycharm', '<defunct>', 'toone.py',
                         '/opt/pycharm-2018.1.3/helpers/pydev/pydevconsole.py']
PYTHON_INTERPRETER_PATH = '/root/.virtualenvs/sp/bin/python'  # python解释器路径
SPIDERS_PATH = os.path.join('/home/workspace/yangmao', 'spiders/')
HEART_BEAT_TIME = 60 * 10  # 心跳时间，检测已经停止的spider，启动spider，默认为秒

# 账户被封预警
NEED_ACCOUNT_BAND_JUDGE = True
DUR_TIME = 10  # 低运行时长判定阈值(秒)
WARNING_TIMES = 20  # 低运行时长次数阈值
REDIS_RECORD_NAME = 'yangmao_low_run_time_record_map'  # redis中存储的记录名

# 邮箱信息(base64编码)
MAIL_USER = b'dG90YWxjaGVja0BzaW5hLmNvbQ=='  # 邮箱账号
MAIL_PASS = b"Z3ExOTk0MDUwNw=="  # 邮箱密码
TO_USERS_LIST = [b"c2F5aGV5YUBxcS5jb20="]  # 收件人邮箱列表
