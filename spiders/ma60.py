import hashlib
import os
import re
import signal
import sys
import time

import requests
from retrying import retry

sys.path.append("..")

import defaults, logger, utils
from BloomFilterRedis_ex.BloomfilterOnRedis import BloomFilterRedis
from BloomFilterRedis_ex.connection import bloom_filter_from_defaults

spider_name = os.path.split(__file__)[1].split('.')[0]
logger = logger.Logger(spider_name)

full_PID_file_name = os.path.join(defaults.PIDS, defaults.PID_FILE_NAME) \
                     % {'spider_name': spider_name, 'tm': defaults.TM}
full_data_file_name = os.path.join(defaults.DATA_PATH, defaults.DATA_FILE_NAME) \
                      % {'spider_name': spider_name, 'tm': defaults.TM}

exit_signal = False
itemId = '13242B3AA4C6046'
RETRY_TIMES = 5  # 网络请求超时重试次数
API_URL = 'http://sms.60ma.net/'


class Ma60Crawl(object):  # 60接码
    name = 'ma60'

    def __init__(self):
        self.user = defaults.USER
        self.pass_ = defaults.PASS
        self.token = self._get_token()
        self.redis_server = bloom_filter_from_defaults(defaults.BLOOM_REDIS_URL)
        self.bf_server = BloomFilterRedis(server=self.redis_server, key=defaults.BLOOM_KEY, blockNum=1)
        self.fp = open(full_data_file_name, 'w', encoding='utf-8')

    def _get_token(self):
        params = {
            'cmd': 'login',
            'encode': 'utf-8',
            'username': self.user,
            'password': hashlib.md5(self.pass_.encode()).hexdigest(),
            'dtype': 'json',
            # 'Developer': 'cvZpfUej8AVQSZPa31W5Lw%3d%3d'
        }
        login_url = API_URL + 'loginuser'
        r = requests.get(login_url, params=params).json()
        self.userID = r['Return']['UserID']
        # self.userKey = r['Return']['UserKey']
        return r['Return']['UserKey']

    @retry(stop_max_attempt_number=RETRY_TIMES)
    def get_phone(self):
        params = {
            'cmd': 'gettelnum',
            'encode': 'utf-8',
            'dtype': 'json',
            'userid': self.userID,
            'userkey': self.token,
            'docks': itemId,

        }
        get_phone_url = API_URL + 'newsmssrv'
        r = requests.get(get_phone_url, params=params)
        return r.content.decode()

    @retry(stop_max_attempt_number=RETRY_TIMES)
    def release_url(self, phone):  # 释放手机号码
        params = {
            'cmd': 'freetelnum',
            'encode': 'utf-8',
            'dtype': 'json',
            'userid': self.userID,
            'userkey': self.token,
            'docks': itemId,
            'telnum': phone,

        }
        release_url = API_URL + 'newsmssrv'
        r = requests.get(release_url, params=params)
        return r.content.decode()

    # @retry(stop_max_attempt_number=RETRY_TIMES)
    # def check_out(self):  # 平台要求登出账号
    #     logout_url = API_URL + 'reg/loginOut?token=%s' % self.token
    #     r = requests.get(logout_url)
    #     # print(r.content.decode())
    #     return r.content.decode()

    def _extract_phone(self, raw):
        return re.findall(r'\d{11}', raw)

    def run(self):
        # # 保存一下进程pid
        # utils.save_pid(full_PID_file_name)
        # record_msg('启动 -> 保存pid文件成功')

        while True:
            global exit_signal
            if exit_signal:  # 退出信号
                self.fp.close()  # 结束退出
                res = utils.remove_pid_file(full_PID_file_name)
                record_msg(res[1] + ' <- 使用signal退出')
                break

            # 取号
            phone_ = self.get_phone()
            record_msg('接码平台取号返回 -> %s' % phone_)

            # if 'Session 过期' in phone_:  # 解决过一段时间 Session 过期
            #     self.token = self._get_token()
            #     record_msg(phone_)

            # 账户异常退出
            res = utils.return_phone_error_check(phone_)
            if res[0]:
                record_msg('账户异常退出，返回 -> %s -> %s' % (phone_, res[1]))
                res = utils.remove_pid_file(full_PID_file_name)
                record_msg('%s <- 账户异常退出' % res[1])
                break

            phone_list = self._extract_phone(phone_)
            if phone_list:
                for phone in phone_list:
                    phone_dict = {}
                    phone_dict['phone'] = phone
                    phone_dict['source'] = Ma60Crawl.name
                    # print(phone_dict)
                    record_msg(str(phone_dict))
                    if not self.bf_server.is_exists(phone):
                        self.fp.write(str(phone_dict) + '\n')
                        self.fp.flush()
                    else:
                        record_msg('过滤了重复手机号码 -> %s' % phone_dict)

                    # 释放手机号码
                    res = self.release_url(phone)
                    record_msg('释放手机号 -> %s' % res)

            time.sleep(defaults.DOWNLOAD_DELAY)

    def __del__(self):
        pass


def record_msg(msg):
    logger.info(msg)
    print(msg)


def quit(signum, frame):
    global exit_signal
    exit_signal = True
    res = utils.remove_pid_file(full_PID_file_name)
    record_msg(res[1] + ' <- 从sys.exit退出')
    sys.exit()


signal.signal(signal.SIGINT, quit)  # 退出信号注册
signal.signal(signal.SIGTERM, quit)

if __name__ == '__main__':
    # logging.lev
    T = Ma60Crawl()
    T.run()
    # print(T._get_token())
    # print(T.check_out())
