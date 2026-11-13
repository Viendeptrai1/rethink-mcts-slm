def max_power_discharge(M, S, steps):
    result = []
    current_power = 1
    max_power = 1
    
    for step in steps:
        if step == '+':
            next_power = (current_power + 1) % (2 ** S)
            if next_power > max_power:
                max_power = next_power
                result.append(step)
            else:
                result.append('o')
            current_power = next_power
        elif step == 'x':
            next_power = (current_power * 2) % (2 ** S)
            if next_power > max_power:
                max_power = next_power
                result.append(step)
            else:
                result.append('o')
            current_power = next_power
        else:
            result.append('o')
    
    return ''.join(result)

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    M = int(data[0])
    S = int(data[1])
    steps = data[2]
    print(max_power_discharge(M, S, steps))