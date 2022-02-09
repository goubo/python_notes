import constant
from download_task import DownloadTask
from entity import ComicInfo, ChapterInfo
from mods.website_interface import WebsiteInterface
from threadpool import BoundedThreadPoolExecutor
from util import find_database_access_class


def set_class_name(comic: ComicInfo, class_name, key, callback):
    """
    填充modName
    :param key: 搜索key,判断渲染线程是否是本线程
    :param comic: 漫画实体对象
    :param class_name: modName
    :param callback: 回调函数,返回漫画实体
    :return:
    """
    comic.service = class_name
    comic.searchKey = key
    callback(comic)


def search_thread(k, callback):
    """
    搜索线程
    如果缓存中有,直接返回,否则调用所有的mod,进行搜索
    :param k: 关键字
    :param callback:回调
    :return:
    """
    if k in constant.temp:
        for item in constant.temp.get(k):
            callback(item)
    else:
        for class_name, class_ in find_database_access_class("comicat", "mods").items():
            co = class_()
            constant.mod_dist[class_name] = co
            constant.temp[k] = co.search_callback(k, lambda comic: set_class_name(comic, class_name, k, callback))


def chapter_thread(comic_info: ComicInfo, callback):
    """
    解析章节的线程
    如果缓存中有,直接返回,否则根据modname获取mod对象,调用mod解析获取章节信息
    :param comic_info:  漫画信息
    :param callback: 回调,返回单个章节的信息 Chapter
    :return:
    """
    if comic_info.url in constant.temp:
        for item in constant.temp.get(comic_info.url):
            callback(item)
    else:
        service = constant.mod_dist[comic_info.service]
        constant.temp[comic_info.url] = service.chapter_callback(comic_info, callback)


class Service(object):
    """
    业务主线程
    """
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.down_pool = BoundedThreadPoolExecutor(max_workers=5)
        self.parse_pool = BoundedThreadPoolExecutor(max_workers=20)

    def search(self, k, callback):
        """
        搜索,提交到解析线程池中
        :param k: 搜索关键字
        :param callback:  回调函数,返回单个 @ComicInfo
        """
        self.parse_pool.submit(search_thread, k, callback)

    def chapter(self, comic_info: ComicInfo, callback):
        """
        解析章节函数
        :param comic_info:  漫画信息
        :param callback: 回调,返回单个章节的信息 Chapter
        :return:
        """
        self.parse_pool.submit(chapter_thread, comic_info, callback)

    def parse_image_thread(self, comic_info: ComicInfo, chapter_info: ChapterInfo, callback):
        """
        解析章节图片列表,创建下载任务,返回下载任务
        :param comic_info: 漫画实体
        :param chapter_info: 章节实体
        :param callback: 返回下载任务,DownloadTask 实体
        :return:
        """
        if constant.APPLICATION_EXIT:  # 正在退出
            return
        service = constant.mod_dist[comic_info.service]
        service: WebsiteInterface
        # 判断此任务是否已经在下载中
        if chapter_info.url not in constant.downloaded_task_map:
            task = DownloadTask()
            task.comicInfo = comic_info
            task.chapterInfo = chapter_info
            task.imageInfos = service.parse_image_list(chapter_info)
            callback(task)
            constant.download_task_map[chapter_info.url] = task
            constant.downloaded_task_map[chapter_info.url] = task
            # 添加到下载线程池中
            self.down_pool.submit(task.download_image_thread)

    def parse_image(self, comic_info: ComicInfo, chapter_info: ChapterInfo, callback):
        """
        解析章节图片列表,创建下载任务,返回下载任务
        :param comic_info: 漫画实体
        :param chapter_info: 章节实体
        :param callback: 返回下载任务,DownloadTask 实体
        :return:
        """
        self.parse_pool.submit(self.parse_image_thread, comic_info, chapter_info, callback)

    def add_task(self, task: DownloadTask):
        """
        添加下载任务到线程池
        :param task:任务实体
        :return:
        """
        self.down_pool.submit(task.download_image_thread)

    def start_all_task(self):
        """
        开始所有下载任务
        :return:
        """
        for url, task in constant.download_task_map:
            if task.status == -3:
                task.status = -2
            self.down_pool.submit(task.download_image_thread)

    def stop_all_task(self):
        for url, task in constant.download_task_map:
            task.status = -3 if task.status == -2 else -2

    def stop_all(self):
        """
        停止所有线程
        :return:
        """
        constant.APPLICATION_EXIT = True
        self.down_pool.shutdown()
        self.parse_pool.shutdown()
