import sys
from collections import Counter

def main():
    import sys
    import collections
    
    def readints():
        return list(map(int, sys.stdin.read().split()))
    
    data = readints()
    n = data[0]
    a = data[1:]
    
    # Count the frequency of each element
    freq = collections.Counter(a)
    
    # Check for elements with frequency more than 2
    for count in freq.values():
        if count > 2:
            print("NO")
            return
    
    # Separate elements into increasing and decreasing parts
    inc = []
    dec = []
    
    for num in sorted(freq):
        if freq[num] == 1:
            inc.append(num)
        elif freq[num] == 2:
            inc.append(num)
            dec.append(num)
    
    # Check if the sequences are valid
    if inc and dec and inc[-1] >= dec[0]:
        print("NO")
        return
    
    # Output the result
    print("YES")
    print(len(inc))
    print(" ".join(map(str, inc)))
    print(len(dec))
    print(" ".join(map(str, dec)))

if __name__ == "__main__":
    main()