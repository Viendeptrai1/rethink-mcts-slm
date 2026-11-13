def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    p = int(data[2])
    x = int(data[3])
    y = int(data[4])
    
    a = list(map(int, data[5:5+k]))
    
    # Calculate the current sum and the number of marks needed
    current_sum = sum(a)
    remaining_tests = n - k
    
    # Calculate the maximum possible sum we can achieve with remaining tests
    max_possible_sum = current_sum + remaining_tests * p
    
    # Check if the current sum exceeds the maximum allowed sum
    if current_sum > x:
        print("-1")
        return
    
    # Check if the maximum possible sum exceeds the allowed sum
    if max_possible_sum > x:
        print("-1")
        return
    
    # Sort the current marks to help with median calculation
    a.sort()
    
    # Calculate the median position
    median_position = (n + 1) // 2
    
    # Try to find a valid set of marks for the remaining tests
    for i in range(remaining_tests):
        # Try to place the minimum possible mark in the current position
        for mark in range(1, p + 1):
            # Simulate adding this mark
            new_sum = current_sum + mark
            new_a = a[:]
            new_a.append(mark)
            new_a.sort()
            
            # Check if the new sum is within the allowed range
            if new_sum <= x:
                # Check if the new median is at least y
                if new_a[median_position - 1] >= y:
                    # If both conditions are satisfied, print the mark
                    print(mark, end=" ")
                    current_sum = new_sum
                    a = new_a
                    break
        else:
            # If no valid mark was found, print -1 and return
            print("-1")
            return
    
    # If we managed to place marks for all remaining tests, print a new line
    print()