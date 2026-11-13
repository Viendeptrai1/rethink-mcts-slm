import sys

def read_input():
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    citizens = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n)]
    return n, citizens

def min_unusefulness(citizens):
    n = len(citizens)
    a = sum(y - x for x, y in citizens) / n
    return a

if __name__ == "__main__":
    n, citizens = read_input()
    result = min_unusefulness(citizens)
    print(f"{result:.6f}")