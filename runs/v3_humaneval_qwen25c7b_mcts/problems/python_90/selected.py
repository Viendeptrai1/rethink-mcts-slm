import heapq

def next_smallest(lst):
    unique_elements = set(lst)
    if len(unique_elements) < 2:
        return None
    smallest, second_smallest = heapq.nsmallest(2, unique_elements)
    return second_smallest