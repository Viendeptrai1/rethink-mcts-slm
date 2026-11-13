def decrypt_repeating_cipher():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    t = data[1]
    
    result = []
    index = 0
    
    for i in range(1, n + 1):
        if index < n and t[index] == t[index + i - 1]:
            result.append(t[index])
            index += i
    
    print("".join(result))

decrypt_repeating_cipher()