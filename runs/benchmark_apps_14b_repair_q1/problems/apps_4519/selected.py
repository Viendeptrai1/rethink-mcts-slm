import sys

def solve():
    import sys
    import heapq
    
    def min_string_after_k_swaps(n, k, s):
        # Convert string to list for easier manipulation
        s = list(s)
        # Create a min-heap to keep track of the positions of '0's
        zeros = []
        for i in range(n):
            if s[i] == '0':
                heapq.heappush(zeros, i)
        
        # Perform up to k swaps
        for _ in range(k):
            if not zeros:
                break
            # Get the position of the nearest '0'
            zero_pos = heapq.heappop(zeros)
            # Swap the '0' with its right neighbor
            if zero_pos < n - 1:
                s[zero_pos], s[zero_pos + 1] = s[zero_pos + 1], s[zero_pos]
                # If the swapped '0' is still in the string, push its new position back into the heap
                if s[zero_pos + 1] == '0':
                    heapq.heappush(zeros, zero_pos + 1)
        
        return ''.join(s)
    
    q = int(sys.stdin.readline())
    results = []
    for _ in range(q):
        n, k = map(int, sys.stdin.readline().split())
        s = sys.stdin.readline().strip()
        result = min_string_after_k_swaps(n, k, s)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    solve()