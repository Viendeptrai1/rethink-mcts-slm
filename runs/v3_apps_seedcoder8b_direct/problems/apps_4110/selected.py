def min_problems_to_achieve_score():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    D = int(data[0])
    G = int(data[1])
    
    problems = []
    index = 2
    for _ in range(D):
        p_i = int(data[index])
        c_i = int(data[index + 1])
        problems.append((p_i, c_i))
        index += 2
    
    def calculate_score(solved):
        base_score = 0
        perfect_bonus = 0
        for i, (p_i, c_i) in enumerate(problems):
            if solved[i] < p_i:
                base_score += solved[i] * (100 * (i + 1))
                break
            else:
                base_score += p_i * (100 * (i + 1))
                perfect_bonus += c_i
        return base_score + perfect_bonus
    
    from itertools import product
    
    min_problems = float('inf')
    
    for solved in product(*(range(p_i + 1) for p_i, _ in problems)):
        if calculate_score(solved) >= G:
            min_problems = min(min_problems, sum(solved))
    
    print(min_problems)