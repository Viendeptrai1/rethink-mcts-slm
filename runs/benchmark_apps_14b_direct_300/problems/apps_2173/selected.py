import sys
import heapq

def main():
    import sys
    import heapq
    
    def solve(n, a):
        # Create a min-heap from the list a
        heapq.heapify(a)
        
        # Initialize the result list
        result = []
        
        # The smallest possible rating we can give
        current_rating = 0
        
        # Distribute ratings
        for _ in range(n):
            # Get the smallest desired rating
            smallest_desired = heapq.heappop(a)
            
            # Assign the current rating if it's greater than or equal to the desired rating
            if current_rating >= smallest_desired:
                result.append(current_rating)
            else:
                result.append(smallest_desired)
                current_rating = smallest_desired
            
            # Increment the current rating for the next user
            current_rating += 1
        
        return result
    
    # Read input
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().strip().split()))
    
    # Solve the problem
    result = solve(n, a)
    
    # Print the result
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()