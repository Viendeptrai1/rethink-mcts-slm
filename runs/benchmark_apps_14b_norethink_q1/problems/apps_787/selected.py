import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    k = int(data[0])
    q = data[1]
    
    if len(set(q)) < k:
        print("NO")
        return
    
    result = []
    used_chars = set()
    
    while q and len(result) < k:
        for i in range(len(q)):
            if q[i] not in used_chars:
                used_chars.add(q[i])
                result.append(q[i:])
                q = q[i+1:]
                break
    
    if len(result) == k:
        print("YES")
        for s in result:
            print(s)
    else:
        print("NO")

if __name__ == "__main__":
    main()