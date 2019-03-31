# coding:utf-8
from __future__ import unicode_literals
from __future__ import print_function
from functools import partial
from inspect import isfunction, isclass
import __builtin__
import sys

# 对原本的内置对象做备份,其他包一样可以导入该包获取到原本的builtins对象
if sys.modules.has_key("__s_builtin__"):
    s_builtin = sys.modules['__s_builtin__']
else:
    s_builtin = {name: getattr(__builtin__, name, None) for name in dir(__builtin__)}
    sys.modules["__s_builtin__"] = s_builtin


def restore():
    '''
    还原内置对象的表
    :return: 返回是否成功
    '''
    # 如果存在备份表
    if sys.modules.has_key("__s_builtin__"):
        # 还原备份表
        for k, v in s_builtin.items():
            setattr(__builtin__, k, v)
        # 丢弃备份表
        sys.modules.pop("__s_builtin__")
        return True
    return False


def tthr(*names, **kwargs):
    '''
    非常叼逼的名字，叫偷天换日
    如果raw_func不进行设置，将在新的函数的第一参数位置放置原本替换的函数内容
    :param names: 要替换的函数的名称，可以是多个
    :param kwargs: 设置参数,同下方获取的参数
    :return: 返回当前函数的
    '''

    _builtin_replace = kwargs.get("builtins", False)  # 内置变量的替换
    _modules_replace = kwargs.get("modules", False)  # 全局的模块的替换
    _auto_import = kwargs.get("auto_import", False)  # 模块替换的时候不存在的模块是否自动导入
    _callable_ = kwargs.get("call", False)  # 调用还是封装
    raw_func = kwargs.get("raw", False)  # 是否需要函数包装返回回去
    __dbg__ = kwargs.get("debug", False)  # 调试模式

    def debug(*info, **kwargs):
        if __dbg__:
            s_builtin['print'](*info, **kwargs)

    debug("[***] 启动TTHR")
    debug("[***] 替换内置对象:%s" % ["关闭", "开启"][_builtin_replace])
    debug("[***] 替换模块对象:%s" % ["关闭", "开启"][_modules_replace])
    debug("[***] 调用类型:%s" % ["封装(不会调用被注解函数)", "调用(会调用被注解函数)"][_callable_])
    debug("[***] 参数类型:%s" % ["包装(会获取原本内容,并且传入处理函数)", "裸参(不会获取原本内容,直接替换)"][raw_func])
    if raw_func:
        debug("[***] 裸参函数启用,调用类型选项失效")
    if _modules_replace == False and _builtin_replace == False:
        debug("[***] 模块替换未开启,强制开启内置对象替换")
        _builtin_replace = True

    def cut(func):
        '''
        函数替换过程中发生了一点小变化，旧的函数会传入新的函数的第一个参数，请注意接收
        :param func: 用于处理该名称函数的功能
        :return: 返回可能是原本的函数，可能什么都没有
        '''
        # 不知道函数的名字可能是什么，没准还是个类
        if isfunction(func):
            src_name = func.func_name

        elif isclass(func):
            src_name = func.__name__
        else:
            src_name = s_builtin['str'](func)

        def contro_r(name, value=None):
            if _builtin_replace:
                if not sys.modules.has_key('__builtin__') and _auto_import:
                    s_builtin['__import__']('__builtin__')
                if value:
                    s_builtin['setattr'](sys.modules['__builtin__'], name, value)
                else:
                    return s_builtin['getattr'](sys.modules['__builtin__'], name, None)
            elif _modules_replace:
                if value != None:
                    sys.modules[name] = value
                else:
                    if not sys.modules.has_key(name) and _auto_import:
                        try:
                            s_builtin['__import__'](name)
                            debug("[+++] 自动导入模块:%s 成功" % name)
                        except Exception as e:
                            debug("[!!!] 自动导入模块:%s 失败,失败原因:%s" % (name, e.message))
                    return sys.modules.get(name, None)

        ret = None
        for name in names:
            debug("=" * 50, "开始替换过程", "=" * 50)
            debug("[***] 替换名称:%s 到: %s" % (src_name, name))
            obj = contro_r(name)
            debug("[+++] 获取替换前内容:%s" % s_builtin['str'](obj))
            if raw_func:
                debug("[***] 裸参直接覆盖原对象")
                contro_r(name, func)
                ret = func
            else:
                if _callable_:
                    debug("[***] 调用包装函数(类),包装函数(类)第一参数为原值,获取返回值,填充到替换位置")
                    ret = func(obj)
                    contro_r(name, ret)
                else:
                    debug("[***] 不调用包装函数,将原本函数作为替换函数第一个参数传入参数")
                    ret = partial(func, obj)
                    contro_r(name, ret)
            debug("=" * 50, "结束替换过程", "=" * 50)
            debug()
        debug("[***] 替换过程结束")
        return ret

    return cut

