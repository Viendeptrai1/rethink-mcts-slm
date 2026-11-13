def even_odd_count(num):
    num = abs(num)
    count_even = sum(1 for digit in str(num) if int(digit) % 2 == 0)
    count_odd = sum(1 for digit in str(num) if int(digit) % 2 != 0)
    return (count_even, count_odd)