def maximize_final_element():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    sequence = list(map(int, data[1:]))
    
    operations = []
    
    while len(sequence) > 1:
        if len(sequence) == 2:
            # If there are only two elements, sum them up
            operations.append(1)
            sequence = [sequence[0] + sequence[1]]
        else:
            # Check the ends of the sequence
            if sequence[0] >= sequence[-1]:
                operations.append(1)
                sequence = sequence[1:]
            else:
                operations.append(N)
                sequence = sequence[:-1]
    
    # Output the result
    print(sequence[0])
    print(len(operations))
    for op in operations:
        print(op)