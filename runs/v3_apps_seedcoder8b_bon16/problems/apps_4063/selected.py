def count_equal_divisions(N, difficulties):
    difficulties.sort()
    count = 0
    total_problems = N // 2
    
    for i in range(N):
        arc_problems = total_problems
        abc_problems = total_problems
        
        if i > 0:
            arc_problems += i
            abc_problems -= i
        
        if arc_problems == abc_problems:
            count += 1
    
    return count

def main():
    N = int(input())
    difficulties = list(map(int, input().split()))
    result = count_equal_divisions(N, difficulties)
    print(result)

if __name__ == "__main__":
    main()