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
DOWNLOAD_DELAY = 0.2

# pid files path
PIDS = os.path.join(ROOT_PATH, './pids')
PID_FILE_NAME = '%(spider_name)s_%(tm)s.pid'

# fp path
DATA_PATH = os.path.join(ROOT_PATH, './data')  # 保存的数据

# fp name maps
FP_MAPS = {
    'demo': 'demo_%s.txt' % TM,
    'shenhua': 'shenhua_%s.txt' % TM,
    'xunma': 'xunma_%s.txt' % TM,
    'yima': 'yima_%s.txt' % TM,
    'jisujiema': 'jisujiema_%s.txt' % TM,
    'kuaima51': 'kuaima51_%s.txt' % TM,
    'xingguang': 'xingguang_%s.txt' % TM,
    'yzma': 'yzma_%s.txt' % TM,
    'taoma': 'taoma_%s.txt' % TM,
    'jima': 'jima_%s.txt' % TM,
    'maiziyun': 'maiziyun_%s.txt' % TM,
}

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
LOG_PATH = 'logs'
LOG_NAME = '%(name)s_%(time)s.log'
