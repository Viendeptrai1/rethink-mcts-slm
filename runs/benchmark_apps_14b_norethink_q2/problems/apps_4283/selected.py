import sys

def max_balanced_team(n, skills):
    skills.sort()
    left = 0
    max_length = 0
    
    for right in range(n):
        while skills[right] - skills[left] > 5:
            left += 1
        max_length = max(max_length, right - left + 1)
    
    return max_length

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    skills = list(map(int, data[1:]))
    
    result = max_balanced_team(n, skills)
    print(result)

if __name__ == "__main__":
    main()