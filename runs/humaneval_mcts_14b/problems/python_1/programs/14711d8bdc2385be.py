from typing import List

def separate_paren_groups(paren_string: str) -> List[str]:
    def find_next_group(s: str, start: int) -> int:
        balance = 0
        for i in range(start, len(s)):
            if s[i] == '(':
                balance += 1
            elif s[i] == ')':
                balance -= 1
            if balance == 0:
                return i
        return -1

    def helper(s: str, start: int, result: List[str]) -> None:
        if start >= len(s):
            return
        end = find_next_group(s, start)
        if end != -1:
            result.append(s[start:end+1])
            helper(s, end + 1, result)

    result = []
    helper(paren_string.replace(' ', ''), 0, result)
    return result