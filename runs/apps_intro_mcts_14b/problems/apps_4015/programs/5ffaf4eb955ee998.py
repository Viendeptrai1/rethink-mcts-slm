import sys

def min_moves(n, m):
    if n == m:
        return 0
    if n > m:
        return -1
    
    queue = [(n, 0)]
    visited = set()
    visited.add(n)
    
    while queue:
        current, moves = queue.pop(0)
        
        if current * 2 == m or current * 3 == m:
            return moves + 1
        
        if current * 2 <= m and current * 2 not in visited:
            visited.add(current * 2)
            queue.append((current * 2, moves + 1))
        
        if current * 3 <= m and current * 3 not in visited:
            visited.add(current * 3)
            queue.append((current * 3, moves + 1))
    
    return -1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    m = int(data[1])
    result = min_moves(n, m)
    print(result)

if __name__ == "__main__":
    main()