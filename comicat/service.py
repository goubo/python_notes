import threading

from entity import ComicInfo, ChapterInfo
from mods.website_interface import WebsiteInterface
from util import find_database_access_class


class Service(object):
    d = dict()

    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def search_thread(self, k, callback):
        if k in self.d:
            for item in self.d.get(k):
                callback(item)
        else:
            found_class_dict = find_database_access_class("comicat", "mods")
            for class_name, class_ in found_class_dict.items():
                # self.d[k] = class_().search_callback(k, callback) # 缓存
                class_().search_callback(k, callback)

    def search(self, k, callback):
        threading.Thread(target=self.search_thread, args=(k, callback)).start()

    def chapter_thread(self, comic_info: ComicInfo, callback):
        if comic_info.url in self.d:
            for item in self.d.get(comic_info.url):
                callback(item)
        else:
            service = comic_info.service
            service: WebsiteInterface
            service.chapter_callback(comic_info, callback)

    def chapter(self, comic_info: ComicInfo, callback):
        threading.Thread(target=self.chapter_thread, args=(comic_info, callback)).start()

    def parse_download(self, comic_info: ComicInfo, chapter_info: ChapterInfo):
        print("解析下载页面")


if __name__ == '__main__':
    found_class_dict = find_database_access_class("comicat", "mods")
    for class_name, class_ in found_class_dict.items():
        class_: WebsiteInterface
        l = class_().search("龙珠")
        for c in l:
            c: ComicInfo
            print(c.title)
            print(c.url)
            print(c.author)
            print(c.describe)
