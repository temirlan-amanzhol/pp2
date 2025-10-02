class MyString:

    def __init__(self):  # Инициализация переменной self.txt
        self.txt = ""

    def getString(self):
        self.txt = input("Enter: ")  # Сохраняем введенную строку в self.txt

    def printString(self):
        print(self.txt.upper())  # Печатаем строку в верхнем регистре

# Пример использования
my_string = MyString()
my_string.getString()  # Ввод строки
my_string.printString()  # Печать строки в верхнем регистре


#2
class Shape:
    def __init__(self):
        pass  # У класса Shape нет инициализации атрибутов

    def area(self):
        return 0  # Площадь для базового класса всегда равна 0

class Square(Shape):
    def __init__(self, length):
        self.length = length  # Инициализация длины стороны квадрата

    def area(self):
        return self.length * self.length  # Площадь квадрата (сторона^2)

# Пример использования
shape = Shape()
print("Shape area:", shape.area())  # Для объекта класса Shape площадь будет 0

square = Square(5)
print("Square area:", square.area())  # Для объекта класса Square площадь будет 25 (5^2)


#3
class Shape:
    def __init__(self):
        pass  # У класса Shape нет инициализации атрибутов

    def area(self):
        return 0  # Площадь для базового класса всегда равна 0

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length  # Длина прямоугольника
        self.width = width    # Ширина прямоугольника

    def area(self):
        return self.length * self.width  # Площадь прямоугольника (длина * ширина)

# Пример использования
shape = Shape()
print("Shape area:", shape.area())  # Для объекта класса Shape площадь будет 0

rectangle = Rectangle(5, 3)
print("Rectangle area:", rectangle.area())  # Для объекта класса Rectangle площадь будет 15 (5*3)


#4
import math

class Point:
    def __init__(self, x, y):
        self.x = x  # Координата x
        self.y = y  # Координата y

    def show(self):
        # Метод для отображения координат точки
        print(f"Point coordinates: ({self.x}, {self.y})")

    def move(self, dx, dy):
        # Метод для изменения координат точки
        self.x += dx
        self.y += dy
        print(f"Point moved to: ({self.x}, {self.y})")

    def dist(self, other_point):
        # Метод для вычисления расстояния между двумя точками
        distance = math.sqrt((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2)
        return distance

# Пример использования
point1 = Point(1, 2)
point2 = Point(4, 6)

point1.show()  # Показать координаты первой точки
point2.show()  # Показать координаты второй точки

point1.move(2, 3)  # Переместить первую точку на (2, 3)

distance = point1.dist(point2)  # Вычислить расстояние между двумя точками
print(f"Distance between point1 and point2: {distance}")


#5
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner  # Владелец счёта
        self.balance = balance  # Баланс счёта

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount  # Увеличиваем баланс на сумму депозита
            print(f"Deposited {amount}. New balance: {self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount <= self.balance:  # Проверяем, что сумма снятия не превышает баланс
            self.balance -= amount  # Уменьшаем баланс на сумму снятия
            print(f"Withdrew {amount}. New balance: {self.balance}")
        else:
            print("Insufficient funds for this withdrawal.")

# Пример использования
account = BankAccount("John Doe", 1000)

# Совершаем депозиты и снятия
account.deposit(500)  # Депозит 500
account.withdraw(200)  # Снятие 200
account.withdraw(2000)  # Попытка снятия более чем на балансе

# Проверка, что снятие не может быть больше, чем баланс
account.deposit(300)  # Депозит 300
account.withdraw(1500)  # Снятие 1500


#6
# Функция для проверки простого числа
is_prime = lambda x: x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1))

# Список чисел
numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

# Использование filter с lambda для фильтрации простых чисел
prime_numbers = list(filter(is_prime, numbers))

print("Prime numbers:", prime_numbers)
