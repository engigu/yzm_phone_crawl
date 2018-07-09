import os
import re
from multiprocessing import Process
from subprocess import call

#
#
#
# 配置
exclude_list = ['demo.py', '__init__.py', 'main.py']
python_interpreter_path = '/home/tk/.virtualenvs/sp/bin/python'  # 解释器路径
spiders_path = '.'

py_files_list = [i for i in os.listdir(spiders_path) if i.endswith('.py')]
spiders_list = [i for i in py_files_list if i not in exclude_list]

# spiders_list = ['demo.py']
print(spiders_list)


def run(spider):
    cmd = [python_interpreter_path, spider]
    call(cmd)


def start_all_spiders():
    ps = []

    for spider in spiders_list:
        p = Process(target=run, args=(spider,))
        ps.append(p)

    for p in ps:
        p.start()

    for p in ps:
        p.join()

        # os.system('%s %s' % (python_interpreter_path, spider))


def get_pids_from_ps():
    print(os.system('ps aux | grep python'))
    res = str(os.system('ps aux | grep python'))
    re.findall(r'(\d+)', res)


if __name__ == '__main__':
    start_all_spiders()
    # get_pids_from_ps()
