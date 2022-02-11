from typing import Optional, List

import requests
from lxml import etree

from entity import ImageInfo, ChapterInfo, ComicInfo
from mods.website_interface import WebsiteInterface


class DogemangaComicat(WebsiteInterface):
    def __init__(self):
        self.session = requests.Session()
        self.webSiteName = "dogemanga"
        self.searchUrl = "https://dogemanga.com/?q={}"
        self.domain = "https://dogemanga.com"
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/97.0.4692.99 Safari/537.36'
        }

    def search_callback(self, key, callback) -> List[ComicInfo]:
        comic_info_list: List[ComicInfo] = []
        url = self.searchUrl.format(key)
        response = self.session.get(url)
        print(response)
        if response.status_code != 200:
            print(url, response.status_code)
        else:
            tree = etree.HTML(response.text)
            for div in tree.xpath('//div[@class="row"]/div'):
                info = ComicInfo()
                info.url = div.xpath('./div[2]//h4/a/@href')[0]
                info.coverUrl = div.xpath('./div[1]//img/@src')[0]
                info.domain = self.webSiteName
                info.cover = self.session.get(info.coverUrl, headers=self.headers).content
                info.title = div.xpath('./div[2]//h4/a/text()')[0].replace("\n", "")
                info.author = div.xpath('./div[2]//h5/a/text()')[0].replace("\n", "")
                info.describe = div.xpath('./div[2]//p/text()')[0].replace("\n", "")
                info.status = div.xpath('./div[2]//li')[0]
                callback(info)
                comic_info_list.append(info)

        return comic_info_list

    def chapter_callback(self, comic_info: ComicInfo, callback) -> List[ChapterInfo]:
        chapter_list = []
        response = self.session.get(comic_info.url)
        if response.status_code != 200:
            print(comic_info.url, response.status_code)
        else:
            tree = etree.HTML(response.text)
            for a in tree.xpath("//div[@class='site-page-thumbnail-icons-box']/a"):
                chapter_info = ChapterInfo()
                chapter_info.title = a.text.strip()
                chapter_info.url = a.attrib.get("href")
                chapter_list.append(chapter_info)
                if callback:
                    callback(chapter_info)
        return chapter_list

    def parse_image_list(self, chapter_info: ChapterInfo) -> List[ImageInfo]:
        image_list = []
        response = self.session.get(chapter_info.url)
        if response.status_code != 200:
            print(chapter_info.url, response.status_code)
        else:
            tree = etree.HTML(response.text)
            for img in tree.xpath("//div[@id='site-page-slides-box']/div/img/@data-src"):
                info = ImageInfo()
                info.url = img
                image_list.append(info)

        return image_list

    def down_image(self, image_info: ImageInfo) -> Optional[bytes]:
        response = self.session.get(image_info.url, headers=self.headers)
        if response.status_code == 200:
            return response.content
        else:
            return


if __name__ == '__main__':
    c = DogemangaComicat()

    # 搜索
    # def test(info):
    #     print(info.title, info.url)
    #
    #
    # c.search_callback('龙珠', test)

    # 测试获取章节
    # def test(info):
    #     print(info.title, info.url)
    #
    #
    # co = ComicInfo()
    # co.url = 'https://dogemanga.com/m/%E9%BE%99%E7%8F%A0%E8%B6%85/Zt7tQcPo'
    #
    # c.chapter_callback(co, test)

    # 测试章节获取图片列表
    # ch = ChapterInfo()
    # ch.url = 'https://dogemanga.com/p/%E9%BE%99%E7%8F%A0%E8%B6%85-%E7%AC%AC77%E8%AF%9D-%E6%82%9F%E7%A9%BA%E4%B9%8B%E7%88%B6%E5%B7%B4%E8%BE%BE%E5%85%8B/8NJ3vqQA'
    #
    # for i in c.parse_image_list(ch):
    #     print(i.url)
