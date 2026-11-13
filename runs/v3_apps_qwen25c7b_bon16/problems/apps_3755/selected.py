import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    seq = list(map(int, data[1:]))
    
    # To maximize the final element, we should always choose the middle element
    # because replacing it with the sum of its neighbors will generally increase the value.
    # We need to perform N-1 operations to reduce the sequence to one element.
    
    max_value = seq[N // 2]
    operations = []
    
    while len(seq) > 1:
        mid_index = len(seq) // 2
        max_value += seq[mid_index]
        operations.append(mid_index + 1)
        
        # Remove the middle element and merge its neighbors
        if mid_index == 0:
            seq = [seq[1]]
        elif mid_index == len(seq) - 1:
            seq = [seq[-2]]
        else:
            new_element = seq[mid_index - 1] + seq[mid_index + 1]
            seq = seq[:mid_index - 1] + [new_element] + seq[mid_index + 2:]
    
    print(max_value)
    print(len(operations))
    for op in operations:
        print(op)

solve()