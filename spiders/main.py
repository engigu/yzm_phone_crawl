import os
import signal
import sys
import time
from multiprocessing import Process
from subprocess import call, getstatusoutput

sys.path.append("..")
import defaults

#
# 忽略文件配置，pre.py为新增待上线测试spider，测试完毕后改成其他名字会自动部署(在启动heart_beat的情况下)
exclude_list = defaults.SPIDERS_EXCLUDE_LISTS
other_list = ['<defunct>', 'main.py']  # 残余主进程名字
python_interpreter_path = defaults.PYTHON_INTERPRETER_PATH  # python解释器路径
spiders_path = defaults.SPIDERS_PATH
heart_beat_time = defaults.HEART_BEAT_TIME  # 心跳时间，检测已经停止的spider，启动spider

py_files_list = [i for i in os.listdir(spiders_path) if i.endswith('.py')]
spiders_list = [i for i in py_files_list if i not in exclude_list and not i.startswith('_')]  # 所有的spider文件，全局变量

# spiders_list = ['demo.py']
# print(spiders_list)


def run(spider):
    cmd = [python_interpreter_path, spider]
    call(cmd)


def start_all_spiders(spiders_list, join=True):
    ps = []
    for spider in spiders_list:
        print('starting spider ->  ', spider)
        p = Process(target=run, args=(spider,))
        ps.append(p)

    for p in ps:
        p.start()

    if join:
        for p in ps:
            p.join()


def get_pids_from_ps():
    res = getstatusoutput("ps aux | grep python | grep -v grep | awk '{print $2,$11,$12,$13}'")
    # print(res)
    if res[1] == '':  # 查找信息为空
        return False
    # total_spiders_list = [ tmp for line in res[1].split('\n') for tmp in line.split(' ') if tmp[2] not in exclude_list]
    online_spider_list = []
    other_spider_list = []
    for line in res[1].split('\n'):
        tmp = line.split(' ')
        if tmp[2] not in exclude_list:
            online_spider_list.append(tmp)
        if tmp[2] in other_list:  # 必须kill的进程，否则会反复重启进程
            other_spider_list.append(tmp)
    return online_spider_list, other_spider_list


def heart_beat():
    online_spider_list, other_spider_list = get_pids_from_ps()
    stopped_spider_list = [spider for spider in spiders_list if spider not in str(online_spider_list)]
    print('stopped_spider_list', stopped_spider_list)
    print('len', len(stopped_spider_list))
    if stopped_spider_list:
        start_all_spiders(stopped_spider_list, join=False)


def _sort_files_name(files_list):
    """
    分割文件列表，分成两个文件列表，一个是当前运行spider最新文件的列表，另一个是历史文件

    :param files_list: 全部文件列表
    :return: 返回不是当前运行spider的文件列表
    """
    sorted_list = sorted(files_list)

    # 单个spider最新时间的文件列表
    tmp = {i.split('_')[0]: '_'.join(i.split('_')[1:]) for i in sorted_list}
    latest_time_files_list = sorted(['_'.join([k, v]) for k, v in tmp.items() if k not in exclude_list])
    return [i for i in files_list if i not in latest_time_files_list if i not in exclude_list]


def remove_empty_files_under_folder(folder_path):
    files_list = os.listdir(folder_path)
    sorted_files_name = _sort_files_name(files_list)
    for file in sorted_files_name:
        with open(folder_path + file, 'r') as  f:
            con = f.read()
        if not con:
            print('remove -> ', folder_path + file)
            os.remove(folder_path + file)


def refresh_spiders_list():
    global spiders_list
    # 重复检测新spider文件
    py_files_list = [i for i in os.listdir(spiders_path) if i.endswith('.py')]
    spiders_list = [i for i in py_files_list if i not in exclude_list and not i.startswith('_')]  # 所有的spider文件


def main():
    len_argv = len(sys.argv)
    if len_argv == 1:  # 提示信息
        print('\nUsage:   python main.py [start_all|heart_beat|pids]\n')
        print('start_all\t-->\t启动所有抓取任务')
        print('heart_beat\t-->\t启动心跳重试')
        print('pids\t\t-->\t管理当前抓取任务\n')

    elif len_argv == 2:
        arg = sys.argv[1]
        if arg == 'start_all':
            start_all_spiders(spiders_list)
            pass

        elif arg == 'heart_beat':
            time.sleep(0.5)
            while True:
                refresh_spiders_list()
                heart_beat()
                remove_empty_files_under_folder(defaults.DATA_PATH)  # 移除多余的data与log文件
                remove_empty_files_under_folder(defaults.LOG_PATH)
                time.sleep(heart_beat_time)

        elif arg == 'pids':
            while True:
                refresh_spiders_list()
                time.sleep(0.2)
                online_spider_list, other_spider_list = get_pids_from_ps()
                stopped_spider_list = [spider for spider in spiders_list if spider not in str(online_spider_list)]

                # 打印任务
                if not online_spider_list:
                    print('\n暂无任务\n')
                    break
                else:
                    print('\n当前运行中的任务列表：')
                    for spider in online_spider_list:
                        line = '++ %d %s' % (online_spider_list.index(spider), ' '.join(spider))
                        print(line)
                print('\n当前已经停掉的任务列表(心跳间隔%ds)：' % heart_beat_time)
                if not stopped_spider_list:
                    print('\n暂无任务\n')
                else:
                    for spider in stopped_spider_list:
                        line = '-- %d %s' % (stopped_spider_list.index(spider), spider)
                        print(line)

                # 结束进程
                select = input('输入要干掉的任务序号(a:所有，q:退出)：')
                if select.isdigit():
                    pid = online_spider_list[int(select)][0]
                    call(['kill', str(pid)])
                elif select.upper() == 'Q':
                    break
                elif select.upper() == 'A':
                    q = input('结束所有任务，二次确认(a)：')
                    if q.upper() == 'A':
                        for spider in online_spider_list:
                            call(['kill', str(spider[0])])
                        time.sleep(1)
                        # kill掉残余主进程，不然会反复重启
                        for other in other_spider_list:
                            call(['kill', str(other[0])])
                    else:
                        print('未结束退出')
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
    # print(spiders_list)
    # print(len(spiders_list))
    # print(spiders_path)
    # print(os.getcwd())
    # remove_empty_files_under_folder('./data_rollback/')
