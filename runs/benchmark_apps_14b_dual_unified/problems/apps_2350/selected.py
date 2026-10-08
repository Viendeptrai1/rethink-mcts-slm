import sys
from math import comb

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        x1 = int(data[index])
        y1 = int(data[index + 1])
        x2 = int(data[index + 2])
        y2 = int(data[index + 3])
        index += 4
        
        # Calculate the number of distinct sums
        if x1 == x2 and y1 == y2:
            results.append(1)
        else:
            dx = x2 - x1
            dy = y2 - y1
            total_steps = dx + dy
            distinct_sums = comb(total_steps, dx)
            results.append(distinct_sums)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()