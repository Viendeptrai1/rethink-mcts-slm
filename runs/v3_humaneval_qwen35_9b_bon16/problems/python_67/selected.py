def fruit_distribution(s, n):
    # Extract the number of apples
    apple_count = 0
    if 'apples' in s:
        apple_str = s.split(' apples')[0]
        if apple_str:
            apple_count = int(apple_str)
        else:
            apple_count = 0
    else:
        apple_count = 0

    # Extract the number of oranges
    orange_count = 0
    if 'oranges' in s:
        orange_str = s.split(' oranges')[0]
        # Remove the 'and ' part if present before the number
        if 'and' in orange_str:
            orange_str = orange_str.split('and ')[1]
        else:
            orange_str = orange_str.strip()
        if orange_str:
            orange_count = int(orange_str)
        else:
            orange_count = 0
    else:
        orange_count = 0

    # Calculate mango count
    mango_count = n - apple_count - orange_count
    return mango_count