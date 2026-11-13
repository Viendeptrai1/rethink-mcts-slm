import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    n = int(next(iterator))
    r = int(next(iterator))
    avg = int(next(iterator))
    
    current_sum = 0
    essays_needed = 0
    
    for _ in range(n):
        a = int(next(iterator))
        b = int(next(iterator))
        current_sum += a
        
    target_sum = n * avg
    diff = target_sum - current_sum
    
    if diff <= 0:
        print(0)
        return
    
    # We need to increase the total sum by 'diff' points with minimum essays.
    # Strategy: greedily pick the exam with the smallest cost per point (smallest b_i).
    # Sort the exams based on b_i.
    
    # Since we only care about the first 10^6 values for b_i potentially? 
    # No, n is up to 10^5, sorting 10^5 items is very fast.
    
    # We need to store (b_i, a_i) to know how many points we can still raise for each exam.
    # Actually, we don't need to store a_i again if we reconstruct or just store pairs.
    # But we already consumed the input. Let's re-parse or store in a list.
    # Since we read all into input_data, we can slice it.
    
    # Re-extracting the pairs from input_data for sorting
    # The pairs start from index 2 (after n, r, avg)
    # Each pair is 2 integers.
    
    # Let's create a list of (b_i, available_points)
    # available_points = r - a_i
    
    # We need to go back to the input list.
    # Current index in input_data: we processed 3 items, then n*2 items.
    # Let's just rebuild the list of tuples from the iterator logic we had, 
    # but since we can't restart the iterator, let's slice input_data.
    
    # input_data[0] = n
    # input_data[1] = r
    # input_data[2] = avg
    # input_data[3::2] are a_i's? No.
    # Pairs are (a_i, b_i). So indices 3,4 is first pair, 5,6 second...
    
    # Let's extract efficiently
    raw_pairs = []
    idx = 3
    for _ in range(n):
        a_val = int(input_data[idx])
        b_val = int(input_data[idx+1])
        raw_pairs.append((b_val, r - a_val))
        idx += 2
        
    # Sort by cost b_i (ascending)
    raw_pairs.sort(key=lambda x: x[0])
    
    points_to_gain = diff
    
    for cost, max_points in raw_pairs:
        if points_to_gain <= 0:
            break
        take = min(points_to_gain, max_points)
        essays_needed += take * cost
        points_to_gain -= take
        
    print(essays_needed)

if __name__ == '__main__':
    solve()