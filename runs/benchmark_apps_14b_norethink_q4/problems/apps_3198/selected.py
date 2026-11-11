import sys

def find_typos(dictionary):
    word_set = set(dictionary)
    typos = []

    for word in dictionary:
        for i in range(len(word)):
            candidate = word[:i] + word[i+1:]
            if candidate in word_set and candidate != word:
                typos.append(word)
                break

    return typos

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
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