import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = []
    for i in range(1, n + 1):
        a.append(int(data[i]))
    
    total_ops = 0
    for x in a:
        while x % 2 == 0:
            x //= 2
            total_ops += 1
    
    print(total_ops)

if __name__ == "__main__":
    solve()