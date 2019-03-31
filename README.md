# hook

# 支持

本支持库目前只在 python2.7 通过测试

# 文档
本库的安装取决于个人习惯，放到python目录也可以，放到个人项目中也可以


    # 样例
    from hook import tthr
    @tthr("替换的第一个名字", # 本装饰器第一参数为*args，专门用于描述被替换的名字
          "替换的第二个名字", 
          modules=True, # 替换模块
          builtins=True, # 替换内置对象
          raw=True, # 直接替换对象进去，不会检查内容是否有效，不会包装成传入函数的第一个参数 
          debug=True, # 调试信息 
          auto_import=True) # 自动导入
    def tmp(old, filename):
        print(old)
        print(filename)
        return old(filename)



该模块的开发主要原因在examples/test_print.py中有展现


    from __future__ import print_function
    from colorterminal import Color
    
    print("hello", color=Color.RED)
    
    for _ in range(100):
        print("hello rand Color", color=Color.RAND)


注意 print_function 是必须的 因为他可以开启支持类似py3的print

只要导入一个看起来对整体没有多少改变的库就可以重写print的功能，这很棒。

该支持库最开始就是为了这个功能，写了很多多余的代码，后来想到把这部分单独提取出来很棒，经常可以用得到

本库中除了tthr装饰器，还有s_builtin字典对象，该对象中存有原本的 __builtin__ 的属性

### 希望这个python的库对python的逆向产生帮助，可以大概获取到python运行时的一些流程信息


# 样例

在 example/test_open.py 中有替换open函数对打开文件进行替换操作的样例

在 example/test_module.py 中有 模块 替换的样例

在 example/test_analyzer.py 中有一个简单的py运行流程分析，这个东西在写的时候耗费的精力是较多的，写的过程中也遇到了很多的问题，最后没办法只能写成这样了，（更多的问题是从某支持库导入某个类，这个类是被其他类继承的，这就造成了很多问题）

在 example/test_requests_default.py 中有一个简单的设置requests请求默认参数的样例，设置了默认的请求的代理以及禁用验证(本样例只是为了展示tthr的使用，并非探讨最好的方法)

注:更多的用法就是直接的替换内置函数，替换一些模块，获取到运行结果，因为有很多被替换的对象可能会当成参数传入其他函数，可能会当成父类型被继承，可能会检查运行类型，添加注释等等的问题，写一个分析的样例就很难，如果是单独的进行一些替换操作应该是可以的


# !!!工作原理

该模块依赖于python导入库后存在sys.modules中，经过尝试发现这个modules好像和globals一样，不能替换成其他对象

# !!! 注意

在样例目录中的例子都有一句sys.path.append("../") ,这句代码是将上层添加到当前环境变量中，如果您要使用这些样例，请删掉这个过程，并且将 hook.py 放到可以正常导入的位置