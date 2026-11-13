def determine_winner(s):
    n = len(s)
    results = [''] * n
    
    for k in range(n):
        # Check substrings starting from each position l = r = k
        l, r = k, k
        current_player = 'Ann'  # Ann starts first
        
        while l > 0 or r < n - 1:
            # Try to find a move for current_player
            found_move = False
            
            # Check moves to the left
            for new_l in range(l, -1, -1):
                if s[new_l:r+1] < s[l:r+1]:
                    l = new_l
                    found_move = True
                    break
            
            if not found_move:
                # Check moves to the right
                for new_r in range(r + 1, n):
                    if s[l:new_r+1] < s[l:r+1]:
                        r = new_r
                        found_move = True
                        break
            
            if found_move:
                current_player = 'Mike' if current_player == 'Ann' else 'Ann'
            else:
                # No valid move found, current player loses
                break
        
        # Determine the winner
        results[k] = 'Mike' if current_player == 'Ann' else 'Ann'
    
    return results

# Read input
s = input().strip()

# Get results
results = determine_winner(s)

# Print results
for result in results:
    print(result)