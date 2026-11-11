import sys
import math

def main():
    import sys
    import math

    def main():
        y1, y2, yw, xb, yb, r = map(int, sys.stdin.readline().split())

        # Calculate the effective height of the goal
        goal_height = y2 - y1

        # Calculate the effective height of the wall
        wall_height = yw - y1

        # Calculate the effective width of the field
        field_width = xb

        # Calculate the effective height of the ball position
        ball_height = yb - y1

        # Calculate the effective radius of the ball
        ball_radius = r

        # Calculate the effective distance from the ball to the wall
        ball_to_wall_distance = field_width

        # Calculate the effective distance from the ball to the goal
        ball_to_goal_distance = 0

        # Calculate the effective angle of incidence
        angle_of_incidence = math.atan((ball_height - wall_height / 2) / ball_to_wall_distance)

        # Calculate the effective angle of reflection
        angle_of_reflection = angle_of_incidence

        # Calculate the effective distance from the wall to the goal
        wall_to_goal_distance = math.sqrt((wall_height / 2 - ball_height) ** 2 + ball_to_wall_distance ** 2)

        # Calculate the effective distance from the ball to the point of reflection
        ball_to_reflection_distance = wall_to_goal_distance * math.cos(angle_of_reflection)

        # Calculate the effective distance from the point of reflection to the goal
        reflection_to_goal_distance = wall_to_goal_distance * math.sin(angle_of_reflection)

        # Calculate the effective abscissa of the point of aiming
        xw = ball_to_reflection_distance

        # Check if the ball will hit the goal post
        if reflection_to_goal_distance < ball_radius or reflection_to_goal_distance > goal_height - ball_radius:
            print("-1")
        else:
            print(xw)

    if __name__ == "__main__":
        main()