import sys

def solve():
    data = sys.stdin.read().strip()
    if not data:
        return
    scores = list(map(int, data.split()))
    total = sum(scores)
    
    if total % 2 != 0:
        print("NO")
        return
    
    target = total // 2
    
    # We need to find if there exists a subset of 3 elements that sums to target
    # Since there are only 6 elements, we can try all combinations of 3
    n = 6
    found = False
    
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if scores[i] + scores[j] + scores[k] == target:
                    found = True
                    break
            if found:
                break
        if found:
            break
    
    if found:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()