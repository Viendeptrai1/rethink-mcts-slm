def determine_winner(n, sequence):
    total_sum = sum(sequence)
    min_value = min(sequence)
    
    if total_sum % 2 == 0:
        return "BitLGM"
    else:
        return "BitAryo"

if __name__ == "__main__":
    n = int(input())
    sequence = list(map(int, input().split()))
    print(determine_winner(n, sequence))