import sys

def max_contest_problems(n, difficulties):
    max_problems = 0
    end = 0
    
    for start in range(n):
        while end < n and difficulties[end] <= difficulties[start] * 2:
            end += 1
        max_problems = max(max_problems, end - start)
    
    return max_problems

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    difficulties = list(map(int, data[1:]))
    
    result = max_contest_problems(n, difficulties)
    print(result)

if __name__ == "__main__":
    main()