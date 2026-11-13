from math import comb

def count_unique_sums(x1, y1, x2, y2):
    return comb((x2 - x1 + y2 - y1), (x2 - x1))

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    
    index = 1
    for _ in range(t):
        x1 = int(data[index])
        y1 = int(data[index + 1])
        x2 = int(data[index + 2])
        y2 = int(data[index + 3])
        
        result = count_unique_sums(x1, y1, x2, y2)
        results.append(result)
        
        index += 4
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()