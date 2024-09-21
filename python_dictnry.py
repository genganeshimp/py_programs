https://www.dataquest.io/blog/python-dictionaries/

del
update
popitems()
pop(key)
get()  #like coalese in sql VERY IMPORTANT
counter(dct)
len(dct)

Q) Difference b/w pop and del

dictionary = dict(key1="value1", key2="value2")
dictionary = dict([("key1", "value1"), ("key2", "value2")])
''' 
Integers, floats, strings, and tuples are hashable data types (and they are also immutable) while lists are an unhashable data type 
(and they are mutable). Python uses hash values to quickly access a dictionary's values.
On the other hand, values can be of whatever type
'''
# Hashing various data types
print(hash(1)) # Integer
print(hash(1.2)) # Float
print(hash("dataquest")) # String
print(hash((1, 2))) # Tuple
print(hash([1, 2, 3]))

#*****Very IMPORTANT********#
# Dictionary with duplicate keys
duplicated_keys = {"key1": "value1", "key1": "value2", "key1": "value3"}

# Access key1
print(duplicated_keys["key1"])
'''
Only the value of the last key is returned, so we can technically use duplicate keys, 
but it's not recommended because one of the strengths of dictionaries is to quickly retrieve a value associated with some key. 
'''

dict1={'a':1,'b':2,'c':3}
dict2={'d':4,'e':5}

dict1.update(dict2)
print(dict1)

dict1={'a':1,'b':2,'c':3}
lst=[['d',4],['e',5]]

dict1.update(lst)
print(dict1)


dict1={'a':1,'b':2,'c':3}
lst=[('d',4),('e',5)]

dict1.update(lst)
print(dict1)

dict1={'a':1,'b':2,'c':3}
dict1.popitem()
print(dict1)

dict1={'a':1,'b':2,'c':3}
dict1.pop('a')
print(dict1)

dict1={'a':1,'b':2,'c':3}
print(dict1.pop('a'))

students = {1: "Neha", 2: "Nidhi", 3: "Sanath"}
for element in students.items():
    print(element)
    
for key,value in students.items():
    print(key,value)

dict1={'a':1,'b':2,'c':3}

print(dict1.get('a','key a not exists'))
print(dict1.get('d','key d not exists'))

#Delete element 
del students[1]
print(students)

if 4 not in students:
    print('4 is not a key')

if 2 in students:
    print('2 is a key in dict')

#Adding element
students[4]='Ganesh'

print(students)

lst = ["apple", "banana", "apple", "orange", "banana", "apple"]
dt = {}

for i in lst:
    if i in dt:
        dt[i]=dt[i]+1
    else:
        dt[i]=1
print(dt)

#Example: update_dict({'a': [1]}, [('a', 2), ('b', 3), ('a', 4)]) should return {'a': [1, 2, 4], 'b': [3]}

lst=[('a', 2), ('b', 3), ('a', 4)]

dct={'a':[1]}


for tpl in lst:
    print(dct)
    if tpl[0] in dct:
        lst=dct[tpl[0]]
        lst=lst.append(tpl[1])
    else:
        dct[tpl[0]]=[tpl[1]]
print(dct)


#Example: dict_to_list({'b': 2, 'a': 1, 'c': 3}) should return [('a', 1), ('b', 2), ('c', 3)]
dct={'b': 2, 'a': 1, 'c': 3}
lst=[]
for key,value in dct.items():
    lst.append((key,value))
print(lst)

#Example: max_key({'a': 5, 'b': 3, 'c': 5}) should return ['a', 'c']
dct={'a': 5, 'b': 3, 'c': 5}
lst=[]
mx=0
for key,value in dct.items():
    if value>mx:
        mx=value
        lst=[key]
    elif value==mx:
        lst.append(key)
print(lst)

#we can use i,j in place of key,value
#Example: remove_key({'a': 1, 'b': 2}, 'b') should return {'a': 1}. If the key 'c' is removed from the same dictionary, it should return 'Key not found'.
dct={'a': 1, 'b': 2,'c':3}

lst=['c','d']

for i in lst:
    try:
        del dct[i]
    except:
        print(i, "not found")
print(dct)
    
#Example: common_keys({'a': 1, 'b': 2}, {'b': 3, 'c': 4}) should return ['b']
dict1={'a': 1, 'b': 2}
dict2={'b': 3, 'c': 4}

lst=[]
for key in dict1.keys():
    if key in dict2.keys():
        lst.append(key)
print(lst)


