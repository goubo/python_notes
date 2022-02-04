from concurrent.futures import ThreadPoolExecutor

import constant
from download_task import DownloadTask
from entity import ComicInfo, ChapterInfo
from mods.website_interface import WebsiteInterface
from util import find_database_access_class


class Service(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.down_pool = ThreadPoolExecutor(max_workers=5)
        self.parse_pool = ThreadPoolExecutor(max_workers=20)

    def search_thread(self, k, callback):
        if k in constant.temp:
            for item in constant.temp.get(k):
                callback(item)
        else:
            for class_name, class_ in find_database_access_class("comicat", "mods").items():
                co = class_()
                constant.mod_dist[class_name] = co
                constant.temp[k] = co.search_callback(k, lambda comic: self.set_class_name(comic, class_name, callback))

    def set_class_name(self, comic: ComicInfo, class_name, callback):
        comic.service = class_name
        callback(comic)

    def search(self, k, callback):
        self.parse_pool.submit(self.search_thread, k, callback)

    def chapter_thread(self, comic_info: ComicInfo, callback):
        if comic_info.url in constant.temp:
            for item in constant.temp.get(comic_info.url):
                callback(item)
        else:
            service = constant.mod_dist[comic_info.service]
            constant.temp[comic_info.url] = service.chapter_callback(comic_info, callback)

    def chapter(self, comic_info: ComicInfo, callback):
        self.parse_pool.submit(self.chapter_thread, comic_info, callback)

    def parse_image_thread(self, comic_info: ComicInfo, chapter_info: ChapterInfo, callback):
        if constant.APPLICATION_EXIT:
            return
        service = constant.mod_dist[comic_info.service]
        service: WebsiteInterface
        # 判断此任务是否已经在下载中
        if chapter_info.url not in constant.download_task_map:
            task = DownloadTask()
            task.comicInfo = comic_info
            task.chapterInfo = chapter_info
            task.imageInfos = service.parse_image_list(chapter_info)
            callback(task)
            # 添加到下载线程池中
            self.down_pool.submit(task.download_image_thread)
            constant.download_task_map[chapter_info.url] = task

    def add_task(self, task: DownloadTask):
        self.parse_pool.submit(task.download_image_thread)

    def parse_image(self, comic_info: ComicInfo, chapter_info: ChapterInfo, callback):
        self.parse_pool.submit(self.parse_image_thread, comic_info, chapter_info, callback)

    def stop_all(self):
        constant.APPLICATION_EXIT = True
        self.down_pool.shutdown()
        self.parse_pool.shutdown()
