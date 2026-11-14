import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return
    
    n = int(data[0])
    s = list(data[1])
    
    # Basic necessary conditions
    if n % 2 != 0:
        print(":(")
        return
    
    # Count fixed '(' and ')'
    open_count = 0
    close_count = 0
    for char in s:
        if char == '(':
            open_count += 1
        elif char == ')':
            close_count += 1
    
    # We need exactly n/2 open and n/2 close parentheses in total.
    # The number of '?' is n - open_count - close_count.
    # We need to add (n/2 - open_count) more '(' and (n/2 - close_count) more ')'.
    needed_open = n // 2 - open_count
    needed_close = n // 2 - close_count
    
    if needed_open < 0 or needed_close < 0:
        print(":(")
        return
    
    # First character must be '(' and last must be ')'
    if s[0] == ')':
        print(":(")
        return
    if s[-1] == '(':
        print(":(")
        return
    
    # If first char is '?', it must become '('
    if s[0] == '?':
        s[0] = '('
        needed_open -= 1
    
    # If last char is '?', it must become ')'
    if s[-1] == '?':
        s[-1] = ')'
        needed_close -= 1
    
    # Now we have a string where s[0] is '(' and s[-1] is ')'
    # We need to fill the remaining '?' such that:
    # 1. Total balance is 0 at the end.
    # 2. Balance never drops to 0 for any strict prefix (indices 0 to n-2).
    # 3. Balance never drops below 0.
    
    # Strategy:
    # We must place all remaining 'needed_open' as '(' as early as possible to keep the balance high.
    # Then we place all remaining 'needed_close' as ')' as late as possible.
    # However, we must ensure that after placing all 'needed_open', the balance is high enough
    # so that even if we place all remaining ')' immediately, we don't hit 0 until the very end.
    
    # Let's simulate the process.
    # We iterate through the string.
    # We maintain current balance.
    # We also track how many '(' we still need to place.
    
    # Actually, a simpler constructive approach:
    # 1. Fill the first k '?' with '(' where k = needed_open.
    # 2. Fill the rest of the '?' with ')'.
    # But we must check if this specific assignment works.
    # Is it possible that filling '(' early causes a prefix sum to hit 0? No, because we start with '(' and only add '(', balance increases.
    # The danger is hitting 0 too early. Since we start at 1 (after first char), and we add '(', balance goes up.
    # The only way to hit 0 is if we have too many ')' early.
    # By putting all necessary '(' first, we maximize the balance before starting to decrease.
    # This minimizes the chance of hitting 0 early.
    
    # Let's verify the logic:
    # We have a sequence of characters. Some are fixed, some are '?'.
    # We decide to turn the first 'needed_open' occurrences of '?' into '(', and the rest into ')'.
    # Let's call this the "Greedy Left" strategy.
    # Does this guarantee no strict prefix has balance 0?
    # Suppose there is a strict prefix with balance 0.
    # Since s[0] is '(', balance starts at 1.
    # To reach 0, we must have more ')' than '(' in that prefix.
    # In our strategy, we put as many '(' as possible as early as possible.
    # Any other strategy would put some ')' earlier than some '(', which would lower the balance earlier.
    # Therefore, if the "Greedy Left" strategy fails (hits 0 early), then any other strategy will also fail (hit 0 even earlier or at the same time).
    # So if a solution exists, the "Greedy Left" strategy should find it.
    
    # Wait, there is a catch.
    # What if putting all '(' early makes the balance too high, and then we are forced to put ')' and hit 0?
    # No, the condition is "not a correct parenthesis sequence". A correct one has balance 0 at the end and never negative.
    # We require NO strict prefix to be correct.
    # A strict prefix is correct if its balance is 0 and it never dropped below 0.
    # Since we start at 1 and only go up with '(', the balance is always >= 1 until we start adding ')'.
    # The balance will drop. If it hits 0 before the end, that's a failure.
    # By delaying ')' as much as possible (putting '(' first), we keep the balance high for as long as possible.
    # This maximizes the minimum balance achieved during the descent.
    # Thus, if the "Greedy Left" strategy results in a balance hitting 0 before the end, then no strategy can avoid it.
    
    # So the algorithm is:
    # 1. Validate basic counts and boundary conditions.
    # 2. Identify indices of '?'.
    # 3. Assign '(' to the first 'needed_open' indices.
    # 4. Assign ')' to the remaining indices.
    # 5. Simulate the balance to ensure:
    #    a. Balance never < 0.
    #    b. Balance never == 0 for indices 0 to n-2.
    #    c. Balance == 0 at index n-1.
    
    # Let's implement this.
    
    # Re-calculate needed_open and needed_close after fixing boundaries
    # We already did that above.
    
    # Find indices of '?'
    q_indices = [i for i, char in enumerate(s) if char == '?']
    
    # Assign '(' to the first needed_open indices
    for i in range(needed_open):
        s[q_indices[i]] = '('
    
    # Assign ')' to the rest
    for i in range(needed_open, len(q_indices)):
        s[q_indices[i]] = ')'
    
    # Now verify
    balance = 0
    possible = True
    
    for i in range(n):
        if s[i] == '(':
            balance += 1
        else:
            balance -= 1
        
        if balance < 0:
            possible = False
            break
        
        # Check strict prefix condition
        # Strict prefix means i < n-1
        if i < n - 1 and balance == 0:
            possible = False
            break
    
    if possible and balance == 0:
        print("".join(s))
    else:
        print(":(")

if __name__ == '__main__':
    solve()