def can_hit_all_targets(N, targets):
    x_coords = [target[0] for target in targets]
    y_coords = [target[1] for target in targets]

    def check_line(coords):
        return len(set(coords)) == 1

    return check_line(x_coords) or check_line(y_coords)

import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
targets = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N)]

result = "success" if can_hit_all_targets(N, targets) else "failure"
print(result)