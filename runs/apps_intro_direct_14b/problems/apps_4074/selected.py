import sys

def min_packages(n, k):
    # If k is greater than or equal to n, the best option is to buy one package of size n
    if k >= n:
        return 1
    # Otherwise, we need to find the smallest number of packages of size i (1 <= i <= k)
    # such that i * num_packages = n. This is equivalent to finding the smallest num_packages
    # which is n // i for some i. The optimal i is the largest divisor of n that is <= k.
    # This can be found by iterating from k down to 1 and checking divisibility.
    for i in range(k, 0, -1):
        if n % i == 0:
            return n // i

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        index += 1
        k = int(data[index])
        index += 1
        results.append(min_packages(n, k))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()