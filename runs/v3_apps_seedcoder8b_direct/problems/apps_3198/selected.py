def find_typos(n, words):
    word_set = set(words)
    typos = []

    for word in words:
        for i in range(len(word)):
            # Create a new word by removing the i-th character
            modified_word = word[:i] + word[i+1:]
            if modified_word in word_set:
                typos.append(word)
                break

    if not typos:
        print("NO TYPOS")
    else:
        for typo in typos:
            print(typo)

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
words = data[1:n+1]

find_typos(n, words)