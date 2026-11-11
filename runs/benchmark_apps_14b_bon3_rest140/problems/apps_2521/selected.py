import sys
import heapq

def max_score(N, a):
    # Split the array into three parts
    part1 = a[:N]
    part2 = a[N:2*N]
    part3 = a[2*N:]
    
    # Max-heap for the first part and min-heap for the third part
    max_heap = [-x for x in part1]
    heapq.heapify(max_heap)
    
    min_heap = part3
    heapq.heapify(min_heap)
    
    # Calculate the initial score with all elements from part1 and part2
    current_score = sum(part1) - sum(part2)
    
    # Try to improve the score by replacing elements from part2 with elements from part3
    for i in range(N):
        if part2[i] < -max_heap[0]:
            # Replace part2[i] with the largest element from part1
            current_score += (-max_heap[0] - part2[i])
            heapq.heappop(max_heap)
            heapq.heappush(max_heap, -part2[i])
        
        if part2[i] > min_heap[0]:
            # Replace part2[i] with the smallest element from part3
            current_score += (min_heap[0] - part2[i])
            heapq.heappop(min_heap)
            heapq.heappush(min_heap, part2[i])
    
    return current_score

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    a = list(map(int, data[1:]))
    
    result = max_score(N, a)
    print(result)

if __name__ == "__main__":
    main()