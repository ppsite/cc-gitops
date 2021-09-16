# coding=utf-8
"""
                    _ _
                   (_) |
   ___ ___     __ _ _| |_ ___  _ __  ___
  / __/ __|   / _` | | __/ _ \| '_ \/ __|
 | (_| (__   | (_| | | || (_) | |_) \__ \\
  \___\___|   \__, |_|\__\___/| .__/|___/
        ______ __/ |          | |
       |______|___/           |_|

"""
import re
import sys


class ColorSchema(object):
    """
    基于 shell 的配色方案
    """
    TERMINATOR = "\033[0m"  # 统一终止符

    FONT_RED = "\033[31m"
    FONT_GREEN = "\033[32m"
    FONT_YELLOW = "\033[33m"
    FONT_BLUE = "\033[34m"
    FONT_VIOLET = "\033[35m"
    FONT_SKY_BLUE = "\033[36m"

    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_VIOLET = "\033[45m"
    BG_SKY_BLUE = "\033[46m"

    def end(self, message):
        print(self.BG_VIOLET + message + self.TERMINATOR)

    def info(self, message):
        message = "[Info] " + message
        print(self.FONT_SKY_BLUE + message + self.TERMINATOR)

    def warning(self, message):
        message = "[🔔️] " + message
        print(self.FONT_YELLOW + message + self.TERMINATOR)

    def error(self, message):
        message = "[🆘] " + message
        print(self.FONT_RED + message + self.TERMINATOR)

    def success(self, message):
        message = "[✅] " + message
        print(self.FONT_GREEN + message + self.TERMINATOR)

    def title(self, message):
        message = "[🚀] " + message
        print(self.BG_GREEN + message + self.TERMINATOR)


class MessageBlock(ColorSchema):
    """
    屏幕输出的信息块，封装统一样式
    """
    TITLE = None
    START = None
    END = None

    def __init__(self):
        if self.TITLE:
            self.title(message=self.TITLE)
        if self.START:
            self.info(message=self.START)
        self.action()
        if self.END:
            self.info(message=self.END)

    def action(self):
        pass

    @staticmethod
    def decode_output(output):
        """
        decode check_output from byte to utf-8
        @param output: subprocess check_output result
        """
        return output.decode('utf-8').strip().strip('\n')


class Welcome(MessageBlock):
    TITLE = "Hi Man, Glad to see you here, Welcome to Star!"
    START = ">>> https://github.com/pyfs/cc_gitops.git <<<"
    END = "----------------------------------------------------------"

    def action(self):
        print(__doc__)


class WellDone(MessageBlock):
    END = """
    Congratulations, Kustomize Structure Generated ⛽️⛽️⛽️
    What's Next?
    1. Check env.yaml
    2. Check secret.yaml
    """


class CheckProjectName(MessageBlock):
    TITLE = "检测项目名称是否合规"

    def action(self):
        reg = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
        project_name = '{{ cookiecutter.project_name }}'
        if not re.match(reg, project_name):
            self.error(' The project name(%s) invalid, use _ instead of -' % project_name)
            sys.exit(1)


class PreGenProjectHooks(object):
    PIPELINE = [
        'Welcome',
        'WellDone',
    ]

    def __call__(self):
        for cls_name in self.PIPELINE:
            try:
                eval(cls_name)()
            except KeyError:
                print("PreGenProjectHooks has got no Attribute: %s" % cls_name)


if __name__ == '__main__':
    PreGenProjectHooks()()
