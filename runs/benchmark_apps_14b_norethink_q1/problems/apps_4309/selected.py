import sys

def find_next_abc_with_same_digits(N):
    while True:
        str_N = str(N)
        if len(set(str_N)) == 1:
            return N
        N += 1

def main():
    N = int(sys.stdin.read().strip())
    result = find_next_abc_with_same_digits(N)
    print(result)

if __name__ == "__main__":
    main()