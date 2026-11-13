def count_missed_trains(s: str) -> int:
    return s.count('1')

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(count_missed_trains(input))