from itertools import product

def generate_gray_code(n):
    return [''.join(p) for p in product('01', repeat=n)]

def is_valid_color_code(code, palette):
    for i in range(len(code) - 1):
        diff = sum(c1 != c2 for c1, c2 in zip(code[i], code[i + 1]))
        if diff not in palette:
            return False
    return True

def find_color_code(n, palette):
    gray_code = generate_gray_code(n)
    if is_valid_color_code(gray_code, palette):
        return gray_code
    else:
        return "impossible"

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
p = int(data[1])
palette = list(map(int, data[2:]))

# Find and print the result
result = find_color_code(n, palette)
if result == "impossible":
    print(result)
else:
    for code in result:
        print(code)