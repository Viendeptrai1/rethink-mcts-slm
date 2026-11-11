import sys
from collections import Counter

def main():
    import sys
    import sys
    n = int(sys.stdin.readline().strip())
    s = sys.stdin.readline().strip()
    
    # Initialize counters for each group
    count_0 = Counter()
    count_1 = Counter()
    count_2 = Counter()
    
    # Group the lamps based on their positions modulo 3
    for i in range(n):
        if i % 3 == 0:
            count_0[s[i]] += 1
        elif i % 3 == 1:
            count_1[s[i]] += 1
        else:
            count_2[s[i]] += 1
    
    # Determine the most frequent color in each group
    max_color_0 = count_0.most_common(1)[0][0]
    max_color_1 = count_1.most_common(1)[0][0]
    max_color_2 = count_2.most_common(1)[0][0]
    
    # Calculate the minimum number of recolors needed
    r = 0
    t = []
    for i in range(n):
        if i % 3 == 0:
            if s[i] != max_color_0:
                r += 1
            t.append(max_color_0)
        elif i % 3 == 1:
            if s[i] != max_color_1:
                r += 1
            t.append(max_color_1)
        else:
            if s[i] != max_color_2:
                r += 1
            t.append(max_color_2)
    
    # Print the result
    print(r)
    print(''.join(t))

if __name__ == "__main__":
    main()