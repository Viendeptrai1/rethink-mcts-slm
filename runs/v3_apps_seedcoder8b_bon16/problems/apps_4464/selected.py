def solve(A, B, C):
    if C == 0:
        return "YES"
    
    if A == 1:
        return "YES"
    
    if C % A == 0:
        return "YES"
    
    for i in range(1, B):
        if (i * A) % B == C:
            return "YES"
    
    return "NO"

if __name__ == "__main__":
    A, B, C = map(int, input().split())
    print(solve(A, B, C))