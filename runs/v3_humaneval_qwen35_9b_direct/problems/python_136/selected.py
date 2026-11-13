def largest_smallest_integers(lst):
    negatives = [x for x in lst if x < 0]
    positives = [x for x in lst if x > 0]
    
    if not negatives:
        a = None
    else:
        a = max(negatives)
    
    if not positives:
        b = None
    else:
        b = min(positives)
    
    return (a, b)