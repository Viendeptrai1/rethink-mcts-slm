def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    q = int(data[1])
    
    a = list(map(int, data[2:n+2]))
    b = list(map(int, data[n+2:n+2+q]))
    
    # Precompute the set of all possible sums using the given coins
    possible_sums = set()
    possible_sums.add(0)
    
    for coin in a:
        new_sums = set()
        for s in possible_sums:
            new_sums.add(s + coin)
        possible_sums.update(new_sums)
    
    # Answer each query
    results = []
    for query in b:
        if query in possible_sums:
            # Find the minimum number of coins needed
            min_coins = float('inf')
            for coin in a:
                if query % coin == 0:
                    count = 0
                    temp_query = query
                    while temp_query > 0:
                        if temp_query % coin == 0:
                            temp_query -= coin
                            count += 1
                        else:
                            break
                    min_coins = min(min_coins, count)
            results.append(min_coins)
        else:
            results.append(-1)
    
    # Print the results
    for result in results:
        print(result)