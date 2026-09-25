import sys

def max_problems_solved(n, k, problems):
    left = 0
    right = n - 1
    solved = 0
    
    while left <= right:
        if problems[left] <= k and problems[right] <= k:
            if problems[left] <= problems[right]:
                solved += 1
                left += 1
            else:
                solved += 1
                right -= 1
        elif problems[left] <= k:
            solved += 1
            left += 1
        elif problems[right] <= k:
            solved += 1
            right -= 1
        else:
            break
    
    return solved

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    problems = list(map(int, data[2:]))
    
    result = max_problems_solved(n, k, problems)
    print(result)

if __name__ == "__main__":
    main()