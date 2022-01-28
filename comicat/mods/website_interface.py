from abc import ABCMeta, abstractmethod
from typing import List

from entity import ComicInfo, ChapterInfo, ImageInfo


class WebsiteInterface(object):
    """
        单个网站的爬虫实现本接口
        class名称必须包括 Comicat 例如 Dm5Comicat , ComicatBilibili
        # webSiteName : 网站名称
        # domain : 网站首页
        # searchUrl: 搜索地址

    """
    __metaclass__ = ABCMeta  # 指定这是一个抽象类

    #
    # webSiteName: str
    # domain: str
    # searchUrl: str

    @abstractmethod  # 抽象方法
    def search_callback(self, key, callback) -> List[ComicInfo]:
        """
        搜索漫画列表,callback 函数逐个抛出爬到的 对象,callback 之前设置本身
        :param key: 搜索关键字
        :param callback: 回调函数,解析后的数据,封装ComicInfo类型,从callback抛出,用于动态渲染
        :return: 最后返回全部的数据,用于缓存
        """
        pass

    @abstractmethod  # 抽象方法
    def chapter_callback(self, comic_info: ComicInfo, callback) -> List[ChapterInfo]:
        """
        根据漫画查找章节,
        :param comic_info: 漫画
        :param callback: 逐行返回章节,用于动态渲染
        :return:最后返回章节数据,用于缓存
        """
        pass

    @abstractmethod  # 抽象方法
    def parse_image_list(self, chapter_info: ChapterInfo) -> List[ImageInfo]:
        """
        :param chapter_info:  章节信息
        :return:  图片地址列表,按顺序
        """
        pass

    @abstractmethod  # 抽象方法
    def down_image(self, image_info: ImageInfo) -> bytes:
        """
        下载图片
        :param image_info:  图片信息
        :return:  返回图片信息
        """
        pass
