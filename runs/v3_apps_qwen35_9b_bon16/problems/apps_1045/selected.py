import sys

def solve():
    input_data = sys.stdin.read().strip()
    if not input_data:
        return
    n = int(input_data)
    
    height = 0
    cubes_used = 0
    level_cubes = 0
    
    while True:
        level_cubes += height + 1
        if cubes_used + level_cubes <= n:
            cubes_used += level_cubes
            height += 1
        else:
            break
    
    print(height)

if __name__ == "__main__":
    solve()