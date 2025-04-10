#!/usr/bin/env python

def gcd(a, b):
    if a < b:
        a, b = b, a
    print("gcd", (a, b))
    while b != 0:
        r = a % b
        a = b
        b = r
    return a

a = int(input("a = "))
b = int(input("b = "))

print(f'gcd(a{a}, b{b}) = {gcd(a, b)}')