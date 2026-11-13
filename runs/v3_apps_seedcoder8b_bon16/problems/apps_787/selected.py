def find_beautiful_sequence(k, q):
    from collections import defaultdict

    if k > len(q):
        print("NO")
        return

    freq = defaultdict(int)
    for char in q:
        freq[char] += 1

    used_chars = set()
    beautiful_sequence = []
    current_string = []

    for char in q:
        if char not in used_chars and len(beautiful_sequence) < k - 1:
            if current_string:
                beautiful_sequence.append(''.join(current_string))
            current_string = [char]
            used_chars.add(char)
        else:
            current_string.append(char)

    if current_string and len(beautiful_sequence) < k:
        beautiful_sequence.append(''.join(current_string))

    if len(beautiful_sequence) == k:
        print("YES")
        for s in beautiful_sequence:
            print(s)
    else:
        print("NO")

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    k = int(data[0])
    q = data[1]
    find_beautiful_sequence(k, q)