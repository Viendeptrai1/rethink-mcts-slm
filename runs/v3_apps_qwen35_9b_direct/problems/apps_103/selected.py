import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = []
    for i in range(n):
        a.append(int(input_data[1 + i]))
    
    if n == 1:
        print(0)
        return
    
    # Check if we can erase the first k elements
    # Condition: a[k] - a[0] > k  (since we need at least k+1 numbers to fill k gaps? No.)
    # Let's re-derive.
    # If we erase a[0]...a[k-1], the remaining array starts at a[k].
    # We need to fill k numbers: x_1, x_2, ..., x_k such that:
    # 1 <= x_1 < x_2 < ... < x_k < a[k]
    # The smallest possible sequence is 1, 2, ..., k.
    # So we need k < a[k] - 1? No.
    # The condition is that there exists a sequence of length k strictly between 1 and a[k].
    # The number of integers strictly between 1 and a[k] is (a[k] - 1) - 1 = a[k] - 2?
    # Wait, the sequence is x_1, ..., x_k.
    # 1 <= x_1 < x_2 < ... < x_k < a[k]
    # The maximum value for x_k is a[k] - 1.
    # The minimum value for x_1 is 1.
    # We need to fit k integers in the range [1, a[k]-1].
    # The number of available integers is (a[k]-1) - 1 + 1 = a[k] - 1.
    # We need k <= a[k] - 1.
    # So a[k] - a[0] > k? No, a[0] is 1 in this case? No, a[0] is the first element.
    # If we erase the first k elements, the new start is a[k].
    # The values must be >= 1.
    # So we need to fit k numbers in [1, a[k]-1].
    # Count of numbers in [1, a[k]-1] is a[k]-1.
    # We need k <= a[k] - 1.
    # So a[k] - 1 >= k  => a[k] >= k + 1.
    # But wait, the original array has a[0]. If we erase a[0]...a[k-1], the remaining is a[k]...a[n-1].
    # The gap is between 1 (implicit lower bound) and a[k].
    # We need to insert k numbers.
    # The condition is: a[k] - 1 >= k.
    # Let's check example 3: 1 2 3 4 5. n=5.
    # Erase first 4: remaining is [5]. k=4.
    # Condition: 5 - 1 >= 4 => 4 >= 4. True.
    # Erase first 5: remaining is []. k=5.
    # Condition: 5 - 1 >= 5 => 4 >= 5. False.
    # So max k for prefix is the largest k such that a[k] - 1 >= k.
    # Actually, if we erase k elements from the start, the first remaining element is a[k] (0-indexed).
    # The number of erased elements is k.
    # We need to fill k numbers in [1, a[k]-1].
    # Number of available slots = a[k] - 1.
    # We need k <= a[k] - 1.
    # So a[k] - k >= 1.
    
    # Check if we can erase the last k elements
    # If we erase a[n-k]...a[n-1], the remaining ends at a[n-k-1].
    # We need to fill k numbers in (a[n-k-1], 1000].
    # The number of available integers is 1000 - a[n-k-1].
    # We need k <= 1000 - a[n-k-1].
    # So 1000 - a[n-k-1] >= k.
    
    # Check if we can erase a middle segment of length k
    # Erase a[i]...a[i+k-1]. Remaining: a[0]...a[i-1] and a[i+k]...a[n-1].
    # We need to fill k numbers in (a[i-1], a[i+k]).
    # Number of available integers = a[i+k] - a[i-1] - 1.
    # We need k <= a[i+k] - a[i-1] - 1.
    # So a[i+k] - a[i-1] - 1 >= k.
    # Note: if i=0, lower bound is 1. If i+k=n, upper bound is 1000.
    
    # We want to maximize k.
    # k can range from 0 to n-1 (since we must leave at least 1 element? 
    # Wait, the problem says "Giraffe can still restore the array".
    # If we erase everything, can he restore? No, because he doesn't know n? 
    # Actually, n is given in the input? No, the input is what Giraffe wrote.
    # "Giraffe has written on the board an array... then went to the bathroom."
    # "JATC decided to prank... erasing some consecutive elements".
    # "Giraffe can still restore the array using the information from the remaining elements."
    # Giraffe knows n? The problem says "Giraffe has written... an array a_1...a_n".
    # Usually in such problems, n is known or can be deduced?
    # If we erase all elements, Giraffe sees an empty board. He knows n?
    # The problem statement says "Giraffe has created the array... he's also aware that it's an increasing array and all the elements are integers in the range [1, 1000]".
    # It doesn't explicitly say he knows n. But typically, if n is not known, he can't restore the array uniquely if multiple lengths are possible.
    # However, the examples suggest we can erase n-1 elements.
    # Example 3: 1 2 3 4 5 -> erase 4 elements -> [5]. Restored as 1,2,3,4,5.
    # If we erase 5 elements -> []. Can he restore? If he doesn't know n, no.
    # But the output for Ex 3 is 4. So we must leave at least 1 element.
    # So k < n.
    
    max_k = 0
    
    # Try all possible lengths k from 1 to n-1
    # And all possible starting positions i such that we erase a[i]...a[i+k-1]
    # The erased segment is from index i to i+k-1 (0-indexed).
    # Length is k.
    # Valid i: 0 <= i <= n - k.
    # If i=0, left bound is 1.
    # If i+k=n, right bound is 1000.
    # Otherwise, left bound is a[i-1], right bound is a[i+k].
    
    for k in range(1, n):
        possible = False
        for i in range(n - k + 1):
            # Erase a[i] ... a[i+k-1]
            # Left neighbor index: i-1. If i=0, left_val = 1.
            # Right neighbor index: i+k. If i+k=n, right_val = 1000.
            
            if i == 0:
                left_val = 1
            else:
                left_val = a[i-1]
            
            if i + k == n:
                right_val = 1000
            else:
                right_val = a[i+k]
            
            # Number of integers strictly between left_val and right_val
            # Count = right_val - left_val - 1
            available = right_val - left_val - 1
            
            if available >= k:
                possible = True
                break
        
        if possible:
            max_k = k
    
    print(max_k)

if __name__ == '__main__':
    solve()