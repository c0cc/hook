# coding:utf-8
# 替换模块的用法 ！！！注意，应该在当前文件的模块导入前进行cut，cut的有效期应该是在cut之后导入的语句都生效
import sys

sys.path.append("../")
from hook import tthr


@tthr("os", modules=True, call=True, auto_import=True)
class OS:
    def __init__(self, m):
        self.__m__ = m
        self.listdir = lambda x: "hello :%s" % x

    def __getattr__(self, item):
        return getattr(self.__m__, item)

    def __str__(self):
        return "hello world"


import os

print(os)
print(os.listdir("/home"))
