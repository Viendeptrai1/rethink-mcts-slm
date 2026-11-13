def int_to_mini_roman(number):
    # Define a mapping of Roman numeral symbols to integers
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syms = [
        "m", "cm", "d", "cd",
        "c", "xc", "l", "xl",
        "x", "ix", "v", "iv",
        "i"
    ]
    # Initialize result string
    roman_num = ''
    i = 0
    # Convert number to mini roman numeral
    while number > 0:
        for _ in range(number // val[i]):
            roman_num += syms[i]
            number -= val[i]
        i += 1
    return roman_num