#1
import math
l = [1, 5, 6, 7]
mul = math.prod(l)
print(mul)

#2
def count(s):
    up = sum(1 for x in s if x.upper())
    low = sum(1 for x in s if x.lower())
    print(up)
    print(low)

count("YOOOOOOOOoooo")

#3
def palindro(s):
    s=s.replace(" ", "").lower()
    return s == s[::-1]

print(palindro("AGGA"))

#4
import math
import time

n = 25600
d = 2134

time.sleep(d/1000)
res = math.sgrt(n)

print(res)

#5
t = (True, True, True)
print(all(t))
f = (False, False, False)
print(all(f))


#1
import os

path = '.'
dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

print("Directories:", dirs)
print("Files:", files)

#2
import os

path = "test.txt"

print("Exists:", os.access(path, os.F_OK))
print("Readable:", os.access(path, os.R_OK))
print("Writable:", os.access(path, os.W_OK))
print("Executable:", os.access(path, os.X_OK))

#3
import os

path = "example/test.txt"

if os.path.exists(path):
    print("Filename:", os.path.basename(path))
    print("Directory:", os.path.dirname(path))
else:
    print("Path does not exist.")

#4
filename = "example.txt"

with open(filename, 'r') as f:
    lines = f.readlines()
    print("Number of lines:", len(lines))

#5
colors = ['red', 'green', 'blue']

with open('colors.txt', 'w') as f:
    for color in colors:
        f.write(color + '\n')

#6
import string

for letter in string.ascii_uppercase:
    with open(f"{letter}.txt", 'w') as f:
        f.write(f"This is file {letter}.txt")

#7
with open('source.txt', 'r') as src, open('destination.txt', 'w') as dest:
    dest.write(src.read())

#8
import os

path = "old.txt"

if os.path.exists(path):
    os.remove(path)
    print("File deleted successfully")
else:
    print("File does not exist")
