def mex(s):
    mex = 0
    while mex in s:
        mex += 1
    return mex

def grundy(a):
    if len(a) == 0:
        return 0
    if len(a) == 1:
        return a[0]
    
    grundy_values = set()
    
    # Option 1: Decrease one element by x (1 <= x <= a[i])
    for i in range(len(a)):
        for x in range(1, a[i] + 1):
            new_a = a[:]
            new_a[i] -= x
            grundy_values.add(grundy(new_a))
    
    # Option 2: Decrease all elements by x (1 <= x <= min(a[i]))
    min_a = min(a)
    for x in range(1, min_a + 1):
        new_a = [a_i - x for a_i in a]
        grundy_values.add(grundy(new_a))
    
    return mex(grundy_values)

def determine_winner(n, a):
    if grundy(a) == 0:
        return "BitAryo"
    else:
        return "BitLGM"

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

print(determine_winner(n, a))