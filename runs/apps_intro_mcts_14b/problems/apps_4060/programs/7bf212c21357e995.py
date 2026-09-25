import sys

def main():
    import sys
    n = int(sys.stdin.readline().strip())
    s = sys.stdin.readline().strip()
    
    # Calculate the balance of the bracket sequence
    balance = 0
    min_balance = 0
    for char in s:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        min_balance = min(min_balance, balance)
    
    # If the final balance is not zero, no single change can make it regular
    if balance != 0:
        print(0)
        return
    
    # Count the number of positions where changing the bracket makes the sequence regular
    count = 0
    balance = 0
    for char in s:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        # Check if changing this bracket would make the sequence regular
        if (char == '(' and balance - 1 >= min_balance) or (char == ')' and balance + 1 >= min_balance):
            count += 1
    
    print(count)

if __name__ == "__main__":
    main()