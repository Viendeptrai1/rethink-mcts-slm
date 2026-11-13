import sys

def draw_cardiogram(a):
    total = sum(a)
    max_y = total
    current_y = 0
    points = []

    for x, value in enumerate(a):
        if current_y + value > max_y:
            max_y = current_y + value
        if current_y - value < 0:
            current_y = 0
        else:
            current_y -= value
        points.append((x + 1, current_y))

    # Draw the cardiogram
    result = [[' '] * total for _ in range(max_y)]
    for x, y in points:
        if y == 0:
            result[y][x-1] = '\\'
        elif y == max_y - 1:
            result[y][x-1] = '/'
        else:
            result[y][x-1] = ' '

    return '\n'.join(''.join(row) for row in reversed(result))

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    a = list(map(int, data[1:]))

    print(draw_cardiogram(a))