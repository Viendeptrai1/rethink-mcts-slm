def count_returnable_rooms(t):
    results = []
    for _ in range(t):
        n = int(input())
        s = input().strip()
        
        # Initialize variables
        visited = [False] * n
        stack = []
        
        # Helper function to check if a room is returnable
        def is_returnable(room):
            if visited[room]:
                return False
            visited[room] = True
            stack.append(room)
            
            while stack:
                current = stack.pop()
                next_room = (current + 1) % n
                prev_room = (current - 1 + n) % n
                
                if s[current] == '>':
                    if not visited[next_room]:
                        stack.append(next_room)
                elif s[current] == '<':
                    if not visited[prev_room]:
                        stack.append(prev_room)
                else:
                    if not visited[next_room]:
                        stack.append(next_room)
                    if not visited[prev_room]:
                        stack.append(prev_room)
            
            return True
        
        # Count returnable rooms
        returnable_count = 0
        for i in range(n):
            if is_returnable(i):
                returnable_count += 1
        
        results.append(returnable_count)
    
    return results

# Example usage
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    t = int(data[0])
    result = count_returnable_rooms(t)
    for res in result:
        print(res)