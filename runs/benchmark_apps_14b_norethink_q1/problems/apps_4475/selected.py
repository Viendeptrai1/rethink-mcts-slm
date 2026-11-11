import sys

def min_product(a, b, x, y, n):
    # Calculate the maximum possible reduction for a and b
    max_reduce_a = a - x
    max_reduce_b = b - y
    
    # If total possible reduction is less than or equal to n, reduce fully
    if max_reduce_a + max_reduce_b <= n:
        return x * y
    
    # Binary search to find the optimal number of reductions
    low, high = 0, n
    best_product = float('inf')
    
    while low <= high:
        mid = (low + high) // 2
        
        # Try reducing a by mid and b by n - mid
        new_a = a - mid
        new_b = b - (n - mid)
        
        # Ensure new_a and new_b are within bounds
        new_a = max(new_a, x)
        new_b = max(new_b, y)
        
        current_product = new_a * new_b
        best_product = min(best_product, current_product)
        
        # Try reducing b by mid and a by n - mid
        new_a = a - (n - mid)
        new_b = b - mid
        
        # Ensure new_a and new_b are within bounds
        new_a = max(new_a, x)
        new_b = max(new_b, y)
        
        current_product = new_a * new_b
        best_product = min(best_product, current_product)
        
        if new_a == x and new_b == y:
            break
        
        if new_a > x or new_b > y:
            low = mid + 1
        else:
            high = mid - 1
    
    return best_product

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        a = int(data[index])
        b = int(data[index + 1])
        x = int(data[index + 2])
        y = int(data[index + 3])
        n = int(data[index + 4])
        index += 5
        results.append(min_product(a, b, x, y, n))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()