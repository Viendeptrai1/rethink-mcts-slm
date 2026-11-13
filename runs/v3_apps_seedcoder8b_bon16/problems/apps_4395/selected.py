def minimum_recolor_for_nice_garland(n, s):
    # Function to calculate the minimum recolor needed for a specific pattern
    def calculate_recolors(pattern):
        recolor_count = 0
        for i in range(n):
            if s[i] != pattern[i % 3]:
                recolor_count += 1
        return recolor_count

    # Generate all possible nice patterns
    patterns = ["RGB", "RBG", "GRB", "GBR", "BRG", "BGR"]
    
    # Calculate the number of recolors needed for each pattern
    min_recolor = float('inf')
    best_pattern = ""
    
    for pattern in patterns:
        recolor_count = calculate_recolors(pattern)
        if recolor_count < min_recolor:
            min_recolor = recolor_count
            best_pattern = pattern
    
    # Construct the resulting nice garland string
    nice_garland = ''.join(best_pattern[i % 3] for i in range(n))
    
    return min_recolor, nice_garland

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result = minimum_recolor_for_nice_garland(n, s)
    
    print(result[0])
    print(result[1])

if __name__ == "__main__":
    main()