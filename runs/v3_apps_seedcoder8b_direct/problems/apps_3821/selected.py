def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    probabilities = list(map(float, data[1:n+1]))
    
    # Calculate the probability of getting exactly one problem
    # This is the sum of the product of the probability of each friend coming up with a problem
    # and the probability of the other friends not coming up with a problem.
    
    # Initialize the probability of getting exactly one problem
    prob_one_problem = 0.0
    
    # Calculate the probability of getting exactly one problem
    for i in range(n):
        # Probability that the i-th friend comes up with a problem
        p_i = probabilities[i]
        # Probability that the i-th friend does not come up with a problem
        p_not_i = 1 - p_i
        
        # Probability that all other friends do not come up with a problem
        p_others_not = 1.0
        for j in range(n):
            if j != i:
                p_others_not *= (1 - probabilities[j])
        
        # Add the contribution of this friend to the total probability
        prob_one_problem += p_i * p_others_not
    
    # Print the result with high precision
    print(f"{prob_one_problem:.12f}")

if __name__ == "__main__":
    main()