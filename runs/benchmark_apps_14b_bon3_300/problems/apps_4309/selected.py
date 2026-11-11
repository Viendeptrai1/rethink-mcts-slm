import sys

def find_earliest_abc(N):
    while True:
        if len(set(str(N))) == 1:
            return N
        N += 1

if __name__ == "__main__":
    N = int(sys.stdin.read().strip())
    result = find_earliest_abc(N)
    print(result)