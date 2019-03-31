# coding:utf-8
from __future__ import print_function, unicode_literals

import urllib3
urllib3.disable_warnings()
import sys
sys.path.append("../")
from hook import tthr


@tthr("requests", modules=True, call=True, auto_import=True)
class Requests(object):
    def __init__(self, request):
        self._request = request

    def __change_default(self, args, kwargs):
        kwargs.setdefault("verify", False)
        kwargs.setdefault("proxies", {"http": "socks5://:@127.0.0.1:1080", "https": "socks5://:@127.0.0.1:1080"})
        return args, kwargs

    def get(self, *args, **kwargs):
        args, kwargs = self.__change_default(args, kwargs)
        return self._request.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        args, kwargs = self.__change_default(args, kwargs)
        return self._request.post(*args, **kwargs)

    def head(self, *args, **kwargs):
        args, kwargs = self.__change_default(args, kwargs)
        return self._request.head(*args, **kwargs)

    def put(self, *args, **kwargs):
        args, kwargs = self.__change_default(args, kwargs)
        return self._request.put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        args, kwargs = self.__change_default(args, kwargs)
        return self._request.delete(*args, **kwargs)

    def options(self, *args, **kwargs):
        args, kwargs = self.__change_default(args, kwargs)
        return self._request.options(*args, **kwargs)

    def patch(self, *args, **kwargs):
        args, kwargs = self.__change_default(args, kwargs)
        return self._request.patch(*args, **kwargs)

    def __getattr__(self, item):
        return getattr(self._request, item)
import requests
r = requests.get("http://ifconfig.me")
print(r.content)