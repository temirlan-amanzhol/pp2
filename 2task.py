# 1. Граммы → унции
def grams_to_ounces(grams):
    return grams / 28.3495231

# 2. F → C
def fahrenheit_to_celsius(f):
    return (5 / 9) * (f - 32)

# 3. Куры и кролики
def solve(numheads, numlegs):
    # h + r = heads, 2h + 4r = legs
    r = (numlegs - 2 * numheads) // 2
    c = numheads - r
    return c, r

# 4. Фильтр простых чисел
def filter_prime(numbers):
    def is_prime(n):
        if n < 2: return False
        for i in range(2, int(n**0.5)+1):
            if n % i == 0: return False
        return True
    return [n for n in numbers if is_prime(n)]

# 5. Все перестановки строки
import itertools
def string_permutations(s):
    return [''.join(p) for p in itertools.permutations(s)]

# 6. Перевернуть слова в предложении
def reverse_words(sentence):
    return ' '.join(sentence.split()[::-1])

# 7. Проверка 33
def has_33(nums):
    for i in range(len(nums)-1):
        if nums[i] == 3 and nums[i+1] == 3:
            return True
    return False

# 8. Проверка на 0,0,7
def spy_game(nums):
    code = [0,0,7]
    for n in nums:
        if n == code[0]:
            code.pop(0)
            if not code: return True
    return False

# 9. Объём сферы
import math
def sphere_volume(r):
    return (4/3) * math.pi * r**3

# 10. Уникальные элементы без set
def unique_list(lst):
    res = []
    for x in lst:
        if x not in res:
            res.append(x)
    return res

# 11. Палиндром
def is_palindrome(s):
    s = ''.join(s.lower().split())
    return s == s[::-1]

# 12. Гистограмма
def histogram(lst):
    for n in lst:
        print('*' * n)

# 13. Игра "угадай число"
import random
def guess_number():
    print("Hello! What is your name?")
    name = input()
    print(f"Well, {name}, I am thinking of a number between 1 and 20.")
    number = random.randint(1, 20)
    guesses = 0
    while True:
        print("Take a guess.")
        guess = int(input())
        guesses += 1
        if guess < number:
            print("Your guess is too low.")
        elif guess > number:
            print("Your guess is too high.")
        else:
            print(f"Good job, {name}! You guessed my number in {guesses} guesses!")
            break
