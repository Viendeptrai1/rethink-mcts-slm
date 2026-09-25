import sys
from functools import lru_cache

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    r = int(data[1])
    
    projects = []
    for i in range(n):
        a_i = int(data[2 + 2 * i])
        b_i = int(data[3 + 2 * i])
        projects.append((a_i, b_i))
    
    @lru_cache(None)
    def max_subset_size(index, current_rating):
        if index == n:
            return 0
        
        a_i, b_i = projects[index]
        
        # Option 1: Skip the current project
        option1 = max_subset_size(index + 1, current_rating)
        
        # Option 2: Take the current project if possible
        option2 = 0
        if current_rating >= a_i:
            new_rating = current_rating + b_i
            if new_rating >= 0:
                option2 = 1 + max_subset_size(index + 1, new_rating)
        
        return max(option1, option2)
    
    result = max_subset_size(0, r)
    print(result)

if __name__ == "__main__":
    main()