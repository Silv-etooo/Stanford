"""
File: brickbreaker.py
----------------
play the brickbeaker game

2 problems not solved.
"""

import tkinter
import time
import random

# How big is the playing area?
CANVAS_WIDTH = 600      # Width of drawing canvas in pixels
CANVAS_HEIGHT = 700     # Height of drawing canvas in pixels

# Constants for the bricks
N_ROWS = 8              # How many rows of bricks are there?
N_COLS = 10             # How many columns of bricks are there?
SPACING = 5             # How much space is there between each brick?
BRICK_START_Y = 50      # The y coordinate of the top-most brick
BRICK_HEIGHT = 20       # How many pixels high is each brick
BRICK_WIDTH = (CANVAS_WIDTH - (N_COLS+1) * SPACING ) / N_COLS

# Constants for the ball and paddle
BALL_SIZE = 20
PADDLE_Y = CANVAS_HEIGHT - 40
PADDLE_WIDTH = 80

# base x and y change value
CHANGE_X = -5
CHANGE_Y = 10


def main():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Brick Breaker')

    # create objects in the game
    bricks = create_bricks(canvas)
    ball = create_ball(canvas)
    paddle = create_paddle(canvas)

    # value by which the ball will move in x and y direction
    change_x = CHANGE_X
    change_y = CHANGE_Y

    # lifes
    Life = 3

    # animation
    while Life != 0:
        # move ball
        canvas.move(ball, change_x, change_y)

        # ball stay inside canvas
        location = is_ball_inside(canvas, ball, change_x, change_y)
        change_x = location[0]
        change_y = location[1]

        # move paddle
        mouse_x = canvas.winfo_pointerx()
        canvas.moveto(paddle, mouse_x, PADDLE_Y)

        # ball collide?
        #   with paddle _> change magnitude of change_x.
        #   with bricks -> remove bricks
        change = did_ball_collide(canvas, ball, paddle, change_y, change_x, bricks)
        change_x = change[0]
        change_y = change[1]

        # Lifes - decrease n of lifes, set pre-conditions
        if change_y == 0:
            Life -= 1
            if Life != 0:
                canvas.moveto(ball,CANVAS_WIDTH/2 - BALL_SIZE/2, CANVAS_HEIGHT/2 - BALL_SIZE/2)
                change_x = CHANGE_X
                change_y = CHANGE_Y


        # Update frames
        canvas.update()
        time.sleep(1 / 30.)

    # Game over
    canvas.delete(ball)
    canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2 , anchor='n', font='Times', text='ГАМЕ ОВЕР')
    canvas.mainloop()



def did_ball_collide(canvas, ball, paddle, change_y, change_x, bricks):
    x = get_left_x(canvas, ball)
    y = get_top_y(canvas, ball)

    overlap_items = canvas.find_overlapping(x, y, x + BALL_SIZE, y + BALL_SIZE)

    for item in overlap_items:
        # depending on where the ball hit the paddle change_x is different

        if item == paddle and change_y > 0:
            change_y *= -1
            change_x = magnitude_of_change_x(canvas, ball, paddle, change_x)
            return change_x, change_y

        for itemb in bricks:
            if item == itemb:

                xb = get_left_x(canvas, itemb)
                if abs(x + BALL_SIZE - xb) <=20 or abs(x - xb + BRICK_WIDTH) <= 20:
                    change_x *= -1
                    canvas.delete(itemb)
                    return change_x, change_y


                print(change_y)
                change_y *= -1
                canvas.delete(itemb)
                return change_x, change_y



    return change_x, change_y

# depending on location where the ball hit the paddle the magnitude of change_x is different
def magnitude_of_change_x(canvas, ball, paddle, change_x):
    middle_ball = canvas.coords(ball)[0]+BALL_SIZE/2
    middle_paddle = canvas.coords(paddle)[0]+PADDLE_WIDTH/2

    if middle_paddle-middle_ball > 0:
        change_x = 1*CHANGE_X*(1+(middle_paddle-middle_ball)/100)
    else:
        change_x = -1*CHANGE_X*(1+(middle_ball-middle_paddle)/100)

    return change_x

# makes ball stay inside canvas
def is_ball_inside(canvas, ball, change_x, change_y):
    # is it out from right or left of canvas
    if get_left_x(canvas, ball) < 0 or get_left_x(canvas, ball) + BALL_SIZE > CANVAS_WIDTH:
        change_x *= -1
    # is it out from top or bottom
    else:
        # top
        if get_top_y(canvas, ball) < 0 :
            change_y *= -1

        # bottom = endgame
        else:
            if get_top_y(canvas, ball) + BALL_SIZE > CANVAS_HEIGHT:
                change_y = 0

    return change_x, change_y

# creates paddle
def create_paddle(canvas):
    paddle = canvas.create_rectangle(CANVAS_WIDTH/2-40, PADDLE_Y , CANVAS_WIDTH/2 + 40, PADDLE_Y+20 , fill='black')
    return paddle

# creates ball that will move around
def create_ball(canvas):
    ball = canvas.create_oval(CANVAS_WIDTH/2 - BALL_SIZE/2, CANVAS_HEIGHT/2 - BALL_SIZE/2 , CANVAS_WIDTH/2 + BALL_SIZE/2, CANVAS_HEIGHT/2 + BALL_SIZE/2, fill='black')
    return ball

# creates the brinks that have to be destroyed by player
def create_bricks(canvas):
    # add the bricks
    # color them

    bricks = []

    for i in range(N_COLS):
        for j in range(N_ROWS):
            x = i * (BRICK_WIDTH + SPACING)
            y = BRICK_START_Y + j * (BRICK_HEIGHT + SPACING)

            color = color_of_brick(j)

            bricks.append(canvas.create_rectangle(x, y, x + BRICK_WIDTH, y + BRICK_HEIGHT, fill=color, outline='black'))

    return bricks

#adds color to bricks
def color_of_brick(i):
    switcher = {
        0: 'purple1',
        1: 'deep sky blue',
        2: 'lawn green',
        3: 'yellow',
        4: 'DarkOrange1',
        5: 'OrangeRed2',
        6: 'red3',
        7: 'maroon2',
    }
    return switcher.get(i)

def get_top_y(canvas, object):
    '''
    This friendly method returns the y coordinate of the top of an object.
    Recall that canvas.coords(object) returns a list of the object 
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 1 is the top-y
    '''
    return canvas.coords(object)[1]

def get_left_x(canvas, object):
    '''
    This friendly method returns the x coordinate of the left of an object.
    Recall that canvas.coords(object) returns a list of the object 
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 0 is the left-x
    '''
    return canvas.coords(object)[0]

def make_canvas(width, height, title):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas

if __name__ == '__main__':
    main()
