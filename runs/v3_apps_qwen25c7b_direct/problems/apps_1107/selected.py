def max_juice_drunk(n, actions):
    # Initialize variables
    juice_count = 0
    previous_actions = []
    
    # Iterate through the actions
    for i, action in enumerate(actions):
        # Check if we have enough previous actions to compare
        if len(previous_actions) >= 3:
            # Compare the last four actions
            if previous_actions[-4:] == [actions[i-4], actions[i-3], actions[i-2], action]:
                juice_count += 1
        
        # Add the current action to the list of previous actions
        previous_actions.append(action)
        
        # Remove the oldest action if the list exceeds length 4
        if len(previous_actions) > 4:
            previous_actions.pop(0)
    
    return juice_count

# Example usage
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    actions = data[1]
    result = max_juice_drunk(n, actions)
    print(result)