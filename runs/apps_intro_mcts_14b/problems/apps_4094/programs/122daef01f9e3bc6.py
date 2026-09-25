import sys

def find_first_multiple_of_k(K):
    num = 7
    position = 1
    
    while True:
        if num % K == 0:
            return position
        num = num * 10 + 7
        position += 1

if __name__ == "__main__":
    K = int(sys.stdin.read().strip())
    result = find_first_multiple_of_k(K)
    sys.stdout.write(str(result))