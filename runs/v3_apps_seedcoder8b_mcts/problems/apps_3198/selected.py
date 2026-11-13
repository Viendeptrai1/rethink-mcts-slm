def find_typos():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    words = data[1:n+1]
    
    word_set = set(words)
    typos = []
    
    for word in words:
        for i in range(len(word)):
            # Create a new word by removing the i-th character
            potential_typo = word[:i] + word[i+1:]
            if potential_typo in word_set:
                typos.append(word)
                break
    
    if typos:
        for typo in typos:
            print(typo)
    else:
        print("NO TYPOS")