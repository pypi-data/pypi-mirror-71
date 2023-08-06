## 1. pip install nb_log
```
very sharp color display,monkey patch bulitin print  
and high-performance multiprocess safe roating file handler,
other handlers includeing dintalk ,email,kafka,elastic and so on 
  
1） 兼容性
使用的是python的内置logging封装的，返回的logger对象的类型是py官方内置日志的Logger类型，兼容性强，
保证了第三方各种handlers扩展数量多和方便，和一键切换现有项目的日志。

比如logru和logbook这种三方库，完全重新写的日志，
它里面主要被用户使用的logger变量类型不是python内置Logger类型，
造成logger说拥有的属性和方法有的不存在或者不一致，这样的日志和python内置的经典日志兼容性差，
只能兼容（一键替换logger类型）一些简单的debug info warning errror等方法，。

2） 日志记录到多个地方
内置了一键入参，每个参数是独立开关，可以把日志同时记录到8个常用的地方的任意几种，
包括 控制台 文件 钉钉 邮件 mongo kafka es 等等 。

3） 日志命名空间独立，采用了多实例logger，按日志命名空间区分。
命名空间独立意味着每个logger单独的日志界别过滤，单独的控制要记录到哪些地方。

logger_aa = LogManager('aa').get_logger_and_add_handlers(10，log_filename='aa.log')
logger_bb = LogManager('bb').get_logger_and_add_handlers(30，is_add_stream_handler=False,
ding_talk_token='your_dingding_token')
logger_cc = LogManager('cc').get_logger_and_add_handlers(10，log_filename='cc.log')

那么logger_aa.debug('哈哈哈')  
将会同时记录到控制台和文件aa.log中，只要debug及debug以上级别都会记录。

logger_bb.warning('嘿嘿嘿')   
将只会发送到钉钉群消息，并且logger_bb的info debug级别日志不会被记录，
非常方便测试调试然后稳定了调高界别到生产。

logger_cc的日志会写在cc.log中，和logger_aa的日志是不同的文件。

4） 对内置looging包打了猴子补丁，使日志永远不会使用同种handler重复记录

例如，原生的  

from logging import getLogger,StreamHandler
logger = getLogger('hi')
getLogger('hi').addHandler(StreamHandler())
getLogger('hi').addHandler(StreamHandler())
getLogger('hi').addHandler(StreamHandler())
logger.warning('啦啦啦')

明明只warning了一次，但实际会造成 啦啦啦 在控制台打印3次。
使用nb_log，对同一命名空间的日志，可以无惧反复添加同类型handler，不会重复记录。


5）支持日志自定义，运行此包后，会自动在你的python项目根目录中生成nb_log_config.py文件，按说明修改。
```

## 2. 最简单的使用方式,这只是演示控制台日志
###### 2.0）自动拦截改变项目中所有地方的print效果。（支持配置文件自定义关闭转化print）
###### 2.1）控制台日志变成可点击，精确跳转。（支持配置文件自定义修改或增加模板，内置了7种模板，部分模板生成的日志可以在pycharm控制台点击跳转）
###### 2.2）控制台日志根据日志级别自动变色。（支持配置文件关闭彩色或者关闭背景色块）

```python
from nb_log import LogManager

logger = LogManager('lalala').get_logger_and_add_handlers()

logger.debug('绿色')
logger.info('蓝色')
logger.warn('黄色')
logger.error('紫红色')
logger.critical('血红色')
print('print样式被自动发生变化')
```

## 3 文件日志
###### 3.1）这个文件日志的自定义filehandler是python史上性能最强大的 支持多进程下日志文件按大小自动切割。

在各种filehandler实现难度上 
单进程永不切割 <  多进程按时间切割 < 单进程按大小切割  << 多进程按大小切割

因为每天日志大小很难确定，如果每天所有日志文件以及备份加起来超过40g了，硬盘就会满挂了，所以nb_log的文件日志filehandler采用的是按大小切割，不使用按时间切割。

文件日志自动使用的是多进程安全切割的自定义filehandler，
logging包的RotatingFileHandler多进程运行代码时候，如果要实现向文件写入到规定大小时候并自动备份切割，win和linux都100%报错。

支持多进程安全切片的知名的handler有ConcurrentRotatingFileHandler，
此handler能够确保win和linux切割正确不出错，此包在linux使用的是高效的fcntl文件锁，
在win上性能惨不忍睹，这个包在win的性能在三方包的英文说明注释中，作者已经提到了。

nb_log是基于自动批量聚合，从而减少写入次数（但文件日志的追加最多会有1秒的延迟），从而大幅度减少反复给文件加锁解锁，
使快速大量写入文件日志的性能大幅提高，在保证多进程安全且排列的前提下，对比这个ConcurrentRotatingFileHandler
使win的日志文件写入速度提高100倍，在linux上写入速度提高10倍。

###### 3.2）演示文件日志，并且直接演示最高实现难度的多进程安全切片文件日志

```python
from multiprocessing import Process
from nb_log import LogManager

#指定log_filename不为None 就自动写入文件了，并且默认使用的是多进程安全的切割方式的filehandler。
#默认都添加了控制台日志，如果不想要控制台日志，设置is_add_stream_handler=False
#为了保持方法入场数量少，具体的切割大小和备份文件个数有默认值，
#如果需要修改切割大小和文件数量，在当前python项目根目录自动生成的nb_log_config.py文件中指定。
logger = LogManager('ha').get_logger_and_add_handlers(is_add_stream_handler=True,
log_filename='ha.log')

def f():
    for i in range(1000000000):
        logger.debug('测试文件写入性能，在满足 1.多进程运行 2.按大小自动切割备份 3切割备份瞬间不出错'
                    '这3个条件的前提下，验证这是不是python史上文件写入速度遥遥领先 性能最强的python logging handler')
       
if __name__ == '__main__':
    [Process(target=f).start() for _ in range(10)]
```

## 4 钉钉日志
```python
from nb_log import LogManager
logger4 = LogManager('hi').get_logger_and_add_handlers(is_add_stream_handler=True,
    log_filename='hi.log',ding_talk_token='your_dingding_token')
logger4.debug('这条日志会同时出现在控制台 文件 和钉钉群消息')
```

## 5 其他handler包括kafka日志，elastic日志，邮件日志，mongodb日志

按照get_logger_and_add_handler函数的入参说明就可以了，和上面的2 3 4中的写法方式差不多，都是一参 傻瓜式，设置了，日志记录就会记载在各种地方。

## 6 日志优先默认配置

只要项目任意文件运行了，带有import nb_log的脚本，就会在项目根目录下生成nb_log_config.py配置文件。
nb_log_config.py的内容如下，默认都是用#注释了，如果放开某项配置则优先使用这里的配置，否则使用nb_log_config_default.py中的配置。

配置示例如下：
```
如果反对日志有各种彩色，可以设置 DEFAULUT_USE_COLOR_HANDLER = False
如果反对日志有块状背景彩色，可以设置 DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = False
如果想屏蔽nb_log包对怎么设置pycahrm的颜色的提示，可以设置 WARNING_PYCHARM_COLOR_SETINGS = False
如果想改变日志模板，可以设置 FORMATTER_KIND 参数，只带了7种模板，可以自定义添加喜欢的模板
```

```python
import logging
ELASTIC_HOST = '127.0.0.1'
ELASTIC_PORT = 9200

KAFKA_BOOTSTRAP_SERVERS = ['192.168.199.202:9092']
ALWAYS_ADD_KAFKA_HANDLER_IN_TEST_ENVIRONENT = False

MONGO_URL = 'mongodb://myUserAdmin:mima@127.0.0.1:27016/admin'

DEFAULUT_USE_COLOR_HANDLER = True  # 是否默认使用有彩的日志。
DISPLAY_BACKGROUD_COLOR_IN_CONSOLE = True  # 在控制台是否显示彩色块状的日志。为False则不使用大块的背景颜色。
AUTO_PATCH_PRINT = True  # 是否自动打print的猴子补丁，如果打了后指不定，print自动变色和可点击跳转。
WARNING_PYCHARM_COLOR_SETINGS = True

DEFAULT_ADD_MULTIPROCESSING_SAFE_ROATING_FILE_HANDLER = False  # 是否默认同时将日志记录到记log文件记事本中。
LOG_FILE_SIZE = 100  # 单位是M,每个文件的切片大小，超过多少后就自动切割
LOG_FILE_BACKUP_COUNT = 3

LOG_LEVEL_FILTER = logging.DEBUG  # 默认日志级别，低于此级别的日志不记录了。例如设置为INFO，那么logger.debug的不会记录，只会记录logger.info以上级别的。
RUN_ENV = 'test'

FORMATTER_DICT = {
    1: logging.Formatter(
        '日志时间【%(asctime)s】 - 日志名称【%(name)s】 - 文件【%(filename)s】 - 第【%(lineno)d】行 - 日志等级【%(levelname)s】 - 日志信息【%(message)s】',
        "%Y-%m-%d %H:%M:%S"),
    2: logging.Formatter(
        '%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),
    3: logging.Formatter(
        '%(asctime)s - %(name)s - 【 File "%(pathname)s", line %(lineno)d, in %(funcName)s 】 - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),  # 一个模仿traceback异常的可跳转到打印日志地方的模板
    4: logging.Formatter(
        '%(asctime)s - %(name)s - "%(filename)s" - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s -               File "%(pathname)s", line %(lineno)d ',
        "%Y-%m-%d %H:%M:%S"),  # 这个也支持日志跳转
    5: logging.Formatter(
        '%(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),  # 我认为的最好的模板,推荐
    6: logging.Formatter('%(name)s - %(asctime)-15s - %(filename)s - %(lineno)d - %(levelname)s: %(message)s',
                         "%Y-%m-%d %H:%M:%S"),
    7: logging.Formatter('%(levelname)s - %(filename)s - %(lineno)d - %(message)s',"%Y-%m-%d %H:%M:%S"), # 一个只显示简短文件名和所处行数的日志模板
}

FORMATTER_KIND = 5  # 如果get_logger_and_add_handlers不指定日志模板，则默认选择第几个模板
```

## 7. 各種日志截圖

钉钉

![Image text](https://i.niupic.com/images/2020/05/12/7OSE.png)

控制台日志模板之一

![Image text](https://i.niupic.com/images/2020/05/12/7OSF.png)

控制台日子模板之二

![Image text](https://i.niupic.com/images/2020/05/12/7OSG.png)

邮件日志

![Image text](https://i.niupic.com/images/2020/05/12/7OSH.png)

文件日志

![Image text](https://i.niupic.com/images/2020/05/12/7OSI.png)

elastic日志

![Image text](https://i.niupic.com/images/2020/05/12/7OSK.png)

mongo日志

![Image text](https://i.niupic.com/images/2020/05/12/7OSL.png)
 