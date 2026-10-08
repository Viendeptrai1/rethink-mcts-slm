import sys

def count_returnable_rooms(t, test_cases):
    results = []
    for n, s in test_cases:
        # Create a list to store the direction of each belt
        directions = [0 if c == '-' else (1 if c == '>' else -1) for c in s]
        
        # Initialize a list to keep track of visited rooms
        visited = [False] * n
        
        # Initialize a list to store the returnable rooms
        returnable_rooms = 0
        
        # Iterate over each room
        for i in range(n):
            if not visited[i]:
                # Start a new cycle
                current = i
                cycle_length = 0
                while not visited[current]:
                    visited[current] = True
                    current = (current + directions[current]) % n
                    cycle_length += 1
                
                # Check if the cycle length is greater than 1
                if cycle_length > 1:
                    returnable_rooms += cycle_length
        
        results.append(returnable_rooms)
    
    return results

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    test_cases = []
    index = 1
    
    for _ in range(t):
        n = int(data[index])
        s = data[index + 1]
        test_cases.append((n, s))
        index += 2
    
    results = count_returnable_rooms(t, test_cases)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()