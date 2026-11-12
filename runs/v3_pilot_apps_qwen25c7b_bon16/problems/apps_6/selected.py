import sys

def min_blow_to_defeat_zmei(gorynich_heads, blows):
    max_decrease = max(blows, key=lambda x: x[0])[0]
    if gorynich_heads <= max_decrease:
        return 1
    
    max_increase = max(blows, key=lambda x: x[1])[1]
    if gorynich_heads > max_decrease + max_increase:
        return -1
    
    dp = [float('inf')] * (gorynich_heads + 1)
    dp[0] = 0
    
    for d, h in blows:
        for i in range(gorynich_heads, d - 1, -1):
            dp[i] = min(dp[i], dp[i - d] + 1)
            if i >= d + h:
                dp[i] = min(dp[i], dp[i - d - h] + 1)
    
    return dp[gorynich_heads]

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    
    results = []
    for _ in range(t):
        n = int(data[index])
        index += 1
        x = int(data[index])
        index += 1
        
        blows = []
        for _ in range(n):
            d = int(data[index])
            index += 1
            h = int(data[index])
            index += 1
            blows.append((d, h))
        
        result = min_blow_to_defeat_zmei(x, blows)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()