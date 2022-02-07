import os
import typing
import urllib

import constant
from entity import ComicInfo, ChapterInfo, ImageInfo
from mods.website_interface import WebsiteInterface


class DownloadTask(object):
    comicInfo: ComicInfo
    chapterInfo: ChapterInfo
    imageInfos: typing.List[ImageInfo]
    success = {}
    error = {}
    widget: object
    status: int = 0  # 0 等待开始 1 开始 2 暂停  -1 完成

    def __init__(self):
        self.success = {}
        self.error = {}

    def download_image_thread(self):
        if constant.APPLICATION_EXIT:
            return

        if self.status == 0 or self.status == 1:
            self.status = 1
            file_path = os.path.join('/Users/bo/my/tmp/comicat_down', self.comicInfo.title, self.chapterInfo.title)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            for page in range(len(self.success) + len(self.error) + 1, len(self.imageInfos) + 1):
                if self.status != 1 or constant.APPLICATION_EXIT:
                    return
                web_service: WebsiteInterface = constant.mod_dist[self.comicInfo.service]
                image_path = file_path + os.sep + ("%0{}d".format(len(str(len(self.imageInfos)))) % page) + \
                             os.path.splitext(urllib.parse.urlparse(self.imageInfos[page - 1].url).path)[-1]

                self.success[image_path] = page
                img_bytes = web_service.down_image(self.imageInfos[page])
                with open(image_path, "wb") as f:
                    f.write(img_bytes)
                self.widget.update_task(self)
            self.status = -1
            print("下载完成")
            self.widget.update_task(self)
        elif self.status == -1:  # 重试error列表
            file_path = os.path.join('/Users/bo/my/tmp/comicat_down', self.comicInfo.title, self.chapterInfo.title)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            for k, v in self.error:
                web_service: WebsiteInterface = constant.mod_dist[self.comicInfo.service]
                image_path = file_path + ("%0{}d".format(len(str(len(self.imageInfos)))) % v) + \
                             os.path.splitext(urllib.parse.urlparse(k).path)[-1]
                self.success[image_path] = k
                # time.sleep(random.randint(0, 5))
                img_bytes = web_service.down_image(self.imageInfos[k])
                with open(image_path, "wb") as f:
                    f.write(img_bytes)
                # 更新下载状态
                self.error.pop(k)
                self.widget.update_task(self)


if __name__ == '__main__':
    print(os.path.splitext('https://www.google.com.hk/search.txt?q=pyhton+Optional&oq=pyhton+Optional&aqs=chrome'
                         '..69i57j0i13l9.3421j0j4&sourceid=chrome&ie=UTF-8'))