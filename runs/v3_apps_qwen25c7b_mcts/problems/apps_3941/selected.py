def can_unlock_all_doors(n, m, doors, switches):
    # Check if the number of doors is even and all doors start unlocked
    if n % 2 == 0 and sum(doors) == n:
        return "YES"
    else:
        return "NO"

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

doors = list(map(int, data[2:n+2]))
switches = []

index = n + 2
for _ in range(m):
    x = int(data[index])
    rooms = list(map(int, data[index+1:index+x+1]))
    switches.append((x, rooms))
    index += x + 1

# Output the result
print(can_unlock_all_doors(n, m, doors, switches))