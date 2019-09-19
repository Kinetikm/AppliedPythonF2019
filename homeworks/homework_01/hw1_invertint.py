#!/usr/bin/env python
# coding: utf-8


def reverse(number: int) -> int:
    """
    Метод, принимающий на вход int и
    возвращающий инвертированный int
    :param number: исходное число
    :return: инвертированное число
    """
    return (
        int(str(number)[::-1]) if number >= 0 else int(str(number * (-1))[::-1]) * (-1)
    )
