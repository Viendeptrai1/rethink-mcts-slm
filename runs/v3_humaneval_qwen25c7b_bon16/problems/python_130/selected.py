def tri(n):
    if n == 0:
        return [1]
    elif n == 1:
        return [1, 3]
    
    tribonacci = [1, 3]
    for i in range(2, n + 1):
        if i % 2 == 0:
            tribonacci.append(1 + i / 2)
        else:
            next_value = tribonacci[i-1] + tribonacci[i-2] + tribonacci[i+1] if i < n else tribonacci[i-1] + tribonacci[i-2] + 3
            tribonacci.append(next_value)
    
    return tribonacci