import sys

def is_regular_sequence(s):
    balance = 0
    for char in s:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return False
    return balance == 0

def count_positions_to_make_regular(n, s):
    count = 0
    for i in range(n):
        # Create a new sequence by changing the i-th bracket
        new_s = s[:i] + ('(' if s[i] == ')' else ')') + s[i+1:]
        if is_regular_sequence(new_s):
            count += 1
    return count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    s = data[1]
    result = count_positions_to_make_regular(n, s)
    print(result)

if __name__ == "__main__":
    main()