import sys
import heapq

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.read().split()))
    
    data = read_ints()
    n = data[0]
    a = data[1:]
    
    # Create a min-heap with the desired ratings
    heap = []
    for i in range(n):
        heapq.heappush(heap, (a[i], i))
    
    # Array to store the result
    b = [0] * n
    
    # Set to keep track of assigned ratings
    assigned_ratings = set()
    
    # Assign ratings
    while heap:
        desired_rating, index = heapq.heappop(heap)
        # Find the smallest rating >= desired_rating that hasn't been assigned
        rating = desired_rating
        while rating in assigned_ratings:
            rating += 1
        b[index] = rating
        assigned_ratings.add(rating)
    
    # Print the result
    print(' '.join(map(str, b)))

if __name__ == "__main__":
    main()