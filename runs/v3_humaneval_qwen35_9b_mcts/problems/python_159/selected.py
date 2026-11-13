def eat(number, need, remaining):
    eaten = min(need, remaining)
    total_eaten = number + eaten
    left = remaining - eaten
    return [total_eaten, left]