import sys

def solve():
    try:
        lines = sys.stdin.read().splitlines()
        if not lines:
            return
        try:
            n = int(lines[0].strip())
        except ValueError:
            return
        s = lines[1] if len(lines) > 1 else ""
        # Ensure we only consider the first n characters if provided
        s = s[:n]
        
        stack = []
        pairs = {')': '(', ']': '[', '}': '{'}
        
        for i, char in enumerate(s):
            if char in '([{':
                stack.append(char)
            elif char in ')]}':
                if not stack:
                    print(f"{char} {i}")
                    return
                top = stack.pop()
                if pairs[char] != top:
                    print(f"{char} {i}")
                    return
            # Spaces are ignored
        
        print("ok so far")
    except Exception:
        pass

if __name__ == "__main__":
    solve()