import sys
from collections import deque

def max_students_in_teams(n, k, skills):
    skills.sort()
    max_students = 0
    queue = deque(skills)
    
    while k > 0 and queue:
        team_size = 1
        current_skill = queue.popleft()
        
        while queue and queue[0] - current_skill <= 5:
            queue.popleft()
            team_size += 1
        
        max_students += team_size
        k -= 1
    
    return max_students

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    skills = list(map(int, data[2:]))
    
    result = max_students_in_teams(n, k, skills)
    print(result)

if __name__ == "__main__":
    main()