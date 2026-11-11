import sys
from collections import Counter

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    heights = list(map(int, data[1:n+1]))
    
    freq = Counter(heights)
    
    max_length = 0
    best_circle = []
    
    for height in sorted(freq):
        if freq[height] > 0:
            current_length = freq[height]
            current_circle = [height] * freq[height]
            
            if freq[height + 1] > 0:
                current_length += freq[height + 1]
                current_circle.extend([height + 1] * freq[height + 1])
            
            if freq[height - 1] > 0:
                current_length += freq[height - 1]
                current_circle.extend([height - 1] * freq[height - 1])
            
            if current_length > max_length:
                max_length = current_length
                best_circle = current_circle
    
    print(max_length)
    print(" ".join(map(str, best_circle)))

if __name__ == "__main__":
    main()