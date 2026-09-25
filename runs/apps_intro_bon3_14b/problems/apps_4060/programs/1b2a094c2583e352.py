import sys

def count_positions_to_make_regular(n, s):
    open_count = 0
    close_count = 0
    imbalance = 0
    result = 0

    for i in range(n):
        if s[i] == '(':
            open_count += 1
        else:
            close_count += 1

        # Calculate the imbalance at position i
        imbalance = close_count - open_count

        # If imbalance is negative, it means there are more ')' than '('
        # Changing this ')' to '(' would make the sequence regular up to this point
        if imbalance < 0:
            result += 1

        # If imbalance is zero, it means the sequence is balanced up to this point
        # Changing any '(' to ')' or ')' to '(' would not make it regular
        # So we reset the imbalance counter
        if imbalance == 0:
            open_count = 0
            close_count = 0

    return result

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