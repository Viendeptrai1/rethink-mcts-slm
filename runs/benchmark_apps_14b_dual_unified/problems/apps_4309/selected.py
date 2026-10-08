import sys

def all_digits_same(n):
    s = str(n)
    return all(c == s[0] for c in s)

def find_earliest_abc(N):
    while True:
        if all_digits_same(N):
            return N
        N += 1

if __name__ == "__main__":
    N = int(sys.stdin.read().strip())
    result = find_earliest_abc(N)
    print(result)