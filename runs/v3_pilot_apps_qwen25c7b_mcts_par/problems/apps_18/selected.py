import heapq

def min_lexicographical_string(s):
    n = len(s)
    heap = []
    t = []
    u = []

    # Push all characters of s into the heap
    for char in s:
        heapq.heappush(heap, char)

    while heap or t:
        if heap:
            # Move the smallest character from heap to t
            t.append(heapq.heappop(heap))
        
        if t:
            # Move the last character from t to u
            u.append(t.pop())

    return ''.join(u)

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    s = data[0]
    result = min_lexicographical_string(s)
    print(result)