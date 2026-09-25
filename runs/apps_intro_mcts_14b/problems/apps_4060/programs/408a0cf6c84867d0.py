import sys

def count_positions_to_make_regular(n, s):
    min_balance = 0
    current_balance = 0
    positions = 0
    
    for i in range(n):
        if s[i] == '(':
            current_balance += 1
        else:
            current_balance -= 1
        
        if current_balance < min_balance:
            min_balance = current_balance
        
        # Check if changing s[i] can make the sequence regular
        if (min_balance + 1 <= 0 <= current_balance) or (current_balance == 0 and min_balance == -1):
            positions += 1
    
    return positions

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