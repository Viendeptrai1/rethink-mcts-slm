import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    
    A = data[2:2+N]
    B = data[2+N:]
    
    def matches(subimage, template):
        for i in range(len(template)):
            for j in range(len(template[0])):
                if template[i][j] == '#' and subimage[i][j] != '#':
                    return False
        return True
    
    found = False
    for i in range(N - M + 1):
        for j in range(N - M + 1):
            subimage = [A[x][j:j+M] for x in range(i, i+M)]
            if matches(subimage, B):
                found = True
                break
        if found:
            break
    
    if found:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()