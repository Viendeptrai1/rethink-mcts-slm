def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    numbers = list(map(int, data[1:]))
    
    sheet = set()
    for number in numbers:
        if number in sheet:
            sheet.remove(number)
        else:
            sheet.add(number)
    
    print(len(sheet))

if __name__ == "__main__":
    main()