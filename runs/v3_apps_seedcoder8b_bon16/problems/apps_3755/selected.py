def solve():
    N = int(input())
    seq = list(map(int, input().split()))
    
    operations = []
    while len(seq) > 1:
        if len(seq) == 2:
            operations.append(1)
            break
        
        max_value = float('-inf')
        max_index = -1
        
        for i in range(len(seq)):
            if i == 0 or i == len(seq) - 1:
                value = seq[i]
            else:
                value = seq[i-1] + seq[i+1]
            
            if value > max_value:
                max_value = value
                max_index = i
        
        if max_index == 0:
            seq.pop(0)
            operations.append(1)
        elif max_index == len(seq) - 1:
            seq.pop()
            operations.append(max_index + 1)
        else:
            new_value = seq[max_index-1] + seq[max_index+1]
            seq[max_index-1] = new_value
            seq.pop(max_index)
            seq.pop(max_index)
            operations.append(max_index + 1)
    
    print(seq[0])
    print(len(operations))
    for op in operations:
        print(op)

solve()