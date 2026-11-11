import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    Q = int(data[2])
    
    scores = [K] * N
    
    index = 3
    for _ in range(Q):
        A_i = int(data[index]) - 1
        for i in range(N):
            if i != A_i:
                scores[i] -= 1
        index += 1
    
    for score in scores:
        if score > 0:
            print("Yes")
        else:
            print("No")

if __name__ == "__main__":
    main()