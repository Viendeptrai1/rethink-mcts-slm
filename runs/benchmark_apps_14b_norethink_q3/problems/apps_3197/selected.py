import sys

def max_participants(n, k, preferences):
    # Create a list of tuples (participant, preferred)
    participants = [(i + 1, preferences[i]) for i in range(n)]
    
    # Sort participants by their preferred participant
    participants.sort(key=lambda x: x[1])
    
    # Use a set to keep track of selected participants
    selected = set()
    
    for participant, preferred in participants:
        # Check if the preferred participant is already selected or if it's the participant itself
        if preferred in selected or preferred == participant:
            # If we haven't reached the bus capacity, add the participant to the selected set
            if len(selected) < k:
                selected.add(participant)
    
    return len(selected)

# Read input from stdin
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
preferences = list(map(int, data[2:]))

# Calculate and print the result
result = max_participants(n, k, preferences)
print(result)