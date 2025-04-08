#!/usr/bin/env python
from types import new_class


def calc(a):

    def add(b):
        return a + b
    return add

sum = calc(1)
print(sum(2))

def hello(msg):
    message = "Hello " + msg

    def say():
        print(message)
    return say

f = hello('Moon')
f()