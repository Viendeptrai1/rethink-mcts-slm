def main():
    import sys
    input = sys.stdin.read
    data = input().split()

    N = int(data[0])
    numbers = data[1:]

    sheet_set = set()

    for number in numbers:
        number = int(number)
        if number in sheet_set:
            sheet_set.remove(number)
        else:
            sheet_set.add(number)

    print(len(sheet_set))

if __name__ == "__main__":
    main()