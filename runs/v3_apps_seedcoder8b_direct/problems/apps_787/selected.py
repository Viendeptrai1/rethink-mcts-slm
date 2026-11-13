def find_beautiful_sequence(k, q):
    from collections import defaultdict

    # Check if it's possible to form a beautiful sequence
    if k > len(q):
        print("NO")
        return

    # Dictionary to keep track of the first character of each string
    first_char_count = defaultdict(int)

    # List to store the beautiful sequence
    beautiful_sequence = []

    # Iterate over the string q
    i = 0
    while i < len(q):
        # Try to form a string starting with a unique first character
        for j in range(i, len(q)):
            first_char = q[i]
            if first_char_count[first_char] == 0:
                # Found a unique first character
                beautiful_sequence.append(q[i:j+1])
                first_char_count[first_char] += 1
                i = j + 1
                break
        else:
            # If no unique first character is found, it's not possible
            print("NO")
            return

    # Check if we have exactly k strings
    if len(beautiful_sequence) == k:
        print("YES")
        for s in beautiful_sequence:
            print(s)
    else:
        print("NO")

# Read input
import sys
input = sys.stdin.read
data = input().split()
k = int(data[0])
q = data[1]

# Find beautiful sequence
find_beautiful_sequence(k, q)