def find_beautiful_sequence(k, q):
    from collections import defaultdict

    # Count frequency of each character in q
    char_count = defaultdict(int)
    for char in q:
        char_count[char] += 1

    # If there are fewer distinct characters than k, it's impossible
    if len(char_count) < k:
        print("NO")
        return

    # Create a list of characters sorted by frequency
    sorted_chars = sorted(char_count.keys(), key=lambda x: -char_count[x])

    # Create the beautiful sequence
    beautiful_sequence = []
    current_string = []
    used_chars = set()

    for char in q:
        if char not in used_chars and len(beautiful_sequence) < k - 1:
            if current_string:
                beautiful_sequence.append(''.join(current_string))
                current_string = []
            used_chars.add(char)
        current_string.append(char)

    # Add the last string
    if current_string:
        beautiful_sequence.append(''.join(current_string))

    # Ensure we have exactly k strings
    while len(beautiful_sequence) < k:
        beautiful_sequence.append('')

    # Print the result
    print("YES")
    for s in beautiful_sequence:
        print(s)

# Read input
k = int(input())
q = input().strip()

# Call the function
find_beautiful_sequence(k, q)