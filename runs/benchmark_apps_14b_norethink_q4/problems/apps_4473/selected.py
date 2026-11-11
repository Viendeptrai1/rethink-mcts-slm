import sys

def solve(a, b, k):
    # Calculate the net effect of each pair of jumps
    net_effect_per_pair = a - b
    # Number of complete pairs
    num_complete_pairs = k // 2
    # Result from complete pairs
    result = num_complete_pairs * net_effect_per_pair
    
    # If k is odd, add the result of the final jump
    if k % 2 == 1:
        result += a
    
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        a = int(data[index])
        b = int(data[index + 1])
        k = int(data[index + 2])
        index += 3
        results.append(solve(a, b, k))
    
    print(' '.join(map(str, results)))

if __name__ == "__main__":
    main()