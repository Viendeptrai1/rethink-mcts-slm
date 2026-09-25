import sys

def can_reach_other_side(n, m, d, c):
    if sum(c) > n:
        return "NO"
    
    # Initialize the river with 0s
    river = [0] * (n + 2)
    
    # Place the platforms in the river
    current_position = 1
    for i in range(m):
        while current_position + c[i] - 1 > n:
            current_position += 1
        for j in range(c[i]):
            river[current_position + j] = i + 1
        current_position += c[i]
    
    # Check if we can reach from 0 to n+1
    reachable = [False] * (n + 2)
    reachable[0] = True
    
    for i in range(n + 2):
        if reachable[i]:
            for j in range(1, d + 1):
                if i + j <= n + 1 and river[i + j] != 0:
                    reachable[i + j] = True
    
    if reachable[n + 1]:
        return "YES", river[1:n + 1]
    else:
        return "NO"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    d = int(data[2])
    c = list(map(int, data[3:3 + m]))
    
    result = can_reach_other_side(n, m, d, c)
    if result == "NO":
        print("NO")
    else:
        print("YES")
        print(" ".join(map(str, result[1])))

if __name__ == "__main__":
    main()