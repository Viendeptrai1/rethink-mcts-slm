import sys

def find_first_multiple_of_k(K):
    num = 7
    length = 1
    while True:
        if num % K == 0:
            return length
        length += 1
        num = num * 10 + 7

def main():
    K = int(sys.stdin.read().strip())
    result = find_first_multiple_of_k(K)
    sys.stdout.write(str(result))

if __name__ == "__main__":
    main()