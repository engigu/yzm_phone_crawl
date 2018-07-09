import os
import re
import signal
import sys
import time

sys.path.append("..")

import requests
from retrying import retry

import defaults, logger, utils
from BloomFilterRedis_ex.BloomfilterOnRedis import BloomFilterRedis
from BloomFilterRedis_ex.connection import bloom_filter_from_defaults

spider_name = os.path.split(__file__)[1].split('.')[0]
logger = logger.Logger(spider_name)

full_PID_file_name = os.path.join(defaults.PIDS, defaults.PID_FILE_NAME) \
                     % {'spider_name': spider_name, 'tm': defaults.TM}
full_data_file_name = os.path.join(defaults.DATA_PATH, defaults.FP_MAPS[spider_name])

exit_signal = False
RETRY_TIMES = 5  # 网络请求超时重试次数
ItemId = '6'  # 企鹅号-自媒体-腾讯开放内容平台
API_URL = 'http://47.75.112.7:9180/service.asmx/'


class YiMaCrawl(object):  # YZ验证码
    name = 'yima'

    def __init__(self):
        self.user = defaults.USER
        self.pass_ = defaults.PASS
        self.token = self._get_token()
        print(self.token)
        self.redis_server = bloom_filter_from_defaults(defaults.BLOOM_REDIS_URL)
        self.bf_server = BloomFilterRedis(server=self.redis_server, key=defaults.BLOOM_KEY, blockNum=1)
        self.fp = open(os.path.join(defaults.DATA_PATH, defaults.FP_MAPS[YiMaCrawl.name]),
                       'w', encoding='utf-8')

    def _get_token(self):
        params = {
            'name': self.user,
            'psw': self.pass_,
        }
        login_url = API_URL + 'UserLoginStr'
        r = requests.get(login_url, params=params)
        token = r.content.decode().split('&')[0]
        return token

    @retry(stop_max_attempt_number=RETRY_TIMES)
    def get_phone(self):
        params = {
            'xmid': ItemId,  # 必填,项目需要先收藏
            'token': self.token,  # 必填
            'sl': '1',
            'lx': '0',
            'ks': '0',
            'a1': '',
            'a2': '',
            'pk': '',
            'rj': '',
        }
        get_phone_url = API_URL + 'GetHM2Str'
        r = requests.get(get_phone_url, params=params)
        return r.content.decode()

    @retry(stop_max_attempt_number=RETRY_TIMES)
    def release_url(self, phone):  # 释放手机号码
        params = {
            'token': self.token,
            'hm': phone
        }
        release_url = API_URL + 'sfHmStr'
        r = requests.get(release_url, params=params)
        return r.content.decode()

    def _extract_phone(self, raw):
        return re.findall(r'\d{11}', raw)

    def run(self):
        # 保存一下进程pid
        utils.save_pid(full_PID_file_name)
        record_msg('启动 -> 保存pid文件成功')

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

            # 账户异常退出
            res = utils.return_phone_error_check(phone_)
            if res[0]:
                record_msg('账户异常退出，返回 -> %s -> %s' % (phone_, res[1]))
                res = utils.remove_pid_file(full_PID_file_name)
                record_msg('%s <- 账户异常退出' % res[1])
                break

            # if 'Session 过期' in phone_:  # 解决过一段时间 Session 过期
            #     self.token = self._get_token()
            #     self.logger.warning(phone_)

            phone_list = self._extract_phone(phone_)
            if phone_list:
                for phone in phone_list:
                    phone_dict = {}
                    phone_dict['phone'] = phone
                    phone_dict['source'] = YiMaCrawl.name
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
        # self.fp.close()
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
    Y = YiMaCrawl()
    Y.run()
