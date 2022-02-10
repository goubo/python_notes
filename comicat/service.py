import os
import typing

import urllib3

import constant
from entity import ComicInfo, ChapterInfo, ImageInfo
from mods.website_interface import WebsiteInterface
from util import BoundedThreadPoolExecutor


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


class DownloadTask(object):
    comicInfo: ComicInfo
    chapterInfo: ChapterInfo
    imageInfos: typing.List[ImageInfo]
    success = {}
    error = {}
    status: int = 0  # 0:等待开始;1:开始;2:暂停;-1:完成;-2:完成,有错误;-3:有错误,暂停
    show: int = 1  # 下载列表是否展示

    def __init__(self):
        self.success = {}
        self.error = {}

    def download_image_thread(self):
        if constant.APPLICATION_EXIT:
            return
        if self.status == 0 or self.status == 1:
            self.status = 1
            file_path = os.path.join(constant.down_path, self.comicInfo.title, self.chapterInfo.title)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            for page in range(len(self.success) + len(self.error) + 1, len(self.imageInfos) + 1):
                if self.status != 1 or constant.APPLICATION_EXIT:
                    return
                web_service: WebsiteInterface = constant.mod_dist[self.comicInfo.service]
                image_path = file_path + os.sep + ("%0{}d".format(len(str(len(self.imageInfos)))) % page) + \
                             os.path.splitext(urllib3.util.parse_url(self.imageInfos[page - 1].url).path)[-1]

                self.success[image_path] = page
                img_bytes = web_service.down_image(self.imageInfos[page - 1])
                with open(image_path, "wb") as f:
                    f.write(img_bytes)
                constant.download_task_widget_map[self.chapterInfo.url].update_task(self)
            self.status = -2 if len(self.error) > 0 else -1
            constant.download_task_widget_map[self.chapterInfo.url].update_task(self)
        elif self.status == -2:  # 重试error列表
            file_path = os.path.join(constant.down_path, self.comicInfo.title, self.chapterInfo.title)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            for k, v in self.error:
                web_service: WebsiteInterface = constant.mod_dist[self.comicInfo.service]
                image_path = file_path + ("%0{}d".format(len(str(len(self.imageInfos)))) % v) + \
                             os.path.splitext(urllib3.util.parse_url(k).path)[-1]
                self.success[image_path] = k
                # time.sleep(0.1)
                img_bytes = web_service.down_image(self.imageInfos[k])
                with open(image_path, "wb") as f:
                    f.write(img_bytes)
                # 更新下载状态
                self.error.pop(k)
                constant.download_task_widget_map[self.chapterInfo.url].update_task(self)
            self.status = -2 if len(self.error) > 0 else -1
            constant.download_task_widget_map[self.chapterInfo.url].update_task(self)
        # 真正完成
        if self.status == -1:
            constant.download_task_map.pop(self.chapterInfo.url, None)
            constant.downloaded_comic_map[self.comicInfo.url] = self.comicInfo


def stop_all_task():
    for url, task in constant.download_task_map:
        task.status = -3 if task.status == -2 else 2


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

    def search_thread(self, k, callback):
        """
        搜索线程
        如果缓存中有,直接返回,否则调用所有的mod,进行搜索
        :param k: 关键字
        :param callback:回调
        :return:
        """

        def work_thread(class_name, _key, mod_server, _callback):
            constant.temp[k] = mod_server.search_callback(_key, lambda comic: set_class_name(comic, class_name, _key,
                                                                                             _callback))

        if k in constant.temp:
            for item in constant.temp.get(k):
                callback(item)
        else:
            for key, value in constant.mod_dist.items():
                try:
                    self.parse_pool.submit(work_thread, key, k, value, callback)
                except Exception as err:
                    print(err)

    def search(self, k, callback):
        """
        搜索,提交到解析线程池中
        :param k: 搜索关键字
        :param callback:  回调函数,返回单个 @ComicInfo
        """
        self.parse_pool.submit(self.search_thread, k, callback)

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
            elif task.status == 2:
                task.status = 0
            self.down_pool.submit(task.download_image_thread)

    def application_down(self):
        """
        停止所有线程
        :return:
        """
        constant.APPLICATION_EXIT = True
        self.down_pool.shutdown()
        self.parse_pool.shutdown()
        constant.DB['downloaded_task_map'] = constant.downloaded_task_map
        constant.DB['download_task_map'] = constant.download_task_map
        constant.DB['downloaded_comic_map'] = constant.downloaded_comic_map
