import re
from typing import List, Optional

import execjs
import requests
from lxml import etree
from parsel import SelectorList, Selector

from entity import ImageInfo, ChapterInfo, ComicInfo
from mods.website_interface import WebsiteInterface


class MangabzComicat(WebsiteInterface):

    def __init__(self):
        self.session = requests.Session()
        self.webSiteName = "mangabz"
        self.searchUrl = "https://mangabz.com/search?title={}"
        self.domain = "https://mangabz.com"
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/97.0.4692.99 Safari/537.36'
        }

    def search_callback(self, key, callback) -> List[ComicInfo]:
        comic_info_list: List[ComicInfo] = []
        url = self.searchUrl.format(key)
        response = self.session.get(url)
        if response.status_code != 200:
            print(url, response.status_code)
        else:
            tree = etree.HTML(response.text)
            for index in tree.xpath("//ul[@class='mh-list']//div[@class='mh-item']/a/@href"):
                response = self.session.get(self.domain + index, headers=self.headers)
                if response.status_code != 200:
                    print(self.domain + index, response.status_code)
                else:
                    tree = etree.HTML(response.text)
                    info = ComicInfo()
                    info['chapterList'] = self.parse_chapter(tree, None)
                    info.url = response.url
                    info.coverUrl = tree.xpath('/html/body/div[3]/div/div/img/@src')[0]
                    info.cover = self.session.get(info.coverUrl, headers=self.headers).content
                    info.domain = self.webSiteName
                    info.title = tree.xpath('/html/body/div[3]/div/div/p[1]/text()')[0].strip()
                    info.author = tree.xpath('/html/body/div[3]/div/div/p[3]/span[1]/a/text()')[0].strip()
                    info.describe = tree.xpath('/html/body/div[4]/div/div/p/text()')[0].strip()
                    info.status = tree.xpath('/html/body/div[3]/div/div/p[3]/span[2]/span/text()')[0].strip()
                    info.tip = ','.join(tree.xpath('/html/body/div[3]/div/div/p[3]/span[3]/span/text()'))
                    info.heat = tree.xpath('/html/body/div[3]/div/div/p[2]/span/text()')[0].strip()
                    callback(info)
                    comic_info_list.append(info)
        return comic_info_list

    def parse_chapter(self, tree, callback):
        chapter_list = []
        alist: SelectorList = tree.xpath("//div[@class='detail-list-form-con']/a")
        for a in alist:
            a: Selector
            chapter_info = ChapterInfo()
            chapter_info.title = a.text.strip()
            chapter_info.url = self.domain + a.attrib.get("href")
            chapter_list.append(chapter_info)
            if callback:
                callback(chapter_info)
        return chapter_list

    def chapter_callback(self, comic_info: ComicInfo, callback) -> List[ChapterInfo]:

        if comic_info['chapterList']:
            for item in comic_info['chapterList']:
                callback(item)
        else:
            response = self.session.get(comic_info.url, headers=self.headers)
            if response.status_code != 200:
                print(comic_info.url, response.status_code)
            else:
                tree = etree.HTML(response.text)
                comic_info['chapterList'] = self.parse_chapter(tree, callback)

        return comic_info['chapterList']

    def parse_image_list(self, chapter_info: ChapterInfo) -> List[ImageInfo]:
        image_list = []
        response = self.session.get(chapter_info.url, headers=self.headers)
        cid = re.findall('var MANGABZ_CID=(.+?);', response.text)[0].strip()
        mid = re.findall('var MANGABZ_MID=(.+?);', response.text)[0].strip()
        page_count = re.findall('var MANGABZ_IMAGE_COUNT=(.+?);', response.text)[0].strip()
        dt = re.findall('var MANGABZ_VIEWSIGN_DT="(.+?)";', response.text)[0].strip()
        dt = dt.replace(" ", "+").replace(":", "%3A")
        sign = re.findall('var MANGABZ_VIEWSIGN="(.*?)";', response.text)[0].strip()
        _headers = self.headers.copy()
        _headers['Referer'] = chapter_info.url
        for page in range(1, int(page_count) + 1):
            chapter_fun_url = f'{chapter_info.url}chapterimage.ashx?cid={cid}&page={page}&key=&_cid={cid}&_mid={mid}&_dt={dt}&_sign={sign} '
            response = self.session.get(chapter_fun_url, headers=_headers)
            js = execjs.eval(response.text)
            info = ImageInfo()
            info.url = js[0]
            # info['dm5Curl'] = dm5_curl
            image_list.append(info)

        return image_list

    def down_image(self, image_info: ImageInfo) -> Optional[bytes]:
        response = self.session.get(image_info.url, headers=self.headers)
        if response.status_code == 200:
            return response.content
        else:
            return
