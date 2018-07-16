#!/bin/bash

expect <<!!
set timeout 60
spawn python3 shell_true.py shell
expect "确定输入a:"
send "a\r"
expect "二次确定输入b:"
send "b\r"
expect eof
!!
