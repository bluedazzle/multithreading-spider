# coding: utf-8
# Author: RaPoSpectre
# Create: 2016-03-29

from __future__ import unicode_literals

import Queue
import copy
import threading
import functools

import requests


class SpiBee(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
        "Content-Type": "text/html",
    }
    proxies = {
        "http": "127.0.0.1",
        "https": "127.0.0.1"
    }

    def __init__(self, q, proxy='127.0.0.1', name='SpiBee'):
        super(SpiBee, self).__init__()
        self.q = q
        self.proxies['http'] = proxy
        self.proxies['https'] = proxy
        self.name = name

    @property
    def proxy(self):
        return self.proxies.get('http')

    @proxy.setter
    def proxy(self, value):
        self.proxies['http'] = value
        self.proxies['https'] = value

    def run(self):
        while True:
            try:
                resource = self.q.get()
                self.work(resource)
                self.q.task_done()
            except Queue.Empty:
                break
            except Exception, e:
                return e

    def work(self, resource):
        pass

    def request(self, url, method='get', data=None, timeout=3):
        if method.upper() == 'GET':
            request = functools.partial(requests.get, headers=self.headers, timeout=timeout)
            if self.proxy == '127.0.0.1':
                return request(url)
            return request(url, proxies=self.proxies)

        request = functools.partial(requests.post, headers=self.headers, timeout=timeout, data=data)
        if self.proxy == '127.0.0.1':
            return request(url)
        return request(url, proxies=self.proxies)


class SpiComb(threading.Thread):
    def __init__(self, q, work_list, name='SpiComb'):
        super(SpiComb, self).__init__()
        self.q = q
        self.work_list = copy.deepcopy(work_list)
        self.name = name

    def run(self):
        while True:
            try:
                resource = self.work()
                self.q.put(resource)
            except Queue.Full:
                break
            except Exception, e:
                return e

    def work(self):
        if len(self.work_list):
            return self.work_list.pop()
        raise Queue.Full
