import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    D = int(data[0])
    G = int(data[1])
    
    problems = []
    index = 2
    for _ in range(D):
        p = int(data[index])
        c = int(data[index + 1])
        index += 2
        problems.append((p, c))
    
    min_problems = float('inf')
    
    for i in range(1 << D):
        base_score = 0
        perfect_bonus = 0
        num_problems = 0
        
        for j in range(D):
            if i & (1 << j):
                num_problems += problems[j][0]
                base_score += problems[j][0] * 100
                perfect_bonus += problems[j][1]
        
        if base_score + perfect_bonus >= G:
            min_problems = min(min_problems, num_problems)
    
    print(min_problems)

if __name__ == "__main__":
    main()