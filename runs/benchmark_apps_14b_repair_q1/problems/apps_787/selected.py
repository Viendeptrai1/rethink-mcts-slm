import sys

def main():
    import sys
    k = int(sys.stdin.readline().strip())
    q = sys.stdin.readline().strip()
    
    if len(q) < k:
        print("NO")
        return
    
    # Check if we can have distinct starting characters
    if len(set(q[:k])) != k:
        print("NO")
        return
    
    # Create the sequence
    sequence = []
    for i in range(k):
        sequence.append(q[i])
    
    # Distribute the remaining characters
    remaining = q[k:]
    for i in range(len(remaining)):
        sequence[i % k] += remaining[i]
    
    print("YES")
    for s in sequence:
        print(s)

if __name__ == "__main__":
    main()