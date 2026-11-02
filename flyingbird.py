
import turtle
import random

# Screen setup
screen = turtle.Screen()
screen.title("Flappy Bird - Python") 
screen.setup(600, 600)
screen.bgcolor("skyblue")
screen.tracer(0)

# Bird
bird = turtle.Turtle()
bird.shape("circle")
bird.color("black")
bird.penup()
bird.goto(-150, 0)

velocity = 0
gravity = -0.5
game_over = False
score = 0

# Pipes
pipes = []

def create_pipe():
    gap_y = random.randint(-100, 150)

    top = turtle.Turtle()
    top.shape("circle")
    top.color("green")
    top.penup()
    top.shapesize(stretch_wid=10, stretch_len=2)
    top.goto(300, gap_y + 200)

    bottom = turtle.Turtle()
    bottom.shape("circle")
    bottom.color("orange")
    bottom.penup()
    bottom.shapesize(stretch_wid=10, stretch_len=2)
    bottom.goto(300, gap_y - 200)

    pipes.append([top, bottom, False])

create_pipe()

# Score display
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.color("black")
pen.goto(0, 250)

def show_score():
    pen.clear()
    pen.write(
        f"Score: {score}",
        align="center",
        font=("Arial", 20, "bold")
    )

show_score()

# Game over message
message = turtle.Turtle()
message.hideturtle()
message.penup()
message.color("red")

def jump():
    global velocity, game_over

    if game_over:
        restart()
    else:
        velocity = 7

def restart():
    global velocity, score, game_over, pipes

    for pair in pipes:
        pair[0].hideturtle()
        pair[1].hideturtle()

    pipes.clear()
    bird.goto(-150, 0)
    velocity = 0
    score = 0
    game_over = False
    message.clear()
    create_pipe()
    show_score()

# Controls
screen.listen()
screen.onkeypress( jump, "space")

def game_loop():
    global velocity, score, game_over

    if not game_over:
        velocity += gravity
        bird.sety(bird.ycor() + velocity)

        # Create new pipes
        if pipes[-1][0].xcor() < 100:
            create_pipe()

        for pair in pipes:
            top, bottom, passed = pair

            top.setx(top.xcor() - 3)
            bottom.setx(bottom.xcor() - 3)

            # Collision detection
            if (bird.distance(top) < 35 or
                    bird.distance(bottom) < 35):
                if abs(bird.xcor() - top.xcor()) < 30:
                    if (bird.ycor() > bottom.ycor() + 100 or
                            bird.ycor() < top.ycor() - 100):
                        game_over = True

            # Score
            if not passed and top.xcor() < bird.xcor():
                pair[2] = True
                score += 1
                show_score()

        # Remove old pipes
        while pipes and pipes[0][0].xcor() < -350:
            old = pipes.pop(0)
            old[0].hideturtle()
            old[1].hideturtle()

        # Ceiling and ground
        if bird.ycor() > 280 or bird.ycor() < -280:
            game_over = True

        if game_over:
            message.goto(0, 30)
            message.write(
                "GAME OVER!" \
                " @MILAN YADAV",
                align="center",
                font=("Arial", 22, "bold")
            )
            message.goto(0, -20)
            message.write(
                "Press SPACE to restart",
                align="center",
                font=("Arial", 15, "bold")
            )

    screen.update()
    screen.ontimer(game_loop, 20)

game_loop()
screen.mainloop()