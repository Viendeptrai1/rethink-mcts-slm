import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    s = input_data[1]
    
    colors = ['R', 'G', 'B']
    perms = []
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            for k in range(3):
                if k == i or k == j:
                    continue
                perms.append((colors[i], colors[j], colors[k]))
    
    min_changes = n + 1
    best_pattern = None
    
    for p in perms:
        # Construct the candidate string based on pattern p
        # t[i] = p[i % 3]
        candidate = []
        changes = 0
        for idx in range(n):
            char_needed = p[idx % 3]
            if char_needed != s[idx]:
                changes += 1
            candidate.append(char_needed)
        
        if changes < min_changes:
            min_changes = changes
            best_pattern = candidate
    
    print(min_changes)
    print("".join(best_pattern))

if __name__ == "__main__":
    solve()