#!/usr/bin/env python

import random

class Binary(object):
    def __init__(self, num, lists):
        self.num = num
        self.lists = lists

    def binaryDigits(self):
        q = self.num
        while True:
            r = q % 2
            q = q // 2
            lists.append(r)
            if q == 0:
                break
        lists.reverse()
        return lists

lists = []
num = random.randrange(4, 20)
binary = Binary(num, lists)
print(f'{num}! = {binary.binaryDigits()}')
