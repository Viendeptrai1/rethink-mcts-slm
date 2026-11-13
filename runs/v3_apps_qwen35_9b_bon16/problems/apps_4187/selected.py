import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    a = [int(x) for x in data[1:]]
    
    # Count consecutive 1s wrapping around the array
    max_rest = 0
    current_rest = 0
    
    # We need to simulate the circular nature. 
    # One way is to concatenate the array to itself and then look for the longest run of 1s.
    # However, since there is at least one 0, the max run cannot exceed n.
    # Concatenating and scanning up to 2*n is safe and efficient.
    
    # Create doubled array
    doubled = a + a
    
    # We only need to scan up to n + (n - 1) effectively, but scanning 2*n is fine.
    # Actually, the longest possible sequence of rests cannot be longer than n because there's at least one 0.
    # So scanning the first n + n - 1 elements of the doubled array is sufficient to cover all wrapping cases.
    
    length = n + n
    for i in range(length):
        if doubled[i] == 1:
            current_rest += 1
            if current_rest > max_rest:
                max_rest = current_rest
        else:
            current_rest = 0
            
    print(max_rest)

if __name__ == "__main__":
    solve()