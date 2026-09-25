import sys

def count_positions_to_make_regular(n, s):
    open_count = 0
    close_count = 0
    balance = 0
    result = 0

    for i in range(n):
        if s[i] == '(':
            open_count += 1
        else:
            close_count += 1

        if s[i] == '(':
            balance += 1
        else:
            balance -= 1

        # If balance is negative, it means there are more ')' than '('
        # We can make it regular by changing this ')'
        if balance < 0:
            result += 1
            balance = 0

    # Check if we have more '(' than ')'
    if open_count > close_count:
        result += open_count - close_count

    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    s = data[1]
    print(count_positions_to_make_regular(n, s))

if __name__ == "__main__":
    main()