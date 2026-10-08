import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    # Calculate the maximum number of problems that can be solved
    max_problems = 0
    current_problems = 1
    for _ in range(k):
        max_problems += current_problems
        current_problems *= 2
    
    if n > max_problems:
        print("NO")
        return
    
    # Construct the sequence
    sequence = []
    remaining_problems = n
    current_problems = 1
    
    for i in range(k):
        if i == k - 1:
            sequence.append(remaining_problems)
        else:
            next_problems = min(2 * current_problems, remaining_problems - (k - i - 1))
            sequence.append(current_problems)
            remaining_problems -= current_problems
            current_problems = next_problems
    
    print("YES")
    print(" ".join(map(str, sequence)))

if __name__ == "__main__":
    main()