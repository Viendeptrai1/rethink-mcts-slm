import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = []
    idx = 1
    for _ in range(n):
        a.append(int(input_data[idx]))
        idx += 1

    # The number must divide all elements, so it must divide the GCD of the array.
    # Also, the number must be one of the elements in the array.
    # Therefore, the answer is the smallest element in the array if and only if
    # that smallest element divides all other elements (i.e., it equals the GCD).
    # Actually, a stronger condition: if an element x divides all elements, then x must be <= GCD.
    # Since x is in the array, and GCD divides x, we must have x = GCD.
    # So we just need to compute the GCD of the array and check if it exists in the array.
    # However, note: if the GCD of the array is g, then any common divisor must divide g.
    # The problem asks for a number *from the array* that divides all elements.
    # Let g = gcd(a_1, ..., a_n). If there is such a number x in the array, then x divides g.
    # But also g divides x (since g divides every element, including x).
    # Therefore, x must equal g.
    # So the answer is the GCD of the array, provided that the GCD is present in the array.
    # Wait, is the GCD always the smallest element? Not necessarily, but the GCD is always <= min(a).
    # And if the GCD is in the array, then it must be the min element? 
    # Let g = gcd(a). Since g divides every element, g <= min(a). 
    # If g is in the array, then since g <= min(a) and min(a) is in the array, g must be min(a).
    # So the algorithm is:
    # 1. Find the minimum element in the array.
    # 2. Check if this minimum element divides all other elements.
    # If yes, print it. Else, print -1.

    min_val = min(a)
    for x in a:
        if x % min_val != 0:
            print("-1")
            return

    print(min_val)

if __name__ == "__main__":
    solve()