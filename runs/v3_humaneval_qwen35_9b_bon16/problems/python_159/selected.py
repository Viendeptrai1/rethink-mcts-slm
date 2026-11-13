def eat(number, need, remaining):
    eaten_more = min(need, remaining)
    total_eaten = number + eaten_more
    left = remaining - eaten_more
    return [total_eaten, left]