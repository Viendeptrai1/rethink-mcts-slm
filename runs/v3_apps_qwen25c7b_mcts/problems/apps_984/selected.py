from sys import stdin, stdout

def find_failures(n, nodes):
    def dfs(node, target):
        if node == -1:
            return True
        if nodes[node][0] == target:
            return False
        if target < nodes[node][0]:
            return dfs(nodes[node][1], target)
        else:
            return dfs(nodes[node][2], target)

    failure_count = 0
    for i in range(n):
        failure_count += dfs(i, nodes[i][0])

    return failure_count

# Read input
n = int(stdin.readline().strip())
nodes = [tuple(map(int, stdin.readline().strip().split())) for _ in range(n)]

# Output the result
stdout.write(str(find_failures(n, nodes)) + '\n')