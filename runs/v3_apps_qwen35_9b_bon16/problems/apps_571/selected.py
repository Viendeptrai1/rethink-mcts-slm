import sys

def solve():
    try:
        input_data = sys.stdin.read().split()
    except Exception:
        return

    if not input_data:
        return

    n = int(input_data[0])
    s = list(input_data[1])

    if n % 2 == 1:
        print(":(")
        return

    # A correct parenthesis sequence must have length even.
    # Also, for the condition "all strict prefixes are NOT correct",
    # we know:
    # 1. The total sequence must be correct (balance == 0, prefix balance >= 0).
    # 2. No proper prefix can be correct. A proper prefix is correct if its balance is 0 and it never dropped below 0.
    #    Since our construction ensures prefix balance >= 0, a proper prefix is correct IFF its balance is 0.
    #    Therefore, we need: total balance = 0, and for all 1 <= i < n, prefix_balance[i] > 0.
    
    # To maximize the chance of satisfying "balance > 0 for all proper prefixes", we should:
    # - Put as many '(' as possible early to keep the balance high.
    # - Put as many ')' as possible late to bring the balance down to 0 only at the very end.
    #
    # Strategy:
    # 1. Count current balance of fixed characters.
    # 2. Determine how many '?' need to be '(' and how many need to be ')'.
    #    Let `cnt_open` be the number of fixed '('.
    #    Let `cnt_close` be the number of fixed ')'.
    #    Let `q` be the number of '?'.
    #    Total open needed = n/2. Total close needed = n/2.
    #    So we need `need_open = n/2 - cnt_open` more opens, and `need_close = n/2 - cnt_close` more closes.
    #    If either is negative or their sum != q, impossible.
    #
    # 3. Fill the first `need_open` question marks with '('.
    # 4. Fill the remaining `need_close` question marks with ')'.
    #
    # 5. Simulate the balance:
    #    - If at any point balance < 0, invalid.
    #    - If at any point i < n-1, balance == 0, invalid (strict prefix would be correct).
    #    - At i == n-1, balance must be 0.

    cnt_open_fixed = s.count('(')
    cnt_close_fixed = s.count(')')
    q_count = s.count('?')

    need_open = n // 2 - cnt_open_fixed
    need_close = n // 2 - cnt_close_fixed

    if need_open < 0 or need_close < 0 or need_open + need_close != q_count:
        print(":(")
        return

    # Fill the '?'
    open_filled = 0
    close_filled = 0
    for i in range(n):
        if s[i] == '?':
            if open_filled < need_open:
                s[i] = '('
                open_filled += 1
            else:
                s[i] = ')'
                close_filled += 1

    # Check conditions
    balance = 0
    for i in range(n):
        if s[i] == '(':
            balance += 1
        else:
            balance -= 1
        
        if balance < 0:
            print(":(")
            return
        
        if i < n - 1 and balance == 0:
            print(":(")
            return

    if balance != 0:
        print(":(")
        return

    print("".join(s))

if __name__ == '__main__':
    solve()