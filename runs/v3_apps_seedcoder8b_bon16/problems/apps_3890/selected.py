def solve():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    n = int(data[0])
    k = int(data[1])
    
    MOD = 1000000007
    
    def count_valid_plaques(n, k):
        from itertools import permutations
        
        count = 0
        
        for p in permutations(range(1, n + 1)):
            if is_valid_plaque(p, k):
                count += 1
                count %= MOD
        
        return count
    
    def is_valid_plaque(p, k):
        visited = [False] * n
        cycle_detected = False
        
        for start in range(1, k + 1):
            if visited[start - 1]:
                continue
            
            current = start
            while not visited[current - 1]:
                visited[current - 1] = True
                current = p[current - 1]
                if current == 1:
                    cycle_detected = True
                    break
            
            if cycle_detected:
                break
        
        if not cycle_detected:
            return False
        
        for start in range(k + 1, n + 1):
            current = start
            while current != 1:
                current = p[current - 1]
            if current != 1:
                return False
        
        return True
    
    result = count_valid_plaques(n, k)
    print(result)