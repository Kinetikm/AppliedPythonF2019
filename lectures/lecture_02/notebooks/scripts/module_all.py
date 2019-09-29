import math as ma_math


def _ma_private_function():
    print('_ma_private_function')


def ma_public_function():
    print('ma_public_function')


__all__ = ['_ma_private_function', 'ma_math']
