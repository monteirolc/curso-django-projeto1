import re
from time import time


def lower(my_str: str) -> str:
    for a in range(26):
        a1 = a + 65
        a2 = a + 97
        my_str = re.sub(chr(a1), chr(a2), my_str)
    return my_str


def upper(my_str: str) -> str:
    for a in range(26):
        a1 = a + 97
        a2 = a + 65
        my_str = re.sub(chr(a1), chr(a2), my_str)
    return my_str


def remove_point(number: float) -> str:
    return re.sub('[.]', '', str(number))


def no_space(my_str: str) -> str:
    return re.sub('\s', '-', my_str)


def end_with_number(my_str: str, nmb: str) -> str:
    return my_str + ' ' + nmb


def myslug(my_str: str) -> str:
    my_str = lower(my_str)
    my_numb = remove_point(float(time()))
    my_str = end_with_number(my_str, my_numb)
    my_str = no_space(my_str)
    return my_str


if __name__ == '__main__':
    print(myslug('This Is My Slug Result'))
