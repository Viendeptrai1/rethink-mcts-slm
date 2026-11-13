def minimum_rolls_to_score(x):
    # The set of possible scores on one dice roll
    dice_values = {2, 3, 4, 5, 6, 7}
    
    # The answer is the smallest number of rolls required to sum up to exactly x
    # We can achieve this using a greedy approach: always try to use the largest dice value
    rolls = 0
    while x > 0:
        for value in sorted(dice_values, reverse=True):
            if value <= x:
                x -= value
                rolls += 1
                break
    return rolls

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    results = []
    for i in range(1, t + 1):
        x = int(data[i])
        results.append(minimum_rolls_to_score(x))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()