import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    n = int(data[0])
    a = []
    for i in range(2 * n):
        a.append(int(data[1 + i]))
    
    current_sum = 0
    for x in a:
        current_sum += x
    
    if current_sum % (2 * n) == 0:
        avg = current_sum // (2 * n)
        # If we sort, can we make one half sum to something other than avg?
        # Actually, if all elements are equal, we cannot split them unequally.
        # Let's check if all elements are the same.
        if len(set(a)) == 1:
            print("-1")
            return
    
    # Strategy: Sort the array. Try to construct two halves such that their sums are different.
    # Since not all elements are equal, there exists at least one pair with different values.
    # We can try a simple greedy approach or sorting based strategy.
    # A known constructive approach for this problem:
    # 1. Sort the array.
    # 2. Try to form the first half with the smallest elements and the second half with the largest?
    #    Or mix them up to avoid the equal sum case if it happens.
    
    # Actually, a simpler randomized or constructive logic works:
    # Since n <= 1000, we can try to construct it.
    # Let's sort the array first.
    a.sort()
    
    # Check if the sorted split works
    left_sum = sum(a[:n])
    right_sum = sum(a[n:])
    
    if left_sum != right_sum:
        print(*(a))
        return
    
    # If the sorted split yields equal sums, we need to swap elements between the two halves
    # to change the sums. Since not all elements are equal, such a swap exists.
    # Find an element in left half and an element in right half that are different.
    # If we swap a[i] (left) and a[j] (right), the new left sum becomes left_sum - a[i] + a[j]
    # and new right sum becomes right_sum - a[j] + a[i].
    # Since left_sum == right_sum, the new sums will differ if a[i] != a[j].
    
    swapped = False
    for i in range(n):
        for j in range(n, 2 * n):
            if a[i] != a[j]:
                # Swap
                a[i], a[j] = a[j], a[i]
                print(*(a))
                swapped = True
                return
    
    # Theoretically unreachable if not all elements are equal
    print("-1")

if __name__ == "__main__":
    solve()