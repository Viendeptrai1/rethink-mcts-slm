import sys
from typing import List

def min_blow_to_defeat_zmei(n: int, x: int, blows: List[List[int]]) -> int:
    # Sort blows by efficiency (h_i / d_i) in descending order
    blows.sort(key=lambda b: b[1] / b[0], reverse=True)
    
    total_blow_count = 0
    
    while x > 0:
        max_heads_gained = 0
        best_blow_index = -1
        
        for i, (d, h) in enumerate(blows):
            heads_gained = min(d, x)
            new_heads = x - heads_gained + h
            
            if new_heads > max_heads_gained:
                max_heads_gained = new_heads
                best_blow_index = i
        
        if best_blow_index == -1:
            return -1
        
        _, h = blows[best_blow_index]
        x -= min(h, x)
        total_blow_count += 1
    
    return total_blow_count

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        index += 1
        x = int(data[index])
        index += 1
        blows = []
        
        for _ in range(n):
            d = int(data[index])
            index += 1
            h = int(data[index])
            index += 1
            blows.append([d, h])
        
        result = min_blow_to_defeat_zmei(n, x, blows)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()