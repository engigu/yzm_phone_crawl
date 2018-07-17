#!/bin/bash

python_env='/home/tk/.virtualenvs/sp/bin/python'

cd ../spiders/

expect <<!!
set timeout 60
spawn $python_env main.py pids
expect "输入要干掉的任务序号(a:所有，q:退出)："
send "a\n"
expect "结束所有任务，二次确认(a)："
send "a\n"
expect eof
!!

exit