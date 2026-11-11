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
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '*':
                # Check if we can place a star centered at (i, j)
                if i < 1 or i >= n-1 or j < 1 or j >= m-1:
                    return False
                if grid[i-1][j] != '*' or grid[i+1][j] != '*' or grid[i][j-1] != '*' or grid[i][j+1] != '*':
                    return False
    return True

def find_stars(grid, n, m):
    stars = []
    for i in range(1, n-1):
        for j in range(1, m-1):
            if grid[i][j] == '*':
                # Find the size of the star
                size = 1
                while i-size >= 0 and i+size < n and j-size >= 0 and j+size < m:
                    if grid[i-size][j] == '*' and grid[i+size][j] == '*' and grid[i][j-size] == '*' and grid[i][j+size] == '*':
                        size += 1
                    else:
                        break
                stars.append((i+1, j+1, size-1))
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