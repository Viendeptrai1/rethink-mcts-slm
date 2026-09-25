import sys

def sum_of_digits(n):
    return sum(int(digit) for digit in str(n))

def find_interesting_number(a):
    while True:
        if sum_of_digits(a) % 4 == 0:
            return a
        a += 1

def main():
    import sys
    a = int(sys.stdin.read().strip())
    result = find_interesting_number(a)
    print(result)

if __name__ == "__main__":
    main()