def find_typos(dictionary):
    n = len(dictionary)
    typos = []
    
    # Create a set for faster lookup
    dict_set = set(dictionary)
    
    for word in dictionary:
        for i in range(len(word)):
            candidate = word[:i] + word[i+1:]
            if candidate in dict_set:
                typos.append(word)
                break
    
    return typos if typos else "NO TYPOS"

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    dictionary = data[1:n+1]
    result = find_typos(dictionary)
    print(result)