import sys

def min_packages(n, k):
    # If k is greater than or equal to n, the best option is to buy one package of size n
    if k >= n:
        return 1
    # Otherwise, we need to find the smallest number of packages of size i (1 <= i <= k)
    # such that i * num_packages = n. This is equivalent to finding the smallest num_packages
    # which is n // i, and ensuring that n % i == 0.
    # The optimal i will be the largest possible that divides n, which is min(k, n).
    # So we calculate n // min(k, n).
    return (n + min(k, n) - 1) // min(k, n)

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