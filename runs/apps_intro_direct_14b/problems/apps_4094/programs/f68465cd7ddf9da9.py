import sys

def find_first_multiple_of_k(K):
    num_str = "7"
    for i in range(1, 10**6 + 1):
        if int(num_str) % K == 0:
            return i
        num_str += "7"
    return -1

if __name__ == "__main__":
    K = int(sys.stdin.read().strip())
    result = find_first_multiple_of_k(K)
    sys.stdout.write(str(result))