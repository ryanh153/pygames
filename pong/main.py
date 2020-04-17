import turtle
import winsound
import time
from datetime import datetime
import random

# game params
max_score = 7
init_vx = 200
init_vy = 200
vx_inc = 8
vy_inc = 6
speedup_inc = 5

# window
wn = turtle.Screen()
wn.title("pong")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)  # stop from updating itself

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)  # this is max? Not for movement for animation (draw)
paddle_a.shape("square")  # default is 20x20 px
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()  # don't draw
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)  # this is max? Not for movement for animation (draw)
paddle_b.shape("square")  # default is 20x20 px
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()  # don't draw
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)  # this is max? Not for movement for animation (draw)
ball.shape("square")  # default is 20x20 px
ball.color("white")
ball.penup()  # don't draw
ball.goto(0, 0)
ball.dx = init_vx*random.choice([1, -1])  # balls speed in px/sec
ball.dy = init_vy*random.choice([1, -1])  # starts in a random direction

# Score
score_a = 0
score_b = 0

# draw boundaries and middle line
bpen = turtle.Turtle()
bpen.speed(0)
bpen.color("white")
bpen.hideturtle()
bpen.penup()
bpen.goto(-390, 255)
bpen.width(10)
bpen.pendown()
bpen.goto(390, 255)
bpen.goto(390, -290)
bpen.goto(-390, -290)
bpen.goto(-390, 255)
bpen.penup()
bpen.goto(0, 255)
bpen.pendown()
bpen.goto(0, -290)

# score
spen = turtle.Turtle()
spen.speed(0)
spen.color("white")
spen.penup()
spen.hideturtle()
spen.goto(0, 260)
spen.write(f"Player A: {score_a} Player B: {score_b}", align="center", font=("Courier", 24, "normal"))


# Functions

def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)

def update_score():
    spen.clear()
    spen.write(f"Player A: {score_a} Player B: {score_b}", align="center", font=("Courier", 24, "normal"))
    ball.goto(0, 0)
    ball.dx = init_vx*random.choice([1, -1])
    ball.dy = init_vy*random.choice([1, -1])

def coll_sound():
    winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

def sign(num): return 1 if num >= 0 else -1

def speed_up(vx, vy):
    vx += vx_inc*sign(vx)*random.uniform(0.25, 0.75,)
    vy += vy_inc*sign(vy)*random.uniform(0.25, 0.75)
    return datetime.now(), vx, vy


# Key bindings

wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")


# Main game loop
game_won = False
prev_time = datetime.now()
last_speed_up = datetime.now()
while not game_won:
    wn.update()  # this is what updates
    dt = (datetime.now() - prev_time).total_seconds()
    if (datetime.now() - last_speed_up).total_seconds() > 3:
        last_speed_up, ball.dx, ball.dy = speed_up(ball.dx, ball.dy)

    prev_time = datetime.now()

    # move the ball
    ball.setx(ball.xcor() + ball.dx*dt)
    ball.sety(ball.ycor() + ball.dy*dt)

    # Border checking
    if ball.ycor() > 240:
        ball.sety(240)
        ball.dy *= -1
        coll_sound()

    if ball.ycor() < -275:
        ball.sety(-275)
        ball.dy *= -1
        coll_sound()

    if ball.xcor() > 375:
        ball.setx(375)
        ball.dx *= -1
        score_a += 1
        update_score()
        coll_sound()

    if ball.xcor() < -375:
        ball.setx(-375)
        ball.dx *= -1
        score_b += 1
        update_score()
        coll_sound()

    if paddle_a.ycor() > 200:
        paddle_a.sety(200)
    elif paddle_a.ycor() < -235:
        paddle_a.sety(-235)

    if paddle_b.ycor() > 200:
        paddle_b.sety(200)
    elif paddle_b.ycor() < -235:
        paddle_b.sety(-235)

    # paddle collision checking
    if (ball.xcor() < -330) and (abs(ball.ycor() - paddle_a.ycor()) < 60):
        ball.setx(paddle_a.xcor()+21)
        ball.dx *= -1
        coll_sound()

    if (ball.xcor() > 330) and (abs(ball.ycor() - paddle_b.ycor()) < 60):
        ball.setx(paddle_b.xcor()-21)
        ball.dx *= -1
        coll_sound()

    if score_a == max_score or score_b == max_score:
        game_won = True


spen.clear()
if score_a > score_b:
    spen.write(f"Player A Wins!", align="center", font=("Courier", 24, "normal"))
else:
    spen.write(f"Player A Wins!", align="center", font=("Courier", 24, "normal"))


winsound.PlaySound("fanfare.wav", winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
time.sleep(1.05)
winsound.PlaySound(None, winsound.SND_FILENAME)
time.sleep(3)
