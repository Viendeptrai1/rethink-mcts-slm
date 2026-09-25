import sys
from collections import Counter

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:]))
    
    # Check if the maximum frequency of any element is greater than k
    freq = Counter(a)
    max_freq = max(freq.values())
    
    if max_freq > k:
        print("NO")
    else:
        print("YES")
        color = 1
        colors = []
        used = {}
        
        for i in range(n):
            if a[i] not in used or used[a[i]] == k:
                used[a[i]] = 1
                colors.append(color)
                color = (color % k) + 1
            else:
                used[a[i]] += 1
                colors.append(color)
        
        print(" ".join(map(str, colors)))

if __name__ == "__main__":
    main()