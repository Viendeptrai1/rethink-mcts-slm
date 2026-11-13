def min_recolors_to_nice_garland(n, s):
    def check_color(color):
        result = list(s)
        count = 0
        for i in range(n):
            if result[i] != color[(i % 3)]:
                result[i] = color[i % 3]
                count += 1
        return count, ''.join(result)

    colors = ['RGB', 'RBG', 'GRB', 'GBR', 'BRG', 'BGR']
    min_count = float('inf')
    best_result = ''

    for color in colors:
        count, result = check_color(color)
        if count < min_count:
            min_count = count
            best_result = result

    return min_count, best_result

# Input handling
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
s = data[1]

# Output handling
result_count, result_string = min_recolors_to_nice_garland(n, s)
print(result_count)
print(result_string)