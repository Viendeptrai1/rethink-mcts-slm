import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    words = input_data[1:]

    # Use a set for O(1) average time complexity lookups
    word_set = set(words)

    typos = []

    for word in words:
        is_typo = False
        # Try deleting each character at each position
        for i in range(len(word)):
            # Create the new word by skipping the character at index i
            candidate = word[:i] + word[i+1:]
            if candidate in word_set:
                is_typo = True
                break
        
        if is_typo:
            typos.append(word)

    if not typos:
        print("NO TYPOS")
    else:
        for t in typos:
            print(t)

if __name__ == "__main__":
    solve()