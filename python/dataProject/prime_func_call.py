#!/usr/bin/env python

import prime_func

while True:
    n = int(input("input number(0: Quit: "))

    if (n == 0):
        break
    if ( n < 2):
        print("re-enter number")
        continue
    print(f"{n} is prime number") if prime_func.is_prime(n) == 1 else print(f"{n} is NOT prime number")