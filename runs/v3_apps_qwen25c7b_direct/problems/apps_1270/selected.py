import sys

def bachgold_problem(n):
    if n <= 2:
        return [n]
    
    primes = []
    while n % 2 == 0:
        primes.append(2)
        n //= 2
    
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            primes.append(i)
            n //= i
    
    if n > 2:
        primes.append(n)
    
    return primes

def solve():
    n = int(sys.stdin.read().strip())
    primes = bachgold_problem(n)
    print(len(primes))
    print(' '.join(map(str, primes)))

if __name__ == "__main__":
    solve()