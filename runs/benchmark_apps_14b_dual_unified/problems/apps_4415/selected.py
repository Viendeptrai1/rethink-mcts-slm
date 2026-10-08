import sys
import bisect

def main():
    import sys
    import bisect

    def readints():
        return list(map(int, sys.stdin.read().split()))

    data = readints()
    n = data[0]
    a = data[1:]

    # Sort the array
    sorted_a = sorted(a)

    # Try to partition the sorted array into two sequences
    inc = []
    dec = []

    for num in sorted_a:
        if not inc or num > inc[-1]:
            inc.append(num)
        elif not dec or num > dec[-1]:
            dec.append(num)
        else:
            print("NO")
            return

    # Check if the union of inc and dec is a permutation of a
    if len(inc) + len(dec) != n:
        print("NO")
        return

    # Print the result
    print("YES")
    print(len(inc))
    print(" ".join(map(str, inc)))
    print(len(dec))
    print(" ".join(map(str, dec)))

if __name__ == "__main__":
    main()