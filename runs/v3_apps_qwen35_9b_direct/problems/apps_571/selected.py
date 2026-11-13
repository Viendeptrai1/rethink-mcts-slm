import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return
    
    n = int(data[0])
    s = list(data[1])
    
    if n % 2 != 0:
        print(":(")
        return
    
    # We need to fill '?' such that:
    # 1. The final string is a correct parenthesis sequence.
    # 2. No strict prefix is a correct parenthesis sequence.
    
    # Conditions for a correct parenthesis sequence:
    # - Total length is even.
    # - Balance (count('(') - count(')')) is 0 at the end.
    # - Balance is never negative at any point.
    
    # Condition for "no strict prefix is correct":
    # - A strict prefix is correct if its balance is 0 and it never dropped below 0.
    # - Since the full string must be correct (balance 0 at end), if any strict prefix has balance 0, it is a correct prefix.
    # - Therefore, we require that the balance is strictly greater than 0 for all indices 0 to n-2.
    # - At index n-1 (the last character), the balance must become 0.
    
    # Strategy:
    # We know the first character must be '(' and the last must be ')' for the whole string to be correct and non-empty.
    # If s[0] is '?' -> set to '('.
    # If s[n-1] is '?' -> set to ')'.
    # For the intermediate characters s[1] to s[n-2], we need to assign them such that the balance stays > 0 until the very end.
    # To maximize our chances of satisfying the "balance > 0" constraint while keeping the total balance 0, 
    # a common greedy approach for this specific problem (Codeforces 1140C / similar) is:
    # - Set the first half of the '?' (excluding first and last) to '('.
    # - Set the second half of the '?' (excluding first and last) to ')'.
    # However, we must be careful with the counts.
    
    # Let's refine the greedy strategy:
    # We need balance > 0 for i in 0..n-2.
    # balance[0] = 1 (since s[0] must be '(').
    # balance[n-1] = 0.
    # We want to ensure balance[i] >= 1 for all 0 <= i <= n-2.
    
    # Let's count existing '(' and ')' and '?'.
    # We will determine the number of '(' and ')' needed.
    # Let open_needed be the number of '(' we need to add.
    # Let close_needed be the number of ')' we need to add.
    # Total length n.
    # Current balance from fixed chars: cur_bal.
    # Number of fixed '(': cnt_open.
    # Number of fixed ')': cnt_close.
    # cur_bal = cnt_open - cnt_close.
    # Number of '?': cnt_q = n - cnt_open - cnt_close.
    # We need final balance 0 => (cnt_open + open_needed) - (cnt_close + close_needed) = 0
    # => open_needed - close_needed = cnt_close - cnt_open = -cur_bal
    # Also open_needed + close_needed = cnt_q.
    # Solving:
    # 2 * open_needed = cnt_q - cur_bal
    # 2 * close_needed = cnt_q + cur_bal
    
    # If (cnt_q - cur_bal) is odd or negative, impossible.
    
    cnt_open = s.count('(')
    cnt_close = s.count(')')
    cnt_q = n - cnt_open - cnt_close
    
    cur_bal = cnt_open - cnt_close
    
    needed_open = (cnt_q - cur_bal) // 2
    needed_close = (cnt_q + cur_bal) // 2
    
    if (cnt_q - cur_bal) % 2 != 0 or needed_open < 0 or needed_close < 0:
        print(":(")
        return
    
    # Now we have the counts. We need to place them to satisfy the prefix condition.
    # The condition is: balance > 0 for all prefixes except the full string.
    # This implies:
    # 1. s[0] must be '('.
    # 2. s[n-1] must be ')'.
    # 3. We should put as many '(' as possible early on to keep balance high, and ')' later.
    # Specifically, we can fill the first 'needed_open' question marks (scanning from left) with '(',
    # and the remaining 'needed_close' question marks with ')'.
    # BUT we must ensure s[0] is '(' and s[n-1] is ')'.
    
    # Let's construct the string carefully.
    # We will iterate through the string.
    # We maintain a counter for how many '(' and ')' we still need to place.
    # We also maintain the current balance.
    
    # Special handling for first and last characters if they are '?'.
    # Actually, the greedy strategy "fill first available '?' with '(' until we run out, then fill rest with ')'" 
    # works IF we ensure the first char is '(' and last is ')'.
    # Since we know s[0] MUST be '(' and s[n-1] MUST be ')', let's force that first.
    
    # Check constraints on first and last
    if s[0] == ')':
        print(":(")
        return
    if s[n-1] == '(':
        print(":(")
        return
    
    # If s[0] is '?', it becomes '('.
    # If s[n-1] is '?', it becomes ')'.
    
    # Let's simulate the filling process.
    # We have `needed_open` and `needed_close` to distribute among the '?' positions.
    # However, we must respect the mandatory first and last.
    
    # Let's create a list of indices where '?' occurs.
    q_indices = [i for i, char in enumerate(s) if char == '?']
    
    # We need to assign the first k of these to '(' and the rest to ')'.
    # But we have constraints:
    # 1. s[0] must be '('. If 0 is in q_indices, it MUST be assigned '('.
    # 2. s[n-1] must be ')'. If n-1 is in q_indices, it MUST be assigned ')'.
    
    # Let's separate the mandatory assignments.
    # If s[0] == '?', we use one of our 'needed_open' for it.
    # If s[n-1] == '?', we use one of our 'needed_close' for it.
    
    # Let's verify if the counts allow this.
    # If s[0] == '?', we decrement needed_open.
    # If s[n-1] == '?', we decrement needed_close.
    
    # Wait, the simple greedy "first available '?' gets '(' until count exhausted" might put a ')' at s[0] if we are not careful, 
    # but we already checked s[0] != ')'.
    # The issue is if s[0] is '?', we MUST assign it '('.
    # If s[n-1] is '?', we MUST assign it ')'.
    
    # Let's adjust the counts based on these mandatory assignments.
    if s[0] == '?':
        needed_open -= 1
    if s[n-1] == '?':
        needed_close -= 1
    
    # Now we have remaining needed_open and needed_close to distribute among the remaining '?' (excluding 0 and n-1 if they were '?').
    # The strategy: fill the remaining '?' from left to right with '(' until needed_open is 0, then with ')'.
    # This maximizes the balance early on.
    
    # Let's re-verify the logic with the mandatory assignments.
    # We identified the total needed.
    # If s[0] was '?', we committed one '(' to it.
    # If s[n-1] was '?', we committed one ')' to it.
    # The remaining '?' should be filled greedily: '(' first, then ')'.
    
    # Let's rebuild the string.
    # We'll iterate through the string.
    # We keep track of current balance.
    # We also keep track of how many '(' and ')' we have left to place.
    
    # Re-calculate needed_open and needed_close considering the mandatory ones were already accounted for in the subtraction above?
    # No, the initial calculation was based on total counts.
    # Let's restart the counting logic to be absolutely sure.
    
    # Total length n.
    # Fixed '(': cnt_open
    # Fixed ')': cnt_close
    # Total '?': cnt_q
    # We need final balance 0.
    # Let x be number of '(' we add to '?'.
    # Let y be number of ')' we add to '?'.
    # x + y = cnt_q
    # (cnt_open + x) - (cnt_close + y) = 0 => x - y = cnt_close - cnt_open
    # => 2x = cnt_q + cnt_close - cnt_open = cnt_q - cur_bal
    # => x = (cnt_q - cur_bal) / 2
    # => y = cnt_q - x
    
    # This x and y are the TOTAL number of '(' and ')' we must insert into the '?' slots.
    
    # Now, we must ensure:
    # 1. s[0] is '('.
    # 2. s[n-1] is ')'.
    # 3. Balance > 0 for all prefixes 0..n-2.
    
    # If s[0] == '?', we MUST use one of our x '(' for it.
    # If s[n-1] == '?', we MUST use one of our y ')' for it.
    
    # Let's check feasibility:
    # If s[0] == '?', we need x >= 1.
    # If s[n-1] == '?', we need y >= 1.
    
    # If these hold, we can proceed.
    # We will fill the '?' slots.
    # We have x '(' and y ')' to distribute.
    # To satisfy the prefix condition (balance > 0), we should put '(' as early as possible.
    # So, we fill the first available '?' with '(' until we run out of x, then fill the rest with ')'.
    # BUT we must ensure that if s[0] is '?', it gets '('.
    # And if s[n-1] is '?', it gets ')'.
    
    # Since we are filling from left to right:
    # - If s[0] is '?', it is the first '?'. It will get '(' (since we start with x > 0). Good.
    # - If s[n-1] is '?', it is the last '?'. It will get ')' (since we run out of '(' before the end, assuming y > 0 and we fill all).
    #   Is it guaranteed that we run out of '(' before the last '?'?
    #   We have x '(' and y ')'. Total slots = cnt_q.
    #   We fill first x slots with '(', next y slots with ')'.
    #   The last slot is the (cnt_q)-th slot (0-indexed cnt_q-1).
    #   If y > 0, then the last slot is in the range of ')' assignments (indices x to cnt_q-1).
    #   So the last '?' gets ')'. Good.
    
    # So the algorithm is:
    # 1. Calculate x and y.
    # 2. Check x >= 0, y >= 0, (cnt_q - cur_bal) % 2 == 0.
    # 3. Check if s[0] == ')' or s[n-1] == '(': impossible.
    # 4. Check if s[0] == '?' and x == 0: impossible (need at least one '(').
    # 5. Check if s[n-1] == '?' and y == 0: impossible (need at least one ')').
    # 6. Construct the string:
    #    Iterate i from 0 to n-1.
    #    If s[i] == '(': keep.
    #    If s[i] == ')': keep.
    #    If s[i] == '?':
    #       If we still have x > 0: assign '(', decrement x.
    #       Else: assign ')', decrement y.
    
    # Wait, is this greedy strategy sufficient to ensure balance > 0 for all strict prefixes?
    # Let's trace.
    # We put all available '(' as early as possible. This maximizes the balance at every step.
    # If this configuration fails the condition (balance <= 0 at some point), then no other configuration will work 
    # because any other configuration would have a ')' earlier or a '(' later, which would lower the balance earlier or raise it later, 
    # potentially causing a dip to 0 or below sooner.
    # Specifically, swapping a '(' at index i with a ')' at index j (where i < j) decreases the balance in the range [i, j-1].
    # Since we want balance > 0, we want to avoid dips. Putting '(' as early as possible is optimal.
    
    # One edge case: What if the mandatory ')' at the end causes a dip?
    # The last character MUST be ')'. So balance goes from 1 to 0 at the very end. That is allowed.
    # The condition is "strict prefix", so index n-1 is not a strict prefix.
    # So balance at n-1 being 0 is fine.
    # We just need balance[i] >= 1 for 0 <= i <= n-2.
    
    # Let's implement this.
    
    # Recalculate x and y properly
    cnt_open = s.count('(')
    cnt_close = s.count(')')
    cnt_q = n - cnt_open - cnt_close
    cur_bal = cnt_open - cnt_close
    
    # x = number of '(' to add
    # y = number of ')' to add
    # x + y = cnt_q
    # x - y = cnt_close - cnt_open = -cur_bal
    # 2x = cnt_q - cur_bal
    
    if (cnt_q - cur_bal) % 2 != 0:
        print(":(")
        return
    
    x = (cnt_q - cur_bal) // 2
    y = cnt_q - x
    
    if x < 0 or y < 0:
        print(":(")
        return
    
    # Check first and last characters
    if s[0] == ')':
        print(":(")
        return
    if s[n-1] == '(':
        print(":(")
        return
    
    # Check if we have enough '(' for the first char if it is '?'
    if s[0] == '?' and x == 0:
        print(":(")
        return
    
    # Check if we have enough ')' for the last char if it is '?'
    if s[n-1] == '?' and y == 0:
        print(":(")
        return
    
    # Now construct
    # We will simulate the balance to be sure, although the greedy logic should hold.
    # But let's just build it.
    
    res = []
    open_left = x
    close_left = y
    
    for i in range(n):
        if s[i] == '(':
            res.append('(')
            # balance += 1
        elif s[i] == ')':
            res.append(')')
            # balance -= 1
        else: # '?'
            if open_left > 0:
                res.append('(')
                open_left -= 1
            else:
                res.append(')')
                close_left -= 1
    
    # Verify the result
    # Check 1: Is it a correct parenthesis sequence?
    # Check 2: Is any strict prefix correct?
    
    bal = 0
    possible = True
    for i, char in enumerate(res):
        if char == '(':
            bal += 1
        else:
            bal -= 1
        
        if bal < 0:
            possible = False
            break
        
        # Check strict prefix condition
        # Strict prefix ends at i. Length is i+1.
        # If i+1 < n and bal == 0, then it's a correct strict prefix -> Invalid.
        if i + 1 < n and bal == 0:
            possible = False
            break
    
    if not possible:
        print(":(")
    else:
        print("".join(res))

if __name__ == '__main__':
    solve()