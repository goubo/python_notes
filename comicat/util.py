import logging
import os
import pkgutil
import queue
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from io import BytesIO

from PIL import Image


def _deco(f):
    @wraps(f)
    def __deco(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.exception(e)

    return __deco


class BoundedThreadPoolExecutor(ThreadPoolExecutor, ):
    def __init__(self, max_workers=None, thread_name_prefix=''):
        ThreadPoolExecutor.__init__(self, max_workers, thread_name_prefix)
        self._work_queue = queue.Queue(max_workers * 2)

    def submit(self, fn, *args, **kwargs):
        fn_deco = _deco(fn)
        super().submit(fn_deco, *args, **kwargs)


def image_resize(image_bytes, width=None, height=None):
    """指定宽或高，得到按比例缩放后的宽高
    :param image_bytes: 图片
    :param width:目标宽度
    :param height:目标高度
    :return:按比例缩放后的 宽和高
    """

    image = Image.open(BytesIO(image_bytes))
    if not width and not height:
        return image.size
    if not width or not height:
        _width, _height = image.size
        height = width * _height // _width if width else height
        width = height * _width // _height if height else width
        return width, height


def find_database_access_class(parent_module_name: str, module_dir: str, sub_class: str = "Comicat") -> dict:
    """
    查找moduel_dir下的所有py文件的所有类，过滤非
    参数：
        parent_module_name:父模块路径
        module_dir:需要导入的模块名称（就是需要查找子类文件的文件夹）
        sub_class:校验类的名字中是否包含TypeA字样
    返回：
        {
            "类name: 类对象
        }
    """
    base_dir = os.path.dirname(__file__)
    # 如果是main执行上面的os.path.dirname，返回的是空，则需要调用abspath获取绝对路径
    if not base_dir:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    modules = pkgutil.iter_modules([base_dir + "/" + module_dir])
    found_modules = []
    for x, sub_file_name, _ in modules:
        module_name = parent_module_name + "." + module_dir + "." + sub_file_name
        found_module = x.find_module(module_name).load_module(module_name)
        found_modules.append(found_module)
    found_type_a_modules = {}
    for module in found_modules:
        attrs = list(dir(module))
        # 校验其类名是否包含 sub_class
        type_a_class = [x for x in attrs if sub_class in x]
        for class_name in type_a_class:
            class_ins = getattr(module, class_name)
            # 校验类中是否包含类name变量
            # if hasattr(class_ins, "name"):
            found_type_a_modules[class_name] = class_ins
    return found_type_a_modules
