from collections import Counter
import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    X = int(data[1], 2)
    
    A = [int(x, 2) for x in data[2:N+2]]
    
    # Initialize the counter with the initial numbers
    cnt = Counter(A)
    
    # Set to keep track of numbers that have been processed
    processed = set(A)
    
    while True:
        new_numbers = False
        
        # Try doubling each number
        for num in list(processed):
            double_num = num * 2
            if double_num <= X and double_num not in processed:
                cnt[double_num] += cnt[num]
                processed.add(double_num)
                new_numbers = True
        
        # Try XORing pairs of numbers
        for num1 in list(processed):
            for num2 in list(processed):
                xor_num = num1 ^ num2
                if xor_num <= X and xor_num not in processed:
                    cnt[xor_num] += cnt[num1] * cnt[num2]
                    processed.add(xor_num)
                    new_numbers = True
        
        # If no new numbers were added, break the loop
        if not new_numbers:
            break
    
    # Sum up the counts of all numbers not exceeding X
    result = sum(cnt[num] for num in range(X + 1))
    
    # Print the result modulo 998244353
    print(result % 998244353)

if __name__ == "__main__":
    main()