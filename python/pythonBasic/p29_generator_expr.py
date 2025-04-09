#!/usr/bin/env python

numbers = [1, 2, 3, 4, 5]
evnens = (2 * i for i in numbers)

print(evnens)
print(evnens.__next__())
print(evnens.__next__())
print(sum(evnens))

print()
print(numbers)
numbers.reverse()
print(numbers)
print()

evnens = (2 * i for i in numbers)

print(evnens)
print(evnens.__next__())
print(evnens.__next__())
print(numbers)
print(evnens.__next__())