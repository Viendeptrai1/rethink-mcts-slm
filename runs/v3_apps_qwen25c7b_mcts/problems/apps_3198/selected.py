import sys

def find_typos(dictionary):
    n = len(dictionary)
    sorted_dict = sorted(dictionary)
    
    def binary_search(word):
        left, right = 0, n - 1
        while left <= right:
            mid = (left + right) // 2
            if sorted_dict[mid] == word:
                return True
            elif sorted_dict[mid] < word:
                left = mid + 1
            else:
                right = mid - 1
        return False
    
    typos = []
    for word in dictionary:
        for i in range(len(word)):
            candidate = word[:i] + word[i+1:]
            if binary_search(candidate):
                typos.append(word)
                break
    
    return typos

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    dictionary = data[1:n+1]
    typos = find_typos(dictionary)
    if typos:
        print("\n".join(typos))
    else:
        print("NO TYPOS")