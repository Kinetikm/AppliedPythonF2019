#!/usr/bin/env python
# coding: utf-8


def calculator(x: "First argument",
               y: "Second argument",
               operator: "From set: plus, minus, mult, divide, power"):
    if operator == "plus":
        return x + y
    if operator == "minus":
        return x - y
    if operator == "mult":
        return x * y
    if operator == "divide":
        if y != 0:
            return x / y
        return x / y
    if operator == "power":
        return x ^ y
    return None
