print("Data types:")

# String (Text)
strData = "This is a string value"
print(type(strData))

# Numbers
intData = 9
floatData = 9.0
complexData = 9j
print(type(intData))
print(type(floatData))
print(type(complexData))

# Range
rangeData = range(3)    # for automatic iterations
print(type(rangeData))
for i in rangeData:
    print(i)

# Collections
listData = ["Apple", "Banana", "Orange", 2]    # common list -> Insertion and deletion are O(1)
print(type(listData))
for i in listData:
    print(i)
tupleData = ("Tuple1", "Tuple2", 10)    # commonly used for function return
print(type(tupleData))
for i in tupleData:
    print(i)

dictData = {"name1": "Carlos", "name2": "Guilherme"}    # Default Dictionary -> Average O(1)
print(type(dictData))
for i in dictData.values():     # in values
    print(i)
for i in dictData.keys():   # in keys
    print(i)
for i in dictData.items():  # key value pair
    print(type(i))
    print(i[0])     # key
    print(i[1])     # value

print(dictData["name1"])
print(dictData["name2"])

setData = {"not_changed1", "not_changed2"}
# can not do setData[i]
print(type(setData))
for i in range(len(setData)):
    print(setData.pop())

# Boolean
boolData = True
print(type(boolData))
print(f"{boolData}")
boolData = False
print(f"{boolData}")

# Casting
strData = str(boolData)
print(type(strData))
print(boolData)
strData = "10.5"
floatData = 10.4 + float(strData)
print(floatData)
strData = "10"
intData = int("20") - int("53")
print(intData)


