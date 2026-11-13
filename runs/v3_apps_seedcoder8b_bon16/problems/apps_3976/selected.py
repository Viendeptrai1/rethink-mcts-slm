def find_valid_qs(n, m, p, a, b):
    from collections import Counter
    
    # Count the frequency of elements in sequence b
    b_count = Counter(b)
    b_values = sorted(b_count.keys())
    b_size = len(b_values)
    
    # Function to check if a subarray can be rearranged to form b
    def can_form_b(start):
        sub_count = Counter(a[start:start + m * p:p])
        return all(sub_count[b_val] == b_count[b_val] for b_val in b_values)
    
    valid_qs = []
    
    # Iterate through valid q positions
    for q in range(1, n - (m - 1) * p + 2):
        if can_form_b(q - 1):
            valid_qs.append(q)
    
    return valid_qs

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    p = int(data[2])
    a = list(map(int, data[3:3 + n]))
    b = list(map(int, data[3 + n:3 + n + m]))
    
    valid_qs = find_valid_qs(n, m, p, a, b)
    
    print(len(valid_qs))
    if valid_qs:
        print(' '.join(map(str, valid_qs)))

if __name__ == "__main__":
    main()