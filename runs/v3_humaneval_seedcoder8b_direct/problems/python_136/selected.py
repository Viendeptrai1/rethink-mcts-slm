def largest_smallest_integers(lst):
    negatives = [x for x in lst if x < 0]
    positives = [x for x in lst if x > 0]
    
    largest_negative = max(negatives) if negatives else None
    smallest_positive = min(positives) if positives else None
    
    return (largest_negative, smallest_positive)