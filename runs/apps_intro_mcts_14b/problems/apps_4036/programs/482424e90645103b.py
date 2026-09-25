import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    # Calculate the minimum number of problems that can be solved in k days
    min_problems = 0
    current_problems = 1
    for i in range(k):
        min_problems += current_problems
        current_problems *= 2
    
    if min_problems > n:
        print("NO")
        return
    
    # Construct the sequence
    sequence = []
    remaining_problems = n
    current_problems = 1
    for i in range(k):
        max_problems = min(remaining_problems, 2 * current_problems)
        if i == k - 1 or max_problems > current_problems:
            sequence.append(current_problems)
            remaining_problems -= current_problems
            current_problems = max_problems
        else:
            print("NO")
            return
    
    if remaining_problems != 0:
        print("NO")
        return
    
    print("YES")
    print(" ".join(map(str, sequence)))

if __name__ == "__main__":
    main()