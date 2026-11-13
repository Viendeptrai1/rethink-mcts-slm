from collections import Counter

def same_chars(s0: str, s1: str) -> bool:
    return Counter(s0) == Counter(s1)