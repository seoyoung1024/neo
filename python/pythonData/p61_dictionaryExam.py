#!/usr/bin/env python

dictictionary = {'김유신':50, '윤봉길' : 40, '김구': 60}
print('Dictionary: ', dictictionary)

for key in dictictionary.keys():
    print(f'key: {key}, value: {dictictionary[key]}')

for value in dictictionary.values():
    print(f'value: {value}')

for key, value in dictictionary.items():
    print('{}의 나이는 {}입니다.'.format(key, dictictionary[key]))

for key, value in dictictionary.items():
    print(f'{key}의 나이는 {value}입니다.')

findkey = '유관순'

if findkey in dictictionary.keys():
    print(f'{findkey}는 존재합니다.')
else:
    print(f'{findkey}는 존재 하지 않습니다.')

result = dictictionary.pop('김구')
print('After pop : ', dictictionary)
print('Result :', result)

dictictionary.clear()
print('Dictionary list : ', dictictionary)
