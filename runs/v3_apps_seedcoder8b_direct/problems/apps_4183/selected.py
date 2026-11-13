def lcm(a, b):
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x
    return a * b // gcd(a, b)

def find_time_for_all_clocks_upward(N, T):
    if N == 0:
        return 0
    current_lcm = T[0]
    for i in range(1, N):
        current_lcm = lcm(current_lcm, T[i])
    return current_lcm

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    T = [int(data[i]) for i in range(1, N + 1)]
    
    result = find_time_for_all_clocks_upward(N, T)
    print(result)

if __name__ == "__main__":
    main()