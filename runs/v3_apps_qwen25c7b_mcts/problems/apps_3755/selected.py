import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
A = list(map(int, data[1:]))

# Initialize variables
max_value = float('-inf')
best_operations = []
best_sequence = []

def dfs(sequence, operations):
    global max_value, best_operations, best_sequence
    
    if len(sequence) == 1:
        if sequence[0] > max_value:
            max_value = sequence[0]
            best_operations = operations[:]
            best_sequence = sequence[:]
        return
    
    # Try deleting each element
    for i in range(len(sequence)):
        new_sequence = sequence[:i] + sequence[i+1:]
        
        # If the element is at either end, just delete it
        if i == 0 or i == len(sequence) - 1:
            dfs(new_sequence, operations + [i + 1])
        else:
            # Replace the element with the sum of its neighbors
            new_element = sequence[i-1] + sequence[i+1]
            new_sequence.insert(i, new_element)
            dfs(new_sequence, operations + [i + 1])

dfs(A, [])

print(max_value)
print(len(best_operations))
for op in best_operations:
    print(op)