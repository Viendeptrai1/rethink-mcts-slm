import sys

def find_interesting_number(a):
    while True:
        if sum(int(digit) for digit in str(a)) % 4 == 0:
            return a
        a += 1

if __name__ == "__main__":
    a = int(sys.stdin.read().strip())
    result = find_interesting_number(a)
    print(result)