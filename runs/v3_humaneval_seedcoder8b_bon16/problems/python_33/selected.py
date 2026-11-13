def sort_third(l: list):
    third_elements = [l[i] for i in range(len(l)) if i % 3 == 0]
    third_elements.sort()
    
    result = l.copy()
    third_index = 0
    for i in range(len(l)):
        if i % 3 == 0:
            result[i] = third_elements[third_index]
            third_index += 1
    
    return result