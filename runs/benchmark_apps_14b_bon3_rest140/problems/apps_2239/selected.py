def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    
    index = 1
    for _ in range(t):
        x = int(data[index])
        index += 1
        
        # Since the minimum value on the dice is 2, the minimum number of rolls needed is x // 2
        # We need to check if we can achieve x with this number of rolls
        min_rolls = x // 2
        while True:
            # Check if we can achieve x with min_rolls
            if min_rolls * 2 <= x <= min_rolls * 7:
                results.append(min_rolls)
                break
            min_rolls += 1
    
    for result in results:
        print(result)

solve()