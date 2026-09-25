import sys

def main():
    import sys
    n = int(sys.stdin.readline().strip())
    s = sys.stdin.readline().strip()
    t = sys.stdin.readline().strip()

    if s == t:
        if s == "aa" or s == "bb" or s == "cc":
            print("NO")
            return
        else:
            res = "a" * n + "b" * n + "c" * n
            print("YES")
            print(res)
            return

    # Try to construct the result string
    res = []
    for i in range(n):
        if i % 3 == 0:
            res.append('a')
        elif i % 3 == 1:
            res.append('b')
        else:
            res.append('c')

    # Check if s or t is a substring
    res_str = ''.join(res)
    if s in res_str or t in res_str:
        # Try another pattern
        res = []
        for i in range(n):
            if i % 3 == 0:
                res.append('b')
            elif i % 3 == 1:
                res.append('c')
            else:
                res.append('a')

        res_str = ''.join(res)
        if s in res_str or t in res_str:
            # Try another pattern
            res = []
            for i in range(n):
                if i % 3 == 0:
                    res.append('c')
                elif i % 3 == 1:
                    res.append('a')
                else:
                    res.append('b')

            res_str = ''.join(res)
            if s in res_str or t in res_str:
                print("NO")
                return

    print("YES")
    print(res_str)

if __name__ == "__main__":
    main()