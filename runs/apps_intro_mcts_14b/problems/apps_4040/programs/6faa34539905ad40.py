import sys

def can_reach_end(n, m, d, c):
    # Check if we can reach the end by placing platforms optimally
    if sum(c) == n:
        # If the sum of platform lengths equals the river width, we can place them contiguously
        return True, [0] * n
    
    # Try to place platforms in different configurations
    def backtrack(pos, platforms, used):
        if pos == n:
            return True, platforms
        for i in range(m):
            if not used[i]:
                if pos + c[i] <= n:
                    used[i] = True
                    platforms[pos:pos + c[i]] = [i + 1] * c[i]
                    if backtrack(pos + c[i], platforms, used):
                        return True, platforms
                    used[i] = False
        return False, []
    
    platforms = [0] * n
    used = [False] * m
    result, platforms = backtrack(0, platforms, used)
    return result, platforms

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    d = int(data[2])
    c = list(map(int, data[3:3 + m]))
    
    result, platforms = can_reach_end(n, m, d, c)
    
    if result:
        sys.stdout.write("YES\n")
        sys.stdout.write(" ".join(map(str, platforms)) + "\n")
    else:
        sys.stdout.write("NO\n")

if __name__ == "__main__":
    main()