# coding:utf-8
import sys

sys.path.append("../")
from hook import tthr

import StringIO

__file_list__ = {}
__prefix__ = ""


@tthr("open", debug=True)
def open_file(open_, name, mode="r", buffering=-1):
    global __file_list__
    global __prefix__
    if __prefix__:
        if name.lower().startswith(__prefix__):
            if __file_list__.has_key(name[len(__prefix__):]):
                content = __file_list__[name[len(__prefix__):]]
                if isinstance(content, file):
                    return content
                elif isinstance(content, str) or isinstance(content, unicode):
                    return StringIO.StringIO(content)
                else:
                    return content
    return open_(name, mode, buffering)


# 删掉作案过程
del open_file


def add_filecut(path, content=""):
    global __file_list__
    __file_list__[path] = content


def set_filecut_prefix(prefix=""):
    global __prefix__
    if prefix:
        __prefix__ = "%s://" % prefix
    else:
        __prefix__ = ""


__all__ = ['add_filecut', 'set_filecut_prefix']
if __name__ == '__main__':
    set_filecut_prefix("ms")
    add_filecut("home.txt", "aaaaaaaaa")
    print(open("ms://home.txt", "r").read())
