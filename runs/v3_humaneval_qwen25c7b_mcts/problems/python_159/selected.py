def eat(number, need, remaining):
    total_eaten = number + min(need, remaining)
    remaining_carrots = max(remaining - need, 0)
    return [total_eaten, remaining_carrots]