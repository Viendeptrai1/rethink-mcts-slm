def count_returnable_rooms(t, test_cases):
    results = []
    for n, s in test_cases:
        # Initialize the degree of change for each room.
        # If s[i] == '>', contribute +1 to room i and -1 to room (i+1) % n.
        # If s[i] == '<', contribute -1 to room i and +1 to room (i+1) % n.
        # If s[i] == '-', contribute 0 to both.
        degree = [0] * n
        
        for i in range(n):
            if s[i] == '>':
                degree[i] += 1
                degree[(i + 1) % n] -= 1
            elif s[i] == '<':
                degree[i] -= 1
                degree[(i + 1) % n] += 1
        
        # To determine if a room is returnable, we need to find a contiguous
        # subarray in the degree array which sums to zero.
        
        # Prefix sum array to find zero sum subarray
        prefix_sum = [0] * (2 * n + 1)
        for i in range(1, 2 * n + 1):
            prefix_sum[i] = prefix_sum[i - 1] + degree[(i - 1) % n]
        
        # Use a set to track seen prefix sums
        seen = set()
        returnable_count = 0
        
        for i in range(2 * n + 1):
            if prefix_sum[i] in seen:
                returnable_count += 1
            seen.add(prefix_sum[i])
        
        results.append(returnable_count)
    
    return results

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    test_cases = []
    
    for _ in range(t):
        n = int(data[index])
        index += 1
        s = data[index]
        index += 1
        test_cases.append((n, s))
    
    results = count_returnable_rooms(t, test_cases)
    for result in results:
        print(result)