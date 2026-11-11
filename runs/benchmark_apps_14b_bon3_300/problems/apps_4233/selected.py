import sys

def read_input():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    grid = []
    index = 2
    for i in range(n):
        grid.append(data[index])
        index += 1
    
    return n, m, grid

def is_possible_to_draw(grid, n, m):
    for i in range(1, n-1):
        for j in range(1, m-1):
            if grid[i][j] == '*':
                if grid[i-1][j] != '*' or grid[i+1][j] != '*' or grid[i][j-1] != '*' or grid[i][j+1] != '*':
                    return False
    return True

def find_stars(grid, n, m):
    stars = []
    for i in range(1, n-1):
        for j in range(1, m-1):
            if grid[i][j] == '*':
                size = 1
                while i-size >= 1 and i+size <= n-2 and j-size >= 1 and j+size <= m-2:
                    if grid[i-size][j] == '*' and grid[i+size][j] == '*' and grid[i][j-size] == '*' and grid[i][j+size] == '*':
                        size += 1
                    else:
                        break
                size -= 1
                stars.append((i+1, j+1, size))
    return stars

def main():
    n, m, grid = read_input()
    if not is_possible_to_draw(grid, n, m):
        print(-1)
        return
    
    stars = find_stars(grid, n, m)
    print(len(stars))
    for star in stars:
        print(star[0], star[1], star[2])

if __name__ == "__main__":
    main()