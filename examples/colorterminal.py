#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import platform
import random
import sys

sys.path.append("../")
from hook import tthr

__is_win__ = 'Windows' in platform.platform()

# 颜色的预先定义

if __is_win__:
    class Color:
        BLACK = 0x00
        BLUE = 0x09
        GREEN = 0x0a
        RED = 0x0c
        YELLOW = 0x0e
        WHITE = 0x0f

        @property
        def RAND(cls):
            return random.choice([cls.BLACK, cls.BLUE, cls.GREEN, cls.RED, cls.YELLOW, cls.WHITE])
else:
    class Color:
        BLACK = '\033[0m'
        BLUE = '\033[34m'
        GREEN = '\033[32m'
        RED = '\033[31m'
        YELLOW = '\033[33m'
        WHITE = '\033[37m'

        @property
        def RAND(cls):
            return random.choice([cls.BLACK, cls.BLUE, cls.GREEN, cls.RED, cls.YELLOW, cls.WHITE])
Color = Color()


@tthr("print", available=True, debug=False)
def print_(print_func, *value, **kwargs):
    sep = kwargs.get("sep", " ")  # 获取分割字符
    end = kwargs.get("end", "\n")  # 获取结束字符
    file = kwargs.get("file", sys.stdout)  # 获取输出位置，默认打印控制台
    color = kwargs.get("color", Color.BLACK)  # 获取颜色，该属性为自定，覆盖外层print功能
    if __is_win__:
        STD_INPUT_HANDLE = -10
        STD_OUTPUT_HANDLE = -11
        STD_ERROR_HANDLE = -12

        def set_cmd_text_color(color):
            import ctypes
            std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            return ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle, color)

        set_cmd_text_color(color | color | color)
        print_func(*value, sep=sep, end=end, file=file)
        set_cmd_text_color(Color.RED | Color.GREEN | Color.BLUE)
    else:
        print_func(color, sep="", end="", file=file)  # 输出目标颜色
        print_func(*value, sep=sep, end="", file=file)  # 输出目标文字
        print_func(Color.BLACK, sep="", end=end, file=file)  # 输出还原颜色


# 删掉作案过程
del print_
if __name__ == '__main__':
    # test
    '''from __future__ import print_function
    from __future__ import unicode_literals
    from utils.colorterminal import Color
    '''
    print("test print color", end="", color=Color.GREEN)
