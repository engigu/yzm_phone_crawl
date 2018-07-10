# 简介

该项目主要用来抓取接码平台的手机号，使用基于redis的bloom filter
接码号码平台现在属于黑色产业，号码被用来接受各个网站的验证码，平台上抓取的手机号可以百分百认定为羊毛党手机号。


# 运行环境
- python3
- redis
- requests


# 食用方法

- 先`down`或者`clone`下来
- 在项目根目录新建 `data`、`logs`、`pids` 三个文件夹
- 最后`python3 spiders/main.py`， 有两个运行参数选择
   - `start_all` 一次开启所有任务
   - `pids` 根据`pid`情况管理运行任务
   - `heart_beat` 心跳检测停止的`spider`，重新启动`spider`，默认时长`5 min`，在`main.py`设置
- 支持其他spiders运行时上线新spider，`spiders`文件夹里`pre.py`文件为预上线代码，测试(测试记得注释掉bloom过滤代码，以免影响生产
  环境过滤)，ok以后，`cp pre.py xxx(newSpiderName).py`，到达心跳间隔，自动会启动

# 配置

- 配置文件在`defaults.py`


# Other

- 项目目前采用单线程，接码平台借口也不适合用多线程
- 网络请求目前采用`requests`，也未封装成下载器，尚待改进
- 未根据pids文件夹pid文件判断运行，实测效果很不理想，改调用shell获取pid，暂时未注释掉相关代码
