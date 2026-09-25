import sys

def can_transform(s, t):
    if sorted(s) != sorted(t):
        return False
    return True

def transform(s, t):
    moves = []
    s = list(s)
    t = list(t)
    
    for i in range(len(s)):
        if s[i] != t[i]:
            for j in range(i + 1, len(s)):
                if s[j] == t[i]:
                    for k in range(j, i, -1):
                        s[k], s[k - 1] = s[k - 1], s[k]
                        moves.append(k)
                    break
    return moves

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    t = data[2]
    
    if not can_transform(s, t):
        print(-1)
        return
    
    moves = transform(s, t)
    
    if len(moves) > 10**4:
        print(-1)
        return
    
    print(len(moves))
    if moves:
        print(" ".join(map(str, moves)))

if __name__ == "__main__":
    main()