def min_problems_to_solve(D, G, problems):
    # Sort problems by their perfect bonus per problem solved in descending order
    problems.sort(key=lambda x: x[1] / x[0], reverse=True)
    
    total_problems = 0
    current_score = 0
    
    for p, c in problems:
        if current_score >= G:
            break
        
        # Solve all problems of this score if it helps to reach or exceed G
        if current_score + p * 100 + c >= G:
            total_problems += p
            current_score += p * 100 + c
        else:
            # Otherwise, solve just enough problems to reach or exceed G
            needed_score = G - current_score
            problems_to_solve = (needed_score - 1) // 100 + 1
            total_problems += problems_to_solve
            current_score += problems_to_solve * 100
    
    return total_problems

# Read input
import sys
input = sys.stdin.read
data = input().split()

D = int(data[0])
G = int(data[1])
problems = []

index = 2
for _ in range(D):
    p = int(data[index])
    c = int(data[index + 1])
    problems.append((p, c))
    index += 2

# Calculate and print the result
result = min_problems_to_solve(D, G, problems)
print(result)