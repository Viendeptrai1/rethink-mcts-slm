def determine_winner(s):
    n = len(s)
    results = []

    for k in range(n):
        # Initialize the current substring
        l, r = k, k
        current_substring = s[k:k+1]
        move_count = 0

        while True:
            move_made = False
            # Check all possible substrings that can be formed
            for l_prime in range(l, -1, -1):
                for r_prime in range(r, n):
                    candidate_substring = s[l_prime:r_prime+1]
                    if candidate_substring < current_substring:
                        # Update the current substring and move
                        l, r = l_prime, r_prime
                        current_substring = candidate_substring
                        move_made = True
                        break
                if move_made:
                    break

            if not move_made:
                # If no move can be made, the current player loses
                break

            move_count += 1

        # Determine the winner based on the number of moves
        if move_count % 2 == 0:
            results.append("Ann")
        else:
            results.append("Mike")

    return results

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    s = input().strip()
    results = determine_winner(s)
    for result in results:
        print(result)