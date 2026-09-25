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
        color_assignment = []
        used_colors = set()
        
        for i in range(n):
            if a[i] not in freq or freq[a[i]] == 0:
                continue
            if color not in used_colors:
                used_colors.add(color)
            color_assignment.append(color)
            freq[a[i]] -= 1
            if freq[a[i]] == 0:
                color += 1
                if color > k:
                    color = 1
        
        print(" ".join(map(str, color_assignment)))

if __name__ == "__main__":
    main()