import sys

def can_transform(s, t):
    if sorted(s) != sorted(t):
        return False
    return True

def transform_string(s, t):
    n = len(s)
    moves = []
    
    s_list = list(s)
    t_list = list(t)
    
    for i in range(n):
        if s_list[i] != t_list[i]:
            for j in range(i + 1, n):
                if s_list[j] == t_list[i]:
                    for k in range(j, i, -1):
                        s_list[k], s_list[k - 1] = s_list[k - 1], s_list[k]
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
    
    moves = transform_string(s, t)
    
    if len(moves) > 10**4:
        print(-1)
        return
    
    print(len(moves))
    if moves:
        print(' '.join(map(str, moves)))

if __name__ == "__main__":
    main()