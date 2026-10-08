def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    numbers = data[1:]
    
    sheet = set()
    
    for num in numbers:
        if num in sheet:
            sheet.remove(num)
        else:
            sheet.add(num)
    
    print(len(sheet))

if __name__ == "__main__":
    main()