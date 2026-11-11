def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    numbers = list(map(int, data[1:]))
    
    written_numbers = set()
    
    for number in numbers:
        if number in written_numbers:
            written_numbers.remove(number)
        else:
            written_numbers.add(number)
    
    print(len(written_numbers))

if __name__ == "__main__":
    main()