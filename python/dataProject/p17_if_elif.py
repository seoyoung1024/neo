#!/usr/bin/env python

while True:
    i = input("input the second number(q:quit) : ")

    if i == 'q' or i == 'Q' or i == 'q':
        break
    elif i.isdigit():
        print('Please enter a vaild input')
        continue
    else:
        if int(i) > 0:
            print("This is positive number")
        elif int(i) < 0:
            print("This is negative number")
        else:
            print("This is zero")

