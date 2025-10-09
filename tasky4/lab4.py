#squre
def pow(n):
    result = []
    for i in range(n + 1):
        result.append(i ** 2)
    return result

print(pow(5))

#even num
def ev(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

n = int(input())
print(",".join(map(str, ev(n))))



def tfd(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

for i in tfd(70):
    print(i)


def tfs(a , b):
    for i in range (a, b + 1):
        yield i ** 2

for x in tfs(1, 6):
    print(x)



    def boo(n):
        while n >= 0:
            yield i
            n -= 1

for x in boo(6):
    print(x)

    