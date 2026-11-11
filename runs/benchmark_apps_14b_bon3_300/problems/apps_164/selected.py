import sys
import math

def main():
    import sys
    import math
    
    def main():
        y1, y2, yw, xb, yb, r = map(int, sys.stdin.readline().split())
        
        # Check if the ball can reach the goal directly without hitting the wall
        if yb + r > y1 and yb - r < y2:
            print("-1")
            return
        
        # Calculate the effective height of the goal
        goal_height = y2 - y1
        
        # Calculate the effective height of the wall
        wall_height = yw - y1
        
        # Calculate the effective width of the field
        field_width = xb
        
        # Calculate the effective height of the ball
        ball_height = yb - y1
        
        # Calculate the effective radius of the ball
        ball_radius = r
        
        # Calculate the effective distance from the ball to the wall
        ball_to_wall_distance = field_width
        
        # Calculate the effective distance from the ball to the goal
        ball_to_goal_distance = field_width
        
        # Calculate the effective angle of incidence
        angle_of_incidence = math.atan((goal_height / 2) / ball_to_wall_distance)
        
        # Calculate the effective angle of reflection
        angle_of_reflection = angle_of_incidence
        
        # Calculate the effective distance from the wall to the goal
        wall_to_goal_distance = ball_to_goal_distance - ball_to_wall_distance
        
        # Calculate the effective height of the ball after reflection
        ball_height_after_reflection = ball_height + 2 * ball_radius * math.sin(angle_of_reflection)
        
        # Check if the ball can reach the goal after reflection
        if ball_height_after_reflection + ball_radius > y1 and ball_height_after_reflection - ball_radius < y2:
            # Calculate the effective distance from the wall to the goal after reflection
            wall_to_goal_distance_after_reflection = wall_to_goal_distance - 2 * ball_radius * math.cos(angle_of_reflection)
            
            # Calculate the effective abscissa of the aiming point
            xw = wall_to_goal_distance_after_reflection
            
            # Print the effective abscissa of the aiming point
            print(f"{xw:.10f}")
        else:
            # Print "-1" if the ball cannot reach the goal after reflection
            print("-1")
    
    if __name__ == "__main__":
        main()