def find_string(a_00, a_01, a_10, a_11):
    # Check if the sum of all given subsequences is consistent
    total_count = a_00 + a_01 + a_10 + a_11
    if (a_00 + a_11 != a_01 + a_10) or (a_00 + a_01 < a_10):
        print("Impossible")
        return
    
    # Construct the string step by step
    result = []
    
    # We start with an empty list and append characters based on conditions
    while a_00 > 0:
        result.append('0')
        result.append('0')
        a_00 -= 1

    while a_01 > 0:
        result.append('0')
        result.append('1')
        a_01 -= 1

    while a_10 > 0:
        result.append('1')
        result.append('0')
        a_10 -= 1

    while a_11 > 0:
        result.append('1')
        result.append('1')
        a_11 -= 1
    
    # Convert the result list to a string and print
    print(''.join(result))

import sys
input = sys.stdin.read
data = input().strip()
a_00, a_01, a_10, a_11 = map(int, data.split())
find_string(a_00, a_01, a_10, a_11)