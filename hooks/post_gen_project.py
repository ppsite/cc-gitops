# coding=utf-8
import os
import shutil


class GenericCCHooks(object):
    """
    通用 CookieCutter Hooks
    file_path_list: 定义待删除的文件路径
    dir_path_list: 定义待删除的文件夹路径
    """

    file_path_list = []
    dir_path_list = []

    def __init__(self, removable):
        self.removable = removable

    def remove(self):
        if self.removable.lower() == 'n':
            for dir_path in self.dir_path_list:
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)

            for file_name in self.file_path_list:
                if os.path.exists(file_name):
                    os.remove(file_name)


class CeleryCCH(GenericCCHooks):
    file_path_list = [
        "base/beat.yaml",
        "base/worker.yaml",
        "overlays/master/beat.yaml",
        "overlays/master/worker.yaml",
    ]


class WebExpressCCH(GenericCCHooks):
    file_path_list = [
        "base/express.yaml",
        "overlays/master/express.yaml"
    ]


if __name__ == "__main__":
    cch_classes = [
        CeleryCCH('{{cookiecutter.use_celery}}'),
        WebExpressCCH('{{cookiecutter.web_express}}'),
    ]

    for cch in cch_classes:
        cch.remove()
