import sys

def draw_cardiogram(n, a):
    total_sum = sum(a)
    max_height = total_sum
    lines = [' ' * total_sum] * max_height
    
    x = 0
    y = 0
    direction = 1
    
    for i in range(n):
        if direction == 1:
            for j in range(a[i]):
                if y < max_height:
                    lines[y] = lines[y][:x] + '/' + lines[y][x+1:]
                x += 1
                y += 1
            direction = -1
        else:
            for j in range(a[i]):
                if y > 0:
                    lines[y-1] = lines[y-1][:x] + '\\' + lines[y-1][x+1:]
                x += 1
                y -= 1
            direction = 1
    
    for line in reversed(lines):
        print(line)

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Draw cardiogram
draw_cardiogram(n, a)