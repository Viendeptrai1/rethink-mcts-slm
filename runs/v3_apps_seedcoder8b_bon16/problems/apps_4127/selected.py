def compute_truncated_product():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    A = int(data[0])
    B = float(data[1])
    result = A * B
    truncated_result = int(result)
    print(truncated_result)

compute_truncated_product()