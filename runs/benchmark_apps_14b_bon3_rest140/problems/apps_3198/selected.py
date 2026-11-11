import sys

def find_typos(dictionary):
    typos = []
    word_set = set(dictionary)
    
    for word in dictionary:
        for i in range(len(word)):
            modified_word = word[:i] + word[i+1:]
            if modified_word in word_set and modified_word != word:
                typos.append(word)
                break
    
    return typos

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    dictionary = data[1:]
    
    typos = find_typos(dictionary)
    
    if typos:
        for typo in typos:
            print(typo)
    else:
        print("NO TYPOS")

if __name__ == "__main__":
    main()