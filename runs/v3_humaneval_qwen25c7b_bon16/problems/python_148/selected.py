def bf(planet1, planet2):
    planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
    
    try:
        index1 = planets.index(planet1)
        index2 = planets.index(planet2)
    except ValueError:
        return ()
    
    start_index = min(index1, index2) + 1
    end_index = max(index1, index2)
    
    return tuple(planets[start_index:end_index])