import sys

def solve():
    D, G = map(int, input().split())
    problems = [list(map(int, input().split())) for _ in range(D)]
    
    def total_score(solved):
        base = sum(i * 100 for i, count in enumerate(solved, 1) for _ in range(count))
        perfect = sum(c for (p, c), count in zip(problems, solved) if count == p)
        return base + perfect
    
    def solve_dfs(index, solved):
        if total_score(solved) >= G:
            return sum(solved)
        
        if index == D:
            return float('inf')
        
        min_problems = float('inf')
        for i in range(problems[index][0] + 1):
            solved[index] = i
            min_problems = min(min_problems, solve_dfs(index + 1, solved))
            solved[index] = 0
        
        return min_problems
    
    print(solve_dfs(0, [0] * D))

if __name__ == "__main__":
    solve()