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
        
        # Since the minimum value on the dice is 2, we need at least x // 2 rolls to get x points.
        # We can always achieve x points by rolling the dice x // 2 times and getting 2 points each time,
        # and then rolling the remaining dice to make up the difference.
        rolls = x // 2
        results.append(rolls)
    
    for result in results:
        print(result)

solve()