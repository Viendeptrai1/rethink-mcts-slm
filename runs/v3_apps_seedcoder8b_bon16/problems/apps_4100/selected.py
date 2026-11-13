def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    Q = int(data[2])
    A = list(map(int, data[3:3+Q]))
    
    scores = [K] * N
    
    for answer in A:
        answer -= 1  # Convert 1-based index to 0-based index
        for i in range(N):
            if i != answer:
                scores[i] -= 1
    
    for score in scores:
        if score > 0:
            print("Yes")
        else:
            print("No")

if __name__ == "__main__":
    main()