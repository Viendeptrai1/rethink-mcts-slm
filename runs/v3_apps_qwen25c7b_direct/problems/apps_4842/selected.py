def predict_next_value():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    values = list(map(int, data[1:]))
    
    def calculate_differences(seq):
        while len(seq) > 1:
            seq = [seq[i] - seq[i-1] for i in range(1, len(seq))]
        return seq
    
    differences = calculate_differences(values)
    d = len(differences) - 1
    
    last_diff = differences[-1]
    next_value = values[-1] + last_diff
    
    print(f"{d} {next_value}")

predict_next_value()