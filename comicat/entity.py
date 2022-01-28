import typing


class ImageInfo(dict):
    url: str


class ChapterInfo(dict):
    url: str
    title: str


class ComicInfo(dict):
    """
    搜索结果:漫画详情
    """
    title: str  # 标题
    cover: bytes  # 封面
    coverUrl: str  # 封面
    describe: str  # 描述
    author: str  # 作者
    heat: int = 0  # 热度
    url: str  # 地址
    domain: str  # 网站编号
    status: str  # 状态
    tip: str  # 分类
    service: object
    chapterList: typing.List[ChapterInfo] = []
