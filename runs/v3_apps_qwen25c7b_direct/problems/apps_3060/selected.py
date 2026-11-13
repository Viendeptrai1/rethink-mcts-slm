from math import factorial

def count_valid_sequences(n):
    return sum(factorial(n - 1) // (factorial(i) * factorial(n - 1 - i)) for i in range(1, n))

def find_kth_sequence(n, k):
    if n == 2:
        return [k]
    
    total_sequences = count_valid_sequences(n)
    if k > total_sequences:
        raise ValueError("k is greater than the total number of valid sequences")
    
    for i in range(1, n):
        count = factorial(n - 1) // (factorial(i) * factorial(n - 1 - i))
        if k <= count:
            return [i] + find_kth_sequence(n - 1, k)
        k -= count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    k = int(data[1])
    result = find_kth_sequence(n, k)
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()