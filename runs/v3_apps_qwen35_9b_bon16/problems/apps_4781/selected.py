import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        k = int(next(iterator))
        n = int(next(iterator))
    except StopIteration:
        return
    
    total_time = 3 * 60 + 30  # 3 minutes and 30 seconds in seconds
    
    current_player = k
    time_elapsed = 0
    
    for _ in range(n):
        try:
            t = int(next(iterator))
            z = next(iterator)
        except StopIteration:
            break
        
        time_elapsed += t
        
        if time_elapsed >= total_time:
            print(current_player)
            return
        
        if z == 'T':
            # Pass to the left (next player in circle)
            current_player = (current_player % 8) + 1

if __name__ == "__main__":
    solve()