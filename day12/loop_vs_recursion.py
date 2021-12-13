#!/usr/bin/env python3

def reverse_string(string):
    reverse = ''

    length = len(string) - 1
    while length >= 0:
        reverse = reverse + string[length]
        length = length - 1
    
    return reverse


def reverse_string_recursion(string):
    """
    conversion: use the loop condition as the base case and the body of the
    loop as the recursive case.
    """

    if len(string) == 0:  # base case (often loop control condition)
        return ''

    # recursive case (often loop body)
    return reverse_string_recursion(string[1:]) + string[0]


data = 'Educative'
print(data[::-1])
print(reverse_string(data))
print(reverse_string(data))
