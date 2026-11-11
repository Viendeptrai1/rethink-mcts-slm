import sys

def determine_winner(s):
    n = len(s)
    winners = []
    
    for k in range(n):
        l = r = k
        turn = 'Ann'  # Ann starts first
        
        while True:
            found = False
            for l_prime in range(l, -1, -1):
                for r_prime in range(r, n):
                    if s[l_prime:r_prime+1] < s[l:r+1]:
                        l, r = l_prime, r_prime
                        found = True
                        break
                if found:
                    break
            
            if not found:
                winners.append(turn)
                break
            
            turn = 'Mike' if turn == 'Ann' else 'Ann'
    
    return winners

def main():
    import sys
    s = sys.stdin.read().strip()
    winners = determine_winner(s)
    for winner in winners:
        print(winner)

if __name__ == "__main__":
    main()