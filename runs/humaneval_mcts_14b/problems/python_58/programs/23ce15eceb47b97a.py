def common(l1: list, l2: list):
    """Return sorted unique common elements for two lists."""
    set1 = set(l1)
    set2 = set(l2)
    common_elements = set1.intersection(set2)
    return sorted(common_elements)

# Example usage:
# print(common([1, 4, 3, 34, 653, 2, 5], [5, 7, 1, 5, 9, 653, 121]))
# print(common([5, 3, 2, 8], [3, 2]))