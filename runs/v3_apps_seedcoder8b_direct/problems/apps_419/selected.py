def count_missed_trains(s: str) -> int:
    # Convert the binary string to an integer
    s = int(s, 2)
    
    # Initialize the count of missed trains
    missed_trains = 0
    
    # Initialize the time of the first train
    train_time = 1
    
    # Iterate over each power of 4
    while train_time < s:
        missed_trains += 1
        train_time *= 4
    
    return missed_trains

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(count_missed_trains(input))