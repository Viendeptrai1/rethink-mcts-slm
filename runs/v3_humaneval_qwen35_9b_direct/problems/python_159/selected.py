def eat(number, need, remaining):
    eaten = number
    left = remaining
    
    if need > 0:
        to_eat = min(need, left)
        eaten += to_eat
        left -= to_eat
    
    return [eaten, left]