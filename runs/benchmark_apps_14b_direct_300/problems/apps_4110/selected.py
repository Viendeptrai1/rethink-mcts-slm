import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    D = int(data[0])
    G = int(data[1])
    
    problems = []
    bonuses = []
    
    index = 2
    for i in range(D):
        p_i = int(data[index])
        c_i = int(data[index + 1])
        problems.append(p_i)
        bonuses.append(c_i)
        index += 2
    
    min_problems = float('inf')
    
    for mask in range(1 << D):
        total_score = 0
        problems_solved = 0
        
        for i in range(D):
            if mask & (1 << i):
                total_score += problems[i] * 100 * (i + 1) + bonuses[i]
                problems_solved += problems[i]
            else:
                max_possible_score = problems[i] * 100 * (i + 1)
                if total_score + max_possible_score >= G:
                    additional_problems = (G - total_score - 1) // (100 * (i + 1)) + 1
                    problems_solved += additional_problems
                    break
        
        if total_score >= G:
            min_problems = min(min_problems, problems_solved)
    
    print(min_problems)

if __name__ == "__main__":
    main()