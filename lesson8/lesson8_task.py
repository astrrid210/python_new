# == Лото ==
#
# Правила игры в лото.
#
# Игра ведется с помощью спе циальных карточек, на которых отмечены числа,
# и фишек (бочонков) с цифрами.
#
# Количество бочонков — 90 штук (с цифрами от 1 до 90).
#
# Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр,
# расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:
#
# --------------------------
#     9 43 62          74 90
#  2    27    75 78    82
#    41 56 63     76      86
# --------------------------
#
# В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается
# случайная карточка.
#
# Каждый ход выбирается один случайный бочонок и выводится на экран.
# Также выводятся карточка игрока и карточка компьютера.
#
# Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
# Если игрок выбрал "зачеркнуть":
#     Если цифра есть на карточке - она зачеркивается и игра продолжается.
#     Если цифры на карточке нет - игрок проигрывает и игра завершается.
# Если игрок выбрал "продолжить":
#     Если цифра есть на карточке - игрок проигрывает и игра завершается.
#     Если цифры на карточке нет - игра продолжается.
#
# Побеждает тот, кто первый закроет все числа на своей карточке.
#
# Пример одного хода:
#
# Новый бочонок: 70 (осталось 76)
# ------ Ваша карточка -----
#  6  7          49    57 58
#    14 26     -    78    85
# 23 33    38    48    71
# --------------------------
# -- Карточка компьютера ---
#  7 87     - 14    11
#       16 49    55 88    77
#    15 20     -       76  -
# --------------------------
# Зачеркнуть цифру? (y/n)
#
# Подсказка: каждый следующий случайный бочонок из мешка удобно получать
# с помощью функции-генератора.
#
# Подсказка: для работы с псевдослучайными числами удобно использовать
# модуль random: http://docs.python.org/3/library/random.html

from random import randint


def generate_nums(count, minimum, maximum):
    if count > maximum - minimum + 1:
        raise ValueError('Wrong data')
    ret = []
    while len(ret) < count:
        new = randint(minimum, maximum)
        if new not in ret:
            ret.append(new)
    return ret


class Keg:
    __num = None

    def __init__(self):
        self.__num = randint(1, 90)

    @property
    def num(self):
        return self.__num

    def __str__(self):
        return str(self.__num)


class Card:
    __rows = 3
    __cols = 9
    __nums_in_row = 5
    __data = None
    __empty_num = 0
    __crossed_num = -1

    def __init__(self):
        uniques_count = self.__nums_in_row * self.__rows
        uniques = generate_nums(uniques_count, 1, 90)

        self.__data = []
        for i in range(0, self.__rows):
            tmp = sorted(uniques[self.__nums_in_row * i: self.__nums_in_row * (i + 1)])
            empty_nums_count = self.__cols - self.__nums_in_row
            for j in range(0, empty_nums_count):
                index = randint(0, len(tmp))
                tmp.insert(index, self.__empty_num)
            self.__data += tmp

    def __str__(self):
        delimiter = '--------------------------'
        ret = delimiter + '\n'
        for index, num in enumerate(self.__data):
            if num == self.__empty_num:
                ret += '  '
            elif num == self.__crossed_num:
                ret += ' -'
            elif num < 10:
                ret += f' {str(num)}'
            else:
                ret += str(num)

            if (index + 1) % self.__cols == 0:
                ret += '\n'
            else:
                ret += ' '

        return ret + delimiter

    def __contains__(self, item):
        return item in self.__data

    def cross_num(self, num):
        for index, item in enumerate(self.__data):
            if item == num:
                self.__data[index] = self.__crossed_num
                return
        raise ValueError(f'Number not in card: {num}')

    def closed(self) -> bool:
        return set(self.__data) == {self.__empty_num, self.__crossed_num}


class Game:
    __user_card = None
    __computer_card = None
    __keg_num = 90
    __kegs = []
    __game_over = False

    def __init__(self):
        self.__user_card = Card()
        self.__computer_card = Card()
        self.__kegs = generate_nums(self.__keg_num, 1, 90)

    def play_round(self) -> int:

        keg = self.__kegs.pop()
        print(f'New keg: {keg} ( {len(self.__kegs)}) left')
        print(f'----- Your card ------\n{self.__user_card}')
        print(f'-- Computer card ---\n{self.__computer_card}')

        user_answer = input('Cross out? (y/n)').lower().strip()
        if user_answer == 'y' and not keg in self.__user_card or \
           user_answer != 'y' and keg in self.__user_card:
            return 2

        if keg in self.__user_card:
            self.__user_card.cross_num(keg)
            if self.__user_card.closed():
                return 1
        if keg in self.__computer_card:
            self.__computer_card.cross_num(keg)
            if self.__computer_card.closed():
                return 2

        return 0


if __name__ == '__main__':
    game = Game()
    while True:
        score = game.play_round()
        if score == 1:
            print('Great, you win!')
            break
        elif score == 2:
            print('You lose')
            break
