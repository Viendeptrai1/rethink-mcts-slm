import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = [int(data[i+1]) for i in range(n)]
    
    # We need to find the longest strictly increasing sequence by taking from left or right.
    # Since all elements are distinct (Problem C1), we can use a two-pointer approach.
    
    left = 0
    right = n - 1
    last_val = 0
    res = []
    
    # While there are elements left to consider
    while left <= right:
        l_val = a[left]
        r_val = a[right]
        
        # If both ends are greater than the last taken value, we have a choice.
        if l_val > last_val and r_val > last_val:
            if l_val < r_val:
                # Taking left is better because it's smaller, giving us more room for future numbers.
                # Also, since all numbers are distinct, if l_val < r_val, taking l_val is always optimal
                # for the immediate next step compared to taking r_val, unless taking r_val allows
                # a much longer chain later. However, with distinct numbers and the constraint of
                # strictly increasing, the greedy choice of the smaller valid endpoint is correct.
                # Why? Because if we take the larger one (r_val), the next number must be > r_val.
                # If we take the smaller one (l_val), the next number must be > l_val.
                # The set of available numbers > l_val is a superset of numbers > r_val.
                # Thus, taking the smaller valid number never hurts and often helps.
                res.append('L')
                last_val = l_val
                left += 1
            else:
                res.append('R')
                last_val = r_val
                right -= 1
        elif l_val > last_val:
            res.append('L')
            last_val = l_val
            left += 1
        elif r_val > last_val:
            res.append('R')
            last_val = r_val
            right -= 1
        else:
            # Neither can be taken
            break
            
    print(len(res))
    print("".join(res))

if __name__ == "__main__":
    solve()