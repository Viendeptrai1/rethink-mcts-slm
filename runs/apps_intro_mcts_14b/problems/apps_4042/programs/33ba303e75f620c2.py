import sys

def find_closest_factors(x):
    target = int(x * 100)
    best_diff = float('inf')
    best_pair = (1, 1)
    
    for i in range(1, 11):
        for j in range(1, 11):
            product = i * j
            diff = abs(product - target)
            if diff < best_diff:
                best_diff = diff
                best_pair = (i, j)
    
    return best_pair

def main():
    import sys
    x = float(sys.stdin.read().strip())
    result = find_closest_factors(x)
    print(result[0], result[1])

if __name__ == "__main__":
    main()