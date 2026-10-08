import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    k = int(data[0])
    q = data[1]
    
    if len(q) < k:
        print("NO")
        return
    
    used_chars = set()
    result = []
    
    for i in range(k):
        if i == k - 1:
            result.append(q[i:])
        else:
            for j in range(1, len(q) - i):
                if q[i] not in used_chars:
                    used_chars.add(q[i])
                    result.append(q[i:i+j])
                    q = q[i+j:]
                    break
            else:
                print("NO")
                return
    
    print("YES")
    for s in result:
        print(s)

if __name__ == "__main__":
    main()