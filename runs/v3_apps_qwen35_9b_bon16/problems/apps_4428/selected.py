import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    d = []
    for i in range(n):
        d.append(int(data[1 + i]))
    
    if n == 0:
        print(0)
        return
    
    # Total sum of the array
    total_sum = sum(d)
    
    # Two pointers approach
    # left_ptr points to the start of the second part (exclusive)
    # right_ptr points to the end of the second part (exclusive)
    # Initially:
    # Part 1 is empty (sum1 = 0)
    # Part 2 is the whole array (sum2 = total_sum)
    # Part 3 is empty (sum3 = 0)
    
    left_ptr = 0
    right_ptr = n
    sum1 = 0
    sum3 = 0
    max_sum = 0
    
    # Move left_ptr forward to build sum1
    # Move right_ptr backward to build sum3
    
    while left_ptr < right_ptr:
        # If sum1 equals sum3, we found a valid split
        if sum1 == sum3:
            max_sum = sum1
            # We can try to expand further. 
            # Since we want to maximize, we continue. 
            # But note: if we expand sum1, we must also have a matching sum3 later.
            # The standard approach is to try to grow the smaller sum.
            # However, a simpler logic is:
            # If sum1 == sum3, we record it. Then we can try to grow sum1 or sum3.
            # But actually, if they are equal, we can try to grow sum1 by including the next element from the left.
            # Or grow sum3 by including the previous element from the right.
            # Which one to choose? It doesn't matter which one we pick first because we will eventually check equality again.
            # But to avoid infinite loops or missing states, let's just pick one.
            # Actually, the standard two-pointer for this problem:
            # If sum1 == sum3, we update max_sum, then we try to grow sum1 (add d[left_ptr]) because if we grow sum3, we might miss the case where sum1 was larger?
            # No, the logic is: if sum1 == sum3, we have a candidate. Then we must move at least one pointer to try new combinations.
            # Let's move the left pointer to try to increase sum1.
            left_ptr += 1
            sum1 += d[left_ptr - 1]
        elif sum1 < sum3:
            # sum1 is smaller, try to increase it
            left_ptr += 1
            sum1 += d[left_ptr - 1]
        else: # sum3 < sum1
            # sum3 is smaller, try to increase it
            right_ptr -= 1
            sum3 += d[right_ptr]
    
    # Final check after loop
    if sum1 == sum3:
        max_sum = sum1
    
    print(max_sum)

if __name__ == '__main__':
    solve()