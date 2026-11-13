def min_cost_preparation_and_printing(n, k, a, b):
    # Sort the preparation costs and printing costs separately
    a_sorted = sorted(a)
    b_sorted = sorted(b)
    
    # The minimum cost will be the sum of the first k elements from both sorted lists
    min_cost = sum(a_sorted[:k]) + sum(b_sorted[:k])
    
    return min_cost

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:n+2]))
    b = list(map(int, data[n+2:2*n+2]))
    
    result = min_cost_preparation_and_printing(n, k, a, b)
    print(result)