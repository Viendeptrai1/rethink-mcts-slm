import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    t = data[2]
    
    # Check if it's possible to transform s into t
    if sorted(s) != sorted(t):
        print(-1)
        return
    
    # Initialize the list of moves
    moves = []
    
    # Convert strings to lists for easier manipulation
    s_list = list(s)
    
    # Try to transform s into t
    for i in range(n):
        if s_list[i] != t[i]:
            # Find the position of the character t[i] in s_list
            for j in range(i + 1, n):
                if s_list[j] == t[i]:
                    # Swap adjacent characters to bring t[i] to position i
                    for k in range(j, i, -1):
                        s_list[k], s_list[k - 1] = s_list[k - 1], s_list[k]
                        moves.append(k)
                    break
    
    # Output the number of moves and the moves themselves
    print(len(moves))
    if moves:
        print(' '.join(map(str, moves)))

if __name__ == "__main__":
    main()