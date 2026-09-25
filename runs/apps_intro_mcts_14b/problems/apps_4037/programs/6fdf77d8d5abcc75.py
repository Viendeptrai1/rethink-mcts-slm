import sys
from functools import lru_cache

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    r = int(data[1])
    
    projects = []
    index = 2
    for _ in range(n):
        a_i = int(data[index])
        b_i = int(data[index + 1])
        projects.append((a_i, b_i))
        index += 2
    
    @lru_cache(None)
    def dp(current_rating, project_index):
        if project_index == n:
            return 0
        
        max_size = dp(current_rating, project_index + 1)
        
        a_i, b_i = projects[project_index]
        if current_rating >= a_i:
            new_rating = current_rating + b_i
            if new_rating >= 0:
                max_size = max(max_size, 1 + dp(new_rating, project_index + 1))
        
        return max_size
    
    result = dp(r, 0)
    print(result)

if __name__ == "__main__":
    main()