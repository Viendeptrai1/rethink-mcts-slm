def determine_winner(s):
    n = len(s)
    results = []

    for k in range(n):
        # Initialize the game state
        l, r = k, k
        moves_ann = 0
        moves_mike = 0

        # Determine the winner for each k
        while True:
            # Find the smallest lexicographical substring
            found_move = False
            for l_prime in range(l, -1, -1):
                for r_prime in range(r, n):
                    if s[l_prime:r_prime + 1] < s[l:r + 1]:
                        l, r = l_prime, r_prime
                        found_move = True
                        break
                if found_move:
                    break

            if not found_move:
                # No move possible, current player loses
                break

            # Alternate turns
            if moves_ann % 2 == 0:
                moves_ann += 1
            else:
                moves_mike += 1

        # Determine the winner based on the number of moves
        if moves_ann > moves_mike:
            results.append("Ann")
        else:
            results.append("Mike")

    return results

# Read input
import sys
input = sys.stdin.read
s = input().strip()

# Determine and print the winner for each k
winners = determine_winner(s)
for winner in winners:
    print(winner)