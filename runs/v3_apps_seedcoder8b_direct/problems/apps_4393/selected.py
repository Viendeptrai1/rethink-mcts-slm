def decrypt_repeating_cipher():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    n = int(data[0])
    t = data[1]
    
    s = []
    index = 0
    
    for i in range(1, n + 1):
        # Calculate the length of the current segment
        segment_length = i
        
        # Extract the segment from the encrypted string
        segment = t[index:index + segment_length]
        
        # Check if the segment is repeated i times
        if segment * i == t[index:index + segment_length * i]:
            s.append(segment[0])
            index += segment_length * i
    
    print(''.join(s))