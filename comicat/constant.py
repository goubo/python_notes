from service import Service

# 程序退出状态,线程监测此状态后,程序处于等待退出状态

APPLICATION_EXIT = False

# 打开的tab页集合,记录页面的url用于区分
OPEN_TAB = []

# 全局业务主线程
SERVICE = Service()

# 加载的所有mod 保存mod对象

mod_dist = dict()

# 配置

# 本地数据
'''下载队列.key value ,url taskInfo'''
download_task_map = dict()

# 临时数据
'''查询缓存,mod解析的页面返回,统统缓存到这个对象中'''
temp = dict()
