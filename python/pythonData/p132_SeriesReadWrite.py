from pandas import Series

myindex = ['용산구', '마포구', '영등포구', '서대문구', '광진구', '은평구', '서초구']
myseries = [50, 60, 40, 80, 70, 30, 20]
myseries = Series(data=myseries, index=myindex)
print(myseries)

print('\n read value')
print(myseries['서대문구'])

print('\n slicing label name')
print(myseries['서대문구':'은평구'])

print('\n read using index')
# print(myseries[[2]]) 현재사용안됨
print(myseries.iloc[2]) #인덱스를 할 때는 이렇게 사용

print('\n read using index 0, 2, 4')
print(myseries.iloc[[0, 2, 4]]) 

print('\n slicing index')
print(myseries[0:5:2])

myseries.iloc[2] = 80
print('\n Series list')
print(myseries)

myseries[2:5] = 33
print('\n Series list')
print(myseries)

myseries[['용산구','서대문구']] = 55
print('\n Series list')
print(myseries)

myseries[0::2] = 80
print('\n Series list')
print(myseries)

