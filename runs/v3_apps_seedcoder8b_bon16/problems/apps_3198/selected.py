def find_typos(n, words):
    word_set = set(words)
    typos = []

    for word in words:
        # Try removing each character from the word
        for i in range(len(word)):
            modified_word = word[:i] + word[i+1:]
            if modified_word in word_set:
                typos.append(word)
                break

    if not typos:
        print("NO TYPOS")
    else:
        for typo in typos:
            print(typo)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    words = data[1:n+1]
    
    find_typos(n, words)