def can_form_congruence(A, B, C):
    return C % GCD(A, B) == 0

def GCD(x, y):
    while(y):
        x, y = y, x % y
    return x

import sys
input = sys.stdin.read
data = input().split()
A = int(data[0])
B = int(data[1])
C = int(data[2])

if can_form_congruence(A, B, C):
    print("YES")
else:
    print("NO")