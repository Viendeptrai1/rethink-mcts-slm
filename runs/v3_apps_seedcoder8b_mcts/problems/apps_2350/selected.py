def count_different_sums(x1, y1, x2, y2):
    # Calculate the number of different sums on the path from (x1, y1) to (x2, y2)
    # The number of different sums is determined by the number of unique paths
    # which is equal to the number of ways to choose (x2 - x1) steps down from the total
    # steps (x2 - x1 + y2 - y1) taken to reach (x2, y2).
    
    from math import comb
    
    # Total steps to reach (x2, y2)
    total_steps = (x2 - x1) + (y2 - y1)
    
    # Number of steps to go down
    down_steps = x2 - x1
    
    # Number of different paths is the combination of down_steps taken in total_steps
    return comb(total_steps, down_steps)

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