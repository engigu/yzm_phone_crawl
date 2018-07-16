import os
import random
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
itemId = '2693'
RETRY_TIMES = 5  # 网络请求超时重试次数
API_URL = 'http://api.yyyzmpt.com/index.php/'

USER = 'ztsp1234567'
PASS = 'ztsp123456'


class TheWolfCrawl(object):  # thewolf接码
    name = 'thewolf'
    redis_server = bloom_filter_from_defaults(defaults.BLOOM_REDIS_URL)

    def __init__(self):
        self.user = USER
        self.pass_ = PASS
        self.req_session = requests.session()
        self.token = self._get_token()
        self.bf_server = BloomFilterRedis(server=self.redis_server, key=defaults.BLOOM_KEY, blockNum=1)
        self.fp = open(full_data_file_name, 'w', encoding='utf-8')

    def _get_token(self):
        params = {
            'backurl': 'http',
            'user': self.user,
            'steplogin': '2',
            'password': self.pass_,
            'remember': '1',
            'x': '42',
            'y': '16',
        }
        login_url = 'http://thewolf.yyyzmpt.com/reg.php?act=login'
        r = self.req_session.post(login_url, data=params)
        # token = r.json()
        return r.cookies, r.content.decode()

    @retry(stop_max_attempt_number=RETRY_TIMES)
    def get_phone(self):
        params = {
            'api': 'get_number',
            'tp': '1',
            't': '1',
            'pid': itemId,
        }
        get_phone_url = 'http://thewolf.yyyzmpt.com/api_getsms.php'
        r = self.req_session.post(get_phone_url, data=params)
        return str(re.findall(r'("qh_number":"\d{11}")', r.content.decode()))

    @retry(stop_max_attempt_number=RETRY_TIMES)
    def release_url(self, phone):  # 释放手机号码
        params = {
            'api': 'complete_number',
            'get_number': phone,
            'tp': '1',
            'success': str(random.randint(7, 10)),
        }
        release_url = 'http://thewolf.yyyzmpt.com/api_getsms.php'
        r = self.req_session.post(release_url, data=params)
        return r.content.decode()

    def _extract_phone(self, raw):
        return re.findall(r'\d{11}', raw)

    @utils.need_save_pid_files(pid_files_path=full_PID_file_name)
    @utils.account_band_judge(server=redis_server, spider_name=spider_name)
    def run(self):
        global exit_signal
        while True:
            if exit_signal:  # 退出信号
                self.fp.close()  # 结束退出
                record_msg(' <- 使用signal退出')
                break

            # 取号
            phone_ = self.get_phone()
            record_msg('接码平台取号返回 -> %s' % phone_)

            if 'Session 过期' in phone_:  # 解决过一段时间 Session 过期
                self.token = self._get_token()
                record_msg(phone_)

            # 账户异常退出
            res = utils.return_phone_error_check(phone_)
            if res[0]:
                record_msg('账户异常退出，返回 -> %s -> %s' % (phone_, res[1]))
                break

            phone_list = self._extract_phone(phone_)
            if phone_list:
                for phone in phone_list:
                    phone_dict = {}
                    phone_dict['phone'] = phone
                    phone_dict['source'] = TheWolfCrawl.name
                    # print(phone_dict)
                    record_msg(str(phone_dict))
                    if not self.bf_server.is_exists(phone):
                        self.fp.write(str(phone_dict) + '\n')
                        self.fp.flush()
                    else:
                        record_msg('过滤了重复手机号码 -> %s' % phone_dict)

                    time.sleep(defaults.RELEASE_DELAY)        

                    # 释放手机号码
                    res = self.release_url(phone)
                    record_msg('释放手机号 -> %s' % res)

            time.sleep(defaults.GET_PHONE_DELAY)

    def __del__(self):
        pass


def record_msg(msg):
    logger.info(msg)
    print(msg)


@utils.need_remove_pid_files(pid_files_path=full_PID_file_name)
def quit(signum, frame):
    global exit_signal
    exit_signal = True
    record_msg(' <- 从sys.exit退出')
    sys.exit()


signal.signal(signal.SIGINT, quit)  # 退出信号注册
signal.signal(signal.SIGTERM, quit)

if __name__ == '__main__':
    T = TheWolfCrawl()
    T.run()
