def find_polynomial_degree_and_next_value():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    n = int(data[0])
    values = list(map(int, data[1:n+1]))
    
    def compute_differences(seq):
        return [seq[i+1] - seq[i] for i in range(len(seq) - 1)]
    
    def is_constant(seq):
        return all(x == seq[0] for x in seq)
    
    differences = values
    degree = 0
    
    while not is_constant(differences) and len(differences) > 1:
        differences = compute_differences(differences)
        degree += 1
    
    # Calculate the next value in the sequence
    if degree == 0:
        # Linear sequence, constant difference
        next_value = values[-1] + (values[-1] - values[-2])
    else:
        # Use the differences to predict the next value
        next_value = values[-1]
        for i in range(degree):
            next_value += differences[i]
    
    print(degree, next_value)