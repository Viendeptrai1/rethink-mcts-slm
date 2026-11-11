import sys

def count_returnable_rooms(t, test_cases):
    results = []
    
    for n, s in test_cases:
        # Create a list to store the state of each room
        room_state = [0] * n
        
        # Traverse the belts to determine the reachability
        current_room = 0
        while True:
            if s[current_room] == '>':
                next_room = (current_room + 1) % n
            elif s[current_room] == '<':
                next_room = (current_room - 1) % n
            else:
                # If the belt is off, we can move in either direction
                next_room = (current_room + 1) % n
            
            # Mark the room as visited
            room_state[current_room] = 1
            
            # If we return to the starting room, break the loop
            if next_room == 0:
                break
            
            current_room = next_room
        
        # Count the number of returnable rooms
        returnable_count = sum(room_state)
        results.append(returnable_count)
    
    return results

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    test_cases = []
    
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