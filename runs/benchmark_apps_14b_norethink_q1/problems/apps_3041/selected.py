import sys

def min_coupons(N, trips):
    INF = float('inf')
    dp = [INF] * 11
    dp[0] = 0
    
    for Z, T in trips:
        new_dp = [INF] * 11
        for i in range(11):
            if dp[i] != INF:
                cost = 2 + abs(i - Z)
                new_dp[Z] = min(new_dp[Z], dp[i] + cost)
        dp = new_dp
    
    return min(dp)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    trips = []
    index = 1
    for _ in range(N):
        Z = int(data[index])
        T = int(data[index + 1])
        trips.append((Z, T))
        index += 2
    
    result = min_coupons(N, trips)
    print(result)

if __name__ == "__main__":
    main()