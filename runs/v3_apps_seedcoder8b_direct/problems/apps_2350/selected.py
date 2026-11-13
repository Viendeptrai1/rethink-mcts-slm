def count_different_sums(x1, y1, x2, y2):
    # Calculate the number of different sums on the path from (x1, y1) to (x2, y2)
    # The number of different sums is determined by the number of unique paths
    # from (x1, y1) to (x2, y2) which is equal to the number of ways to arrange
    # (x2 - x1) down moves and (y2 - y1) right moves.
    from math import comb
    
    # The number of unique paths is given by the binomial coefficient
    return comb(x2 - x1 + y2 - y1, x2 - x1)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    
    for i in range(1, t + 1):
        x1 = int(data[4 * (i - 1) + 1])
        y1 = int(data[4 * (i - 1) + 2])
        x2 = int(data[4 * (i - 1) + 3])
        y2 = int(data[4 * (i - 1) + 4])
        
        result = count_different_sums(x1, y1, x2, y2)
        results.append(result)
    
    for res in results:
        print(res)

if __name__ == "__main__":
    main()