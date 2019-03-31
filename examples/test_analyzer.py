# coding:utf-8
from __future__ import print_function
from inspect import isclass, ismethod, isbuiltin, isfunction, iscode
from lscore.utils.colorterminal import Color
import marshal
import sys

sys.path.append("../")
from hook import tthr, s_builtins


class Partial(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        kwargs.update(self.kwargs)
        args = self.args + args
        return self.func(*args, **kwargs)


def get_info(i=0):
    frame = sys._getframe(i + 2)
    line = frame.f_lineno
    filename = frame.f_code.co_filename
    return filename, line


def method_replace(func, name, *args, **kwargs):
    filename, line = get_info(1)
    if name == "_getframe" and not args:
        return func(1)
    if name == "CodeType":
        for p in args:
            if isinstance(p, tuple):
                for x in p:
                    if iscode(x):
                        print(repr(marshal.dumps(x)))
    print("[***] 文件:%s 第 %s 行 调用函数:%s 传入参数:*args=%s **kwargs=%s" % (filename, line, name, args, kwargs),
          color=Color.YELLOW)
    return func(*args, **kwargs)


def var_package(src, name):
    if isinstance(src, Partial):  # 解决已经被封装的对象二次封装的过程
        return src

    # 有些对象封装不得，问题卡在传入参数，检查过不去
    if isinstance(src, (str, bool, int, float, tuple, dict, list, bytearray)):
        return src
    if src == None:
        return src
    # 下层沟通障碍，socket设置超时时间md居然默认是个object
    if hasattr(src, "__class__"):
        if src.__class__ == object:
            return src

    if isclass(src):
        print("[+++] 类对象未包装:%s" % name, color=Color.GREEN)
        r = src
    elif isfunction(src):
        print("[+++] 函数包装:%s" % name, color=Color.GREEN)
        r = Partial(method_replace, src, name)
    elif ismethod(src):
        print("[+++] 方法包装:%s" % name, color=Color.GREEN)
        r = Partial(method_replace, src, name)
    elif isbuiltin(src):
        print("[+++] 内置对象包装:%s" % name, color=Color.GREEN)
        r = Partial(method_replace, src, name)
    elif isinstance(src, type):
        r = src
    else:
        print("[+++] 其他对象封装:%s" % name, color=Color.GREEN)
        r = create_class_package(src, name)
    return r


def create_class_package(module, name):
    class replace_obj(object):
        def __init__(self, name, module):
            self.__names__ = name
            self.__modules__ = module
            self.__class__.__self_obj__ = self

        def GOBJ(self):
            return self.__modules__

        def __getattr__(self, item):
            filename, line = get_info()
            print("[***] 文件:%s 第 %s 行 获取 %s 属性:%s" % (filename, line, self.__names__, item), color=Color.YELLOW)

            p = getattr(self.__modules__, item)

            # 无法处理的对象
            if self.__names__ == "os" and item == "environ":
                return p
            return var_package(p, item)

        @property
        def __all__(self):
            return dir(self.__modules__)

        def __getitem__(self, item):
            return self.__modules__.__getitem__(item)

    return replace_obj(name, module)


class Global(dict):

    def __init__(self, name=""):
        super(dict, self).__init__()
        dict.__setattr__(self, '__tmp', {})
        self.__names__ = name or "Dict"

    def __getattr__(self, item):
        filename, line = get_info()
        print("[%s] 文件:%s 第 %s 行 调用方法:%s" % (self.__names__, filename, line, item), color=Color.RED)
        return getattr(self, item)

    def __getitem__(self, item):
        filename, line = get_info()
        __tmp = self.__getattribute__('__tmp')
        print("[%s] 文件:%s 第 %s 行 获取变量:%s" % (self.__names__, filename, line, item), color=Color.RED)
        if item == "print":
            return Partial(method_replace, s_builtins["print"], "print")
        return __tmp.get(item)

    def __setitem__(self, key, value):
        filename, line = get_info()
        print("[%s] 文件:%s 第 %s 行 设置变量:%s 值:%s" % (self.__names__, filename, line, key, repr(value)), color=Color.RED)
        __tmp = self.__getattribute__('__tmp')
        __tmp[key] = value

    def __delitem__(self, key):
        filename, line = get_info()
        print("[%s] 文件:%s 第 %s 行 删除变量:%s" % (self.__names__, filename, line, key), color=Color.RED)
        __tmp = self.__getattribute__('__tmp')
        del __tmp[key]


@tthr('input', call=False, _builtin_replace=True)
def input(func, prompt=""):
    filename, line = get_info()
    t = func(prompt)
    print("[***] 文件:%s 第 %s 行 获取输入提示: %s 输入内容:%s" % (filename, line, prompt, t))
    return


@tthr('input', 'raw_input', call=False, _builtin_replace=True)
def input(func, prompt=""):
    filename, line = get_info()
    t = func(prompt)
    print("[***] 文件:%s 第 %s 行 获取输入提示: %s 输入内容:%s" % (filename, line, prompt, t))
    return t


@tthr('len', call=False, _builtin_replace=True)
def len(func, o):
    filename, line = get_info()
    t = func(o)
    print("[***] 文件:%s 第 %s 行 获取 %s 的长度为 %s" % (filename, line, repr(o), t))
    return t


@tthr('ord', call=False, _builtin_replace=True)
def ord(func, c):
    filename, line = get_info()
    t = func(c)
    print("[***] 文件:%s 第 %s 行 转换字符 %s 到ascii:%s" % (filename, line, repr(c), t))
    return t


@tthr('reload', call=False, _builtin_replace=True)
def reload(func, module):
    filename, line = get_info()
    t = func(module)
    print("[***] 文件:%s 第 %s 行 重新载入模块:%s" % (filename, line, module))
    return t


@tthr('repr', call=False, _builtin_replace=True)
def repr(func, o):
    filename, line = get_info()
    t = func(o)
    print("[***] 文件:%s 第 %s 行 repr:%s" % (filename, line, t))
    return t


@tthr('dir', call=False, _builtin_replace=True)
def dir(func, o):
    filename, line = get_info()
    t = func(o)
    print("[***] 文件:%s 第 %s 行 查看对象 %s 的属性为:%s" % (filename, line, o, t))
    return t


@tthr('cmp', call=False, _builtin_replace=True)
def cmp(func, x, y):
    filename, line = get_info()
    t = func(x, y)
    print("[***] 文件:%s 第 %s 行 比较 %s 和 %s 返回 %s" % (filename, line, x, y, t))
    return t


@tthr('sum', call=False, _builtin_replace=True)
def sum(func, iterable):
    filename, line = get_info()
    t = func(iterable)
    print("[***] 文件:%s 第 %s 行 计算列表 %s 的总数 %s" % (filename, line, iterable, t))
    return t


@tthr('open', call=False, _builtin_replace=True)
def open(func, name, mode="r", buffering=-1):
    filename, line = get_info()
    t = func(name, mode, buffering)
    print("[***] 文件:%s 第 %s 行 打开文件:%s" % (filename, line, name), color=Color.BLUE)
    return t


@tthr('compile', call=False, _builtin_replace=True)
def compile(func, source, filename, mode, flags=None, dont_inherit=None):
    filename1, line = get_info()
    t = func(source, filename, mode, flags, dont_inherit)
    print("[***] 文件:%s 第 %s 行 编译文件:%s 源码:%s" % (filename1, line, filename, source), color=Color.BLUE)
    return t


@tthr('eval', call=False, _builtin_replace=True)
def eval(func, source, globals=None, locals=None):
    filename1, line = get_info()
    t = func(source, globals, locals)
    print("[***] 文件:%s 第 %s 行 运行表达式:%s 结果为:%s" % (filename1, line, repr(source), repr(t)), color=Color.BLUE)
    return t


# 该语句有一部分是为了初始化一次上面print函数，防止产生bug
print("=" * 50)
print("=" * 5 + " " * 40 + "=" * 5)

print("=" * 5 + " " * 12, end="")
print("妈的智障 行为分析器 ", end="", color=Color.BLUE)
print(" " * 11 + "=" * 5)

print("=" * 5 + " " * 40 + "=" * 5)

print("=" * 5 + " " * 13, end="")
print("内置函数加载完成", end="", color=Color.RED)
print(" " * 13 + "=" * 5)

print("=" * 5 + " " * 40 + "=" * 5)
print("=" * 50)


@tthr("__import__", debug=False)
def imports(import_func, name, globals={}, locals={}, fromlist=[], level=-1):
    r = import_func(name, globals, locals, fromlist, level)
    filename, line = get_info()
    print("[***] 文件:%s 第 %s 行 导入:%s" % (filename, line, name), color=Color.YELLOW)

    if name in ["_ssl", "sys"]:  # 分析出错的表
        return r
    if isclass(r):
        return r
    if name in ["__feture__"]:
        print("[***] 文件:%s 第 %s 行 启用魔法方式" % (filename, line), color=Color.YELLOW)
        return r
    return create_class_package(r, name)


def analyzer(co):
    globals_ = Global("Globals")
    locals_ = Global("Locals")
    print("=" * 50, color=Color.RED)
    print("[+++] 开始进行文件行为分析", color=Color.RED)
    print("=" * 50, color=Color.RED)
    # print("文件名称:%s" % co.co_filename)
    exec (co, globals_, locals_)
    print("=" * 50, color=Color.RED)
    print("[!!!] 文件分析结束", color=Color.RED)
    print("=" * 50, color=Color.RED)


analyzer("""
import chardet
print(chardet.detect("admin")) 
""")


# =========================================================================================================
# 未进行替换的函数
#
# @tthr('super', 'all', 'vars', 'unicode', 'memoryview', 'oct',
#       'bin', 'format', 'sorted', 'list', 'iter', 'round', 'set', 'bytes', 'reduce',
#       'intern', 'issubclass', 'Ellipsis', 'slice', 'getattr', 'abs', 'exit', 'print', 'hash',
#       'credits', 'frozenset', 'super', 'filter', 'range', 'staticmethod', 'pow', 'float',
#       'divmod', 'enumerate', 'apply', 'quit', 'basestring', 'zip', 'hex', 'long', 'next', 'chr',
#       'xrange', 'type', 'tuple', 'reversed', 'hasattr', 'delattr', 'setattr', 'compile', 'str', 'property',
#       'int', 'coerce', 'file', 'unichr', 'id', 'min', 'execfile', 'any', 'complex', 'bool', 'map', 'buffer', 'max',
#       'callable', 'eval', 'classmethod', call=False, _builtin_replace=True)
# =========================================================================================================
