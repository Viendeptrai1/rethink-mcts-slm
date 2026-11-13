import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    k = int(input_data[1])
    
    divisors = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisors.append(i)
            if i * i != n:
                divisors.append(n // i)
        i += 1
    
    divisors.sort()
    
    if len(divisors) < k:
        print(-1)
    else:
        print(divisors[k - 1])

if __name__ == "__main__":
    solve()