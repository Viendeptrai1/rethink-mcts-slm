import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = []
    for i in range(n):
        a.append(int(input_data[i + 1]))

    # The candidate must be one of the elements in the array.
    # The smallest element is the only possible candidate that could divide all others.
    # If the smallest element divides all other elements, it is the answer.
    # Otherwise, no such number exists because any other number would be >= smallest
    # and if it's not the smallest, it can't divide the smallest (unless equal).
    # Actually, the logic is simpler: the answer must be the GCD of all elements.
    # If the GCD is present in the array, that's our answer. Since the GCD divides every element,
    # and the GCD is the smallest possible divisor common to all, if the GCD is in the array,
    # it must be the minimum element.
    
    # Let's find the minimum element first.
    min_val = min(a)
    
    # Check if min_val divides all elements
    for x in a:
        if x % min_val != 0:
            print("-1")
            return
    
    print(min_val)

if __name__ == "__main__":
    solve()