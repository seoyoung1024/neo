#!/usr/bin/env python


class SmartPhone(object):

    def __init__(self, brand, details):
        self.brand = brand
        self.details = details

    def __str__(self):
        return f'str:{self.brand} - {self.details}'

    def __repr__(self):
        return f'repr:Instance_name = SmartPhone - {self.details})'

    def __doc__(self):
        return f'This class is SmartPhone Class. It is have a brand name and details description'

SmartPhone1 = SmartPhone('Iphone', {'color':"White", "price": 100000})
SmartPhone2 = SmartPhone('Galaxy', {'color':"Black", "price": 80000})
SmartPhone3 = SmartPhone('Blackberry', {'color':"Silver", "price": 60000})

print(SmartPhone.__doc__)
print(dir(SmartPhone1))
print(SmartPhone1)
print(SmartPhone1.__dict__)
print(SmartPhone2.__dict__)
print(SmartPhone3.__dict__)

print(id(SmartPhone1))
print(id(SmartPhone2))
print(id(SmartPhone3))

print(id(SmartPhone1))
print(id(SmartPhone2))
print(id(SmartPhone3))


print(SmartPhone1.brand == SmartPhone2.brand)
print(SmartPhone1 is SmartPhone2)

print(SmartPhone.__str__(SmartPhone1))
print(SmartPhone.__str__(SmartPhone2))
print(SmartPhone.__str__(SmartPhone3))

print(help(SmartPhone))