#!/bin/bash

python_env='/home/tk/.virtualenvs/sp/bin/python'

data_bak='../data_bak'

cd ../data_rollback/
# cd ../data/
# 备份数据到回滚文件夹
# cp ./* ../data_rollback/

# 取时间
t=`date +%Y_%m_%d__%H_%M`
echo $t

# 合并数据文件
$python_env toone.py $t

file_name=one_${t}.txt
echo $file_name

# 改名删除其他数据文件
mv $file_name one_${t}.bak
# 上线去掉注释
rm *.txt
mv one_${t}.bak $data_bak/$file_name

# 备份logs文件
cd ../logs/
tar_file=logs_${t}.tar.gz
tar -zcf ${tar_file} ./*.log
# 上线去掉注释
# rm *.log
mv ${tar_file} $data_bak/

