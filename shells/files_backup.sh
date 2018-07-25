#!/bin/bash

python_env='/root/.virtualenvs/sp/bin/python'

data_bak='../data_bak'


# 最终效果是
# 1. 复制data/文件下所有抓取数据文件，到data_rollback/回滚文件夹下
# 2. 到data_rollback/文件夹下合并成一个数据文件(one_xxxx.txt)
# 3. 到logs/文件夹下合并成一个数据文件(logs_xxxx.tar.gz)
# 4. 将两个文件移到data_bak/最终数据文件夹下

cd ../data_rollback/
rm *.txt        # 删掉上次的回滚数据(一天的周期)
cp ../data/* ./

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
mv one_${t}.bak $data_bak/$file_name

# 备份logs文件
cd ../logs/
tar_file=logs_${t}.tar.gz
tar -zcf ${tar_file} ./*.log
# 上线去掉注释
# rm *.log
mv ${tar_file} $data_bak/

