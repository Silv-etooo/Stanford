"""
    # TODO: 1. create canvas, background and character
    # TODO: 2 1. Play infinitely  2. play until wrong answer
    # TODO: 3 1. create hoops 2. hoops move 3. hopes have a question
    # TODO: 4 1. track mouse 2. check if player is inside hoop
    # TODO: 5 1. Check for correct/wrong 2. correct - count 3. wrong - game over
"""

import tkinter
import time
import random

CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 700
SIZE_PLAYER = 50
SIZE_OBSTACLE = 120
SPEED = 300


def main():

    # 1. create background and character
    canvas = draw_background()
    player = canvas.create_oval(CANVAS_WIDTH/4, CANVAS_HEIGHT/2, CANVAS_WIDTH/4 + SIZE_PLAYER, CANVAS_HEIGHT/2 + SIZE_PLAYER, fill='magenta1', outline='black')



    # 3. create hoops that have a question
    # add first hoop
    hoops = [draw_hoop(canvas)]
    generate = add_questions(canvas, hoops[0])
    text = [generate[0]]
    check = [generate[1]]

    num_of_hoops_on_canvas = 1
    points = 0
    print_points = 0

    # 2 Play until wrong answer
    while points != -1:

        # 4. mouse traction
        mouse_y = canvas.winfo_pointery() - SIZE_PLAYER
        canvas.moveto(player, CANVAS_WIDTH / 3, mouse_y)


        # 3. add second hoop
        if get_left_x(canvas, hoops[0]) < (CANVAS_WIDTH *2 /3):
            if num_of_hoops_on_canvas == 1:
                hoops.append(draw_hoop(canvas))

                generate = add_questions(canvas, hoops[1])
                text.append(generate[0])
                check.append(generate[1])

                num_of_hoops_on_canvas = 2

        # 3. add third hoop
        if get_left_x(canvas, hoops[0]) < (CANVAS_WIDTH /3):
            if num_of_hoops_on_canvas == 2:
                hoops.append(draw_hoop(canvas))

                generate = add_questions(canvas, hoops[2])
                text.append(generate[0])
                check.append(generate[1])

                num_of_hoops_on_canvas = 3

        # 3. move hoops, replace by new ones
        # 4. check if player answers correct or wrong
        #!!!
        points = action(canvas, text, hoops, check, num_of_hoops_on_canvas, mouse_y, points)

        # show points
        if points != -1:
            if int(print_points) != points:
                canvas.delete(print_points)
                print_points = canvas.create_text(65, 0, anchor='nw', font=('Helvetica', 14), text=str(points))

        # world update
        canvas.update()
        time.sleep(1/300.)

    # end subtitles
    text = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, anchor='center', font=('Helvetica', 50), text='GAME OVER')

    canvas.mainloop()


def action(canvas, text, hoops, check, num_of_hoops, mouse_y, points):

    # for every hoop
    for i in range(num_of_hoops):

        if is_hoop_in_canvas(canvas, hoops[i]):
            canvas.move(hoops[i], -1, 0)
            canvas.move(text[i], -1, 0)

            # if we have identified that a correct answer is given dont check again
            if canvas.itemcget(hoops[i], "fill") != 'greenyellow':
                # question given is correct
                if check[i] == 0:
                    points = question_is_right(canvas, text, hoops, mouse_y, i, points)

                # question given is wrong
                else:
                    points = question_is_wrong(canvas, text, hoops, mouse_y, i, points)

        # replace hoops (text, position) that go out off the canvas
        else:
            canvas.delete(hoops[i])
            del hoops[i]
            hoops.insert(i, draw_hoop(canvas))

            generate = add_questions(canvas, hoops[i])
            canvas.delete(text[i])
            del text[i]
            text.insert(i, generate[0])
            del check[i]
            check.insert(i, generate[1])

    return points


def question_is_right(canvas, text, hoops, mouse_y, i, points):
    # if the hoop is at the same x coordinate
    if (get_left_x(canvas, hoops[i]) < CANVAS_WIDTH / 3) and (
            get_left_x(canvas, hoops[i]) + SIZE_OBSTACLE > CANVAS_WIDTH / 3):

        # correct question - mouse is outside = wrong answer
        if (mouse_y > get_top_y(canvas, hoops[i]) + SIZE_OBSTACLE) or (mouse_y < get_top_y(canvas, hoops[i])):
            points = -1

        # correct question - mouse is inside = correct answer
        else:
            canvas.itemconfig(hoops[i], fill='greenyellow')
            points += 1

    return points


def question_is_wrong(canvas, text, hoops, mouse_y, i, points):
    # question is wrong - mouse is inside = wrong answer
    if (get_left_x(canvas, hoops[i]) < CANVAS_WIDTH / 3) and (
            get_left_x(canvas, hoops[i]) + SIZE_OBSTACLE > CANVAS_WIDTH / 3):
        if (mouse_y < get_top_y(canvas, hoops[i]) + SIZE_OBSTACLE) and (mouse_y > get_top_y(canvas, hoops[i])):
            points = -1

    return points


# place the question in the hoop and return whether its correct or wrong
def add_questions(canvas, hoop):
    # coordinates
    x = get_left_x(canvas, hoop) + 10
    y = get_top_y(canvas, hoop) + SIZE_OBSTACLE/2

    generation = generate_question()
    question = generation[0]
    check = generation[1]

    text = canvas.create_text(x, y, anchor='w', font=('Helvetica',14), text= str(question))
    return text, check


# return the questions and whether they are right or wrong
def generate_question():

    check = random.randint(0, 1)
    number1 = random.randrange(0, 50)
    number2 = random.randrange(0, 50)
    answer = number1 + number2
    text = (str(number1) + ' + ' + str(number2) + ' = ')

    if check == 0:
        text = text + str(answer)
    else:
        text = text + str(random.randrange(0, answer - 1))

    return text, check


def is_hoop_in_canvas(canvas, hoop):
    curr_x = get_left_x(canvas, hoop)
    return curr_x + SIZE_OBSTACLE >= 0


# draw hoop at random height
def draw_hoop(canvas):

    y_coor = random.randrange(100, CANVAS_HEIGHT)
    oval = canvas.create_oval(CANVAS_WIDTH, y_coor - 100, CANVAS_WIDTH + SIZE_OBSTACLE, y_coor - 100 + SIZE_OBSTACLE, fill="brown1")

    return oval


def draw_background():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Bouncing Ball')
    # sky
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill='slateblue4')
    # sun
    canvas.create_oval(-50,-50 , 100, 100, fill='snow')
    # grass
    canvas.create_rectangle(0, 600, CANVAS_WIDTH, CANVAS_HEIGHT, fill='darkgreen')
    # text
    canvas.create_text(5, 0, anchor='nw', font=('Helvetica', 14), text="Points: ")

    return canvas



######## These helper methods use "lists" ###########
### Which is a concept you will learn Monday ###########

def get_left_x(canvas, object):
    return canvas.coords(object)[0]

def get_top_y(canvas, object):
    return canvas.coords(object)[1]

def get_right_x(canvas, object):
    return canvas.coords(object)[2]

def get_bottom_y(canvas, object):
    return canvas.coords(object)[3]

######## DO NOT MODIFY ANY CODE BELOW THIS LINE ###########

# This function is provided to you and should not be modified.
# It creates a window that contains a drawing canvas that you
# will use to make your drawings.
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