import math
from sys import stdin, stdout

def find_sequence(n, k):
    if n < k:
        return -1
    
    gcd = n // k
    if gcd * k != n:
        return -1
    
    sequence = [i * gcd for i in range(1, k + 1)]
    
    if sum(sequence) == n:
        return sequence
    else:
        return -1

def main():
    n, k = map(int, stdin.readline().split())
    result = find_sequence(n, k)
    if result == -1:
        stdout.write("-1\n")
    else:
        stdout.write(" ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()