import sys
from typing import List

def bachgold_problem(n: int) -> List[int]:
    if n <= 2:
        return [n]
    elif n % 2 == 0:
        return [2] * (n // 2)
    else:
        return [2] * ((n - 3) // 2) + [3]

if __name__ == "__main__":
    n = int(sys.stdin.read().strip())
    result = bachgold_problem(n)
    print(len(result))
    print(*result)