import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = []
    for i in range(n):
        a.append(int(data[i+1]))
    
    # Count the number of factors of 2 in each number
    count = 0
    for x in a:
        while x % 2 == 0:
            x //= 2
            count += 1
    
    print(count)

if __name__ == "__main__":
    solve()