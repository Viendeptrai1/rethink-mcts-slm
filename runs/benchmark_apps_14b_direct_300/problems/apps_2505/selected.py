import sys
from itertools import combinations

MOD = 998244353

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    points = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N)]
    
    x_coords = sorted(set(x for x, y in points))
    y_coords = sorted(set(y for x, y in points))
    
    x_index = {x: i for i, x in enumerate(x_coords)}
    y_index = {y: i for i, y in enumerate(y_coords)}
    
    points = [(x_index[x], y_index[y]) for x, y in points]
    
    result = 0
    
    for r in range(1, N + 1):
        for subset in combinations(points, r):
            min_x = min(x for x, y in subset)
            max_x = max(x for x, y in subset)
            min_y = min(y for x, y in subset)
            max_y = max(y for x, y in subset)
            count = (max_x - min_x + 1) * (max_y - min_y + 1)
            result = (result + count) % MOD
    
    print(result)

if __name__ == "__main__":
    main()