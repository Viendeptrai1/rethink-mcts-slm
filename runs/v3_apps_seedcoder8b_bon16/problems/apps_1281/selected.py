def max_segments(n, k, a):
    # To maximize the number of segments with XOR not equal to 0, consider toggling
    # each bit position separately. This results in 2^k possibilities for each bit position.

    # We will use a greedy approach:
    # 1. Calculate the current XOR for the entire array.
    # 2. For each bit position, consider flipping that bit for every element in the array.
    # 3. Calculate the new XOR for the array after the bit flip.
    # 4. Keep track of the maximum number of segments that can be obtained.

    # Step 1: Calculate the XOR of the entire array
    total_xor = 0
    for num in a:
        total_xor ^= num
    
    # If the total XOR is already non-zero, we can have all segments.
    if total_xor != 0:
        return n

    # Step 2: Consider flipping each bit position
    max_segments = 0
    # Since k can be at most 30, the maximum number of unique results we can have is 2^30, which is a large number.
    # To ensure we cover all possibilities, let's simulate flipping each bit position one by one.
    for bit in range(k):
        # We will try to see what happens if we flip each bit position.
        xor_with_flip = 0
        for num in a:
            # Flip the bit at position `bit`
            flipped_num = num ^ (1 << bit)
            xor_with_flip ^= flipped_num
        
        # If flipping this bit results in non-zero XOR, count the segments
        if xor_with_flip != 0:
            max_segments = max(max_segments, n)
            # Once we find one position where flipping gives us a non-zero XOR,
            # we can conclude that we can get all segments since we are flipping all bits.

    return max_segments

# To handle input and output according to the problem statement
import sys
input = sys.stdin.read

def main():
    data = input().strip().split()
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:n+2]))
    
    result = max_segments(n, k, a)
    print(result)

if __name__ == "__main__":
    main()