import sys

def find_shortest_cycle(n, files, dependencies):
    def dfs(node, parent, visited, rec_stack, path):
        visited[node] = True
        rec_stack[node] = True
        path.append(node)
        
        for neighbor in dependencies[node]:
            if not visited[neighbor]:
                if dfs(neighbor, node, visited, rec_stack, path):
                    return True
            elif rec_stack[neighbor]:
                # Cycle detected
                cycle_start_index = path.index(neighbor)
                cycle = path[cycle_start_index:]
                return cycle
        
        rec_stack[node] = False
        path.pop()
        return False

    visited = {file: False for file in files}
    rec_stack = {file: False for file in files}
    
    for file in files:
        if not visited[file]:
            path = []
            cycle = dfs(file, None, visited, rec_stack, path)
            if cycle:
                return cycle
    
    return []

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    files = data[1].split()
    dependencies = {file: [] for file in files}
    
    index = 2
    for i in range(n):
        file_name, k = data[index].split()
        index += 1
        for _ in range(int(k)):
            line = data[index].split(', ')
            dependencies[file_name].extend(line[1:])
            index += 1
    
    cycle = find_shortest_cycle(n, files, dependencies)
    
    if cycle:
        print(' '.join(cycle))
    else:
        print("SHIP IT")

if __name__ == "__main__":
    main()