# 1. Реализовать класс Matrix (матрица).
# Обеспечить перегрузку конструктора класса (метод __init__()),
# который должен принимать данные (список списков) для формирования матрицы.
# Подсказка: матрица — система некоторых математических величин, расположенных в виде прямоугольной схемы.
# Примеры матриц вы найдете в методичке.
# Следующий шаг — реализовать перегрузку метода __str__() для вывода матрицы в привычном виде.
# Далее реализовать перегрузку метода __add__() для реализации операции сложения двух объектов
# класса Matrix (двух матриц). Результатом сложения должна быть новая матрица.
# Подсказка: сложение элементов матриц выполнять поэлементно —
# первый элемент первой строки первой матрицы складываем с первым элементом первой строки второй матрицы и т.д.

class Matrix:
    def __init__(self, data):
        self.input = data

    def __str__(self):
        return '\n'.join([' '.join([str(el) for el in line]) for line in self.input])

    def __add__(self, other):
        answer = ''
        if len(self.input) == len(other.input):
            for line1, line2 in zip(self.input, other.input):
                if len(line1) != len(line2):
                    return 'Wrong data'

                sum_line = [x + y for x, y in zip(line1, line2)]
                answer += ' '.join([str(i) for i in sum_line]) + '\n'
        else:
            return 'Wrong data'
        return answer


matrix1 = Matrix([[10, 20], [30, 40], [50, 60], [70, 80]])
matrix2 = Matrix([[20, 30], [40, 50], [60, 70], [80, 90]])

print(matrix1)
print()
print(matrix1 + matrix2)
