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

### `spiders`文件夹下文件状态

- `pre.py`文件为预上线代码，支持其他spiders运行时上线新spider测试，(测试记得注释掉bloom过滤代码，以免影响生产
  环境过滤)，ok以后，`cp pre.py xxx(newSpiderName).py`，到达心跳间隔，自动会启动
- `demo.py`为功能测试文件
- `_xxx(spider_name).py` 下划线开头的是上线后代码后期异需要整改的文件


# 配置

- 配置文件在`defaults.py`


# Other

- 项目目前采用单线程，接码平台借口也不适合用多线程
- 网络请求目前采用`requests`，也未封装成下载器，尚待改进
- 未根据pids文件夹pid文件判断运行，实测效果很不理想，改调用shell获取pid，暂时未注释掉相关代码


### 平台

- [米粒](http://www.mili02.com/)   [集码](www.jima99.com)    [极速接码](http://jsjmpt.com/index.html)
- [51快码](http://www.51kmf.com/ )    [60码](http://www.60ma.net/)    [麦子云](http://www.maiziyzm.com)
- [神话](http://115.28.184.182:8000/login.html)    [淘码](http://w6888.cn/)    [thewolf](http://www.yyyzmpt.com/)
- [外星码](http://www.waixing666.com/oszc.html)    [星光码](http://120.79.137.205/oszc.html) [讯码](http://xunma.net/)
- [一码](http://yima998.com//oszc.html)    [柚子码](http://www.yzm9.com/homepage.html)    [YZ码](http://www.yzm8888.cn/oszc.html)
- [E云]( http://www.ema666.com/)    [千万码](http://kkk.yika66.com:8000/)    [来码](http://jiemapingtai.cn/index.html)
- [共享国际](http://www.gx-gj.com/login.aspx)    [云码](http://www.yzm7.com/userManage/Index.aspx)