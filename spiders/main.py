import os
import signal
import sys
import time
from multiprocessing import Process
from subprocess import call, getstatusoutput

#
# 配置
exclude_list = ['demo.py', '__init__.py', 'main.py', 'pycharm', '<defunct>',
                '/opt/pycharm-2018.1.3/helpers/pydev/pydevconsole.py']
python_interpreter_path = '/home/tk/.virtualenvs/sp/bin/python'  # 解释器路径
spiders_path = '.'
heart_beat_time = 60 * 5  # 心跳时间，检测已经停止的spider，启动spider

py_files_list = [i for i in os.listdir(spiders_path) if i.endswith('.py')]
spiders_list = [i for i in py_files_list if i not in exclude_list]  # 所有的spider文件

# spiders_list = ['demo.py']
# print(spiders_list)


def run(spider):
    cmd = [python_interpreter_path, spider]
    call(cmd)


def start_all_spiders(spiders_list):
    ps = []
    for spider in spiders_list:
        print('starting spider ->  ', spider)
        p = Process(target=run, args=(spider,))
        ps.append(p)

    for p in ps:
        p.start()

    for p in ps:
        p.join()


def get_pids_from_ps():
    res = getstatusoutput("ps aux | grep python| grep -v grep | awk '{print $2,$11,$12}'")
    # print(res)
    if res[1] == '':
        return False
    # total_spiders_list = [ tmp for line in res[1].split('\n') for tmp in line.split(' ') if tmp[2] not in exclude_list]
    online_spider_list = []
    for line in res[1].split('\n'):
        tmp = line.split(' ')
        if tmp[2] not in exclude_list:
            online_spider_list.append(tmp)
    return online_spider_list


def heart_beat():
    online_spider_list = get_pids_from_ps()
    stopped_spider_list = [spider for spider in spiders_list if spider not in str(online_spider_list)]
    if stopped_spider_list:
        start_all_spiders(stopped_spider_list)


def main():
    len_argv = len(sys.argv)
    if len_argv == 1:  # 提示信息
        print('Usage:')
        print()
        print('start_all\t-->\t启动所有抓取任务')
        print('heart_beat\t-->\t启动心跳重试')
        print('pids\t\t-->\t管理当前抓取任务')

    elif len_argv == 2:
        arg = sys.argv[1]
        if arg == 'start_all':
            start_all_spiders(spiders_list)
            pass

        elif arg == 'heart_beat':
            while True:
                heart_beat()
                time.sleep(heart_beat_time)

        elif arg == 'pids':
            while True:
                time.sleep(0.2)
                total_spiders_list = get_pids_from_ps()
                stopped_spider_list = [spider for spider in spiders_list if spider not in str(total_spiders_list)]

                # 打印任务
                if not total_spiders_list:
                    print('None')
                    break
                else:
                    print('当前运行中的任务列表：')
                    for spider in total_spiders_list:
                        line = '%d %s' % (total_spiders_list.index(spider), ' '.join(spider))
                        print(line)
                print('当前已经停掉中的任务列表：')
                if not stopped_spider_list:
                    print('None')
                else:
                    for spider in stopped_spider_list:
                        line = '%d %s' % (stopped_spider_list.index(spider), spider)
                        print(line)

                # 结束进程
                select = input('输入要干掉的任务序号(a:所有，q:退出)：')
                if select.isdigit():
                    pid = total_spiders_list[int(select)][0]
                    call(['kill', str(pid)])
                elif select.upper() == 'Q':
                    break
                elif select.upper() == 'A':
                    q = input('结束所有任务，二次确认(a)：')
                    if q.upper() == 'A':
                        for i in total_spiders_list:
                            call(['kill', str(i[0])])
                    else:
                        break
                else:
                    print('输入错误')
        else:
            print('参数错误')
    else:
        print('参数长度错误')


def quit(signum, frame):
    print('退出...')
    sys.exit()


signal.signal(signal.SIGINT, quit)  # 退出信号注册
signal.signal(signal.SIGTERM, quit)


if __name__ == '__main__':
    main()
