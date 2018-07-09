import os

#
TO_ONE_FILE_NAME = 'one.txt'

print(os.listdir('.'))

all_files_list = os.listdir('.')

if TO_ONE_FILE_NAME in all_files_list:
    all_files_list.remove(TO_ONE_FILE_NAME)
if 'toone.py' in all_files_list:
    all_files_list.remove('toone.py')

i = 0
with open(TO_ONE_FILE_NAME, 'w') as f_o:
    for file_path in all_files_list:
        with open(file_path, 'r') as f_r:
            while True:
                line = f_r.readline()
                if not line:
                    break
                f_o.write(line)
                f_o.flush()
                i += 1
                print('current line no is', i)

print('total num is ', i)
