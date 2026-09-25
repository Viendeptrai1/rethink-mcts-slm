import sys
from collections import deque

def max_students_in_teams(n, k, skills):
    skills.sort()
    max_students = 0
    queue = deque()
    
    for skill in skills:
        while queue and skill - queue[0] > 5:
            queue.popleft()
        if len(queue) < k:
            queue.append(skill)
            max_students += 1
    
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