import os
import pkgutil


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
        module_name = parent_module_name + "." + sub_file_name
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
