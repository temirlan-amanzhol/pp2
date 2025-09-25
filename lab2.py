#booleans
print(10 > 1)
print(5 < 2)
print(3==3)

#if else
x = 2
y = 4
if x > y:
    print("NO")
else:
    print("YES")

#while loops

r = 1
while r < 8:
    print(r)
    r += 1

#match

day = 4
match day:
  case 1:
    print("Monday")
  case 2:
    print("Tuesday")
  case 3:
    print("Wednesday")
  case 4:
    print("Thursday")
  case 5:
    print("Friday")
  case 6:
    print("Saturday")
  case 7:
    print("Sunday")

#tuple unchangable

t = ("i" , "hate" , "losers")
print(t)

thistuple = ("apple", "banana", "cherry")
print(thistuple[-1])

#operators 

1 + 2
3 - 1
5 * 1
6 / 2
5 % 2
5 ** 2

#dictinary

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
x = thisdict["model"]

#2 dictinary
car = {
"brand": "Ford",
"model": "Mustang",
"year": 1964
}

x = car.keys()

print(x) #before the change

car["color"] = "white"

print(x) #after the change


#3 dictionary
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
mydict = thisdict.copy()
print(mydict)              # Make a copy of a dictionary with the copy() method:

# three dictionaries
myfamily = {
  "child1" : {
    "name" : "Emil",
    "year" : 2004
  },
  "child2" : {
    "name" : "Tobias",
    "year" : 2007
  },
  "child3" : {
    "name" : "Linus",
    "year" : 2011
  }
}

print(myfamily)

# clear()	Removes all the elements from the dictionary
# copy()	Returns a copy of the dictionary
# fromkeys()	Returns a dictionary with the specified keys and value
# get()	Returns the value of the specified key
# items()	Returns a list containing a tuple for each key value pair
# keys()	Returns a list containing the dictionary's keys
# pop()	Removes the element with the specified key
# popitem()	Removes the last inserted key-value pair
# setdefault()	Returns the value of the specified key. If the key does not exist: insert the key, with the specified value
# update()	Updates the dictionary with the specified key-value pairs
# values()	Returns a list of all the values in the dictionary


thislist = ["apple", "banana", "cherry"]
thislist.remove("banana")
print(thislist)         #remove element


thislist = ["apple", "banana", "cherry"]
thislist[1] = "blackcurrant"
print(thislist)         #change 2 element


thislist = ["apple", "banana", "cherry"]
thislist.insert(2, "watermelon")
print(thislist)           #add second element to thw list 


# Using the append() method to append an item:

thislist = ["apple", "banana", "cherry"]
thislist.append("orange")
print(thislist)

# Add the elements of tropical to thislist:

thislist = ["apple", "banana", "cherry"]
tropical = ["mango", "pineapple", "papaya"]
thislist.extend(tropical)
print(thislist)