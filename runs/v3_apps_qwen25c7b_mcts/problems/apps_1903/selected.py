def max_significance(n, m, d, physics_cups, informatics_cups):
    physics_cups.sort(key=lambda x: (-x[0], -x[1]))
    informatics_cups.sort(key=lambda x: (-x[0], -x[1]))

    if physics_cups[0][1] > d or informatics_cups[0][1] > d:
        return 0

    selected_physics = [physics_cups[0]]
    selected_informatics = [informatics_cups[0]]

    remaining_width = d - physics_cups[0][1] - informatics_cups[0][1]

    i, j = 1, 1
    while i < n and j < m:
        if physics_cups[i][1] <= remaining_width and physics_cups[i][0] >= selected_physics[-1][0]:
            selected_physics.append(physics_cups[i])
            remaining_width -= physics_cups[i][1]
            i += 1
        elif informatics_cups[j][1] <= remaining_width and informatics_cups[j][0] >= selected_informatics[-1][0]:
            selected_informatics.append(informatics_cups[j])
            remaining_width -= informatics_cups[j][1]
            j += 1
        else:
            break

    while i < n and physics_cups[i][0] >= selected_physics[-1][0]:
        if physics_cups[i][1] <= remaining_width:
            selected_physics.append(physics_cups[i])
            remaining_width -= physics_cups[i][1]
            i += 1
        else:
            break

    while j < m and informatics_cups[j][0] >= selected_informatics[-1][0]:
        if informatics_cups[j][1] <= remaining_width:
            selected_informatics.append(informatics_cups[j])
            remaining_width -= informatics_cups[j][1]
            j += 1
        else:
            break

    return sum(cup[0] for cup in selected_physics + selected_informatics)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
d = int(data[2])

physics_cups = []
for i in range(n):
    c_i = int(data[3 + 2 * i])
    w_i = int(data[4 + 2 * i])
    physics_cups.append((c_i, w_i))

informatics_cups = []
for i in range(m):
    c_j = int(data[3 + 2 * n + 2 * i])
    w_j = int(data[4 + 2 * n + 2 * i])
    informatics_cups.append((c_j, w_j))

print(max_significance(n, m, d, physics_cups, informatics_cups))