def can_solve_problems(n, k):
    if n < k or n > 2 * k - 1:
        return "NO"
    
    def backtrack(day, current_sum, last_problem):
        if day == k:
            return current_sum == n
        
        max_problems = min(2 * last_problem, n - current_sum)
        for problems in range(last_problem + 1, max_problems + 1):
            if backtrack(day + 1, current_sum + problems, problems):
                return True
        return False
    
    if backtrack(0, 0, 0):
        return "YES"
    else:
        return "NO"

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

result = can_solve_problems(n, k)
print(result)

if result == "YES":
    # Construct the sequence if possible
    def construct_sequence(n, k):
        sequence = []
        current_sum = 0
        last_problem = 0
        for _ in range(k):
            max_problems = min(2 * last_problem, n - current_sum)
            for problems in range(last_problem + 1, max_problems + 1):
                if current_sum + problems <= n:
                    sequence.append(problems)
                    current_sum += problems
                    last_problem = problems
                    break
        return sequence
    
    sequence = construct_sequence(n, k)
    print(" ".join(map(str, sequence)))
else:
    print("")