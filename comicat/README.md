# 漫画下载阅读器

基于pyqt6,

`main.py` 进入,`ui_windows.py` 为 界面  
service 为业务模块,和gui线程同级,爬虫\下载放到单独线程中,通过回调函数通过service调用ui中的钩子函数,触发插槽更新ui.  
mods模块为爬虫拓展,继承实现`website_interface.py`接口,service模块init自动装载对象.

主界面搜索框回车搜索,调用service.search函数,遍历爬虫mod进行搜索,mod解析数据通过回调到主线程,更新漫画列表ui.  
点击漫画标题,加载漫画详情和章节目录.
选择章节,点击下载,解析章节中图片列表,加入下载线程池队列.同时更新ui

搜索,解析章节,解析图片添加下载任务为多线程异步操作,ui为动态更新,没有loading,根据网速耐心等待







