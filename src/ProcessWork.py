# coding: utf-8
# Author: RaPoSpectre
# Create: 2016-03-29

from __future__ import unicode_literals

import threading


class ProcessWorker(threading.Thread):
    def __init__(self, q, name='ProcessWorker'):
        super(ProcessWorker, self).__init__()
        self.q = q
        self.total = q.qsize()
        self.name = name
        self.last = -1

    def run(self):
        while True:
            finish_part = float(self.total - self.q.qsize())
            current_percent = round(finish_part / self.total * 100, 1)
            if self.last == current_percent:
                continue
            self.last = current_percent
            sign = ''
            if current_percent > 0:
                sign = '=' * int(now_num / 10 * 2)
            self.display(current_percent, sign, finish_part)
            if self.q.empty():
                break

    def display(self, cp, sign, fp):
        sys.stdout.write('\r任务进度: [{0}%{1}->]({2}/{3})'.format(cp, sign, int(fp), self.total))
        sys.stdout.flush()



