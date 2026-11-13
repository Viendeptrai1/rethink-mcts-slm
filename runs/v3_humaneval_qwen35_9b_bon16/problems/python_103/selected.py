def rounded_avg(n, m):
    if n > m:
        return -1
    total = (n + m) * (m - n + 1) // 2
    avg = total / (m - n + 1)
    rounded = round(avg)
    return bin(rounded)