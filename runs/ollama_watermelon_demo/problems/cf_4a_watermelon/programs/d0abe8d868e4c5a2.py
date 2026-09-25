import sys

def can_divide_watermelon(w):
    if w % 2 != 0:
        return "NO"
    else:
        for i in range(2, w, 2):
            if (w - i) % 2 == 0 and i > 0 and w - i > 0:
                return "YES"
    return "NO"

# Read input from standard input
input_line = sys.stdin.readline().strip()
weight = int(input_line)

# Print the result to standard output
print(can_divide_watermelon(weight))