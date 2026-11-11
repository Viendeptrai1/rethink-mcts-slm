import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    K = int(data[0])
    N = int(data[1])
    
    index = 2
    current_player = K
    
    for _ in range(N):
        T = int(data[index])
        Z = data[index + 1]
        index += 2
        
        if Z == 'T':
            current_player = (current_player % 8) + 1
    
    print(current_player)

if __name__ == "__main__":
    main()