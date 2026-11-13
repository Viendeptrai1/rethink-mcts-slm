def eat(number, need, remaining):
    total_eaten = number + min(need, remaining)
    carrots_left = max(remaining - need, 0)
    return [total_eaten, carrots_left]