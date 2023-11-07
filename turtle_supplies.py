from turtle import *
from random import randrange, choice



# GENERAL DRAWING FUNCTIONS

def get_state():
    return(pos(), heading(), pen())

def restore_state(state):
    penup()
    setx(state[0][0])
    sety(state[0][1])
    seth(state[1])
    pen(state[2])

def hop(dx, dy):
    penup()
    fd(dy)
    rt(90)
    fd(dx)
    lt(90)
    pendown()

def rectangle_empty(height, width, col, size):
    state = get_state()
    color(col)
    pensize(size)
    for i in range(2):
        fd(height)
        rt(90)
        fd(width)
        rt(90)
    restore_state(state)

def rectangle_full(height, width, col):
    state = get_state()
    color(col, col)
    begin_fill()
    for i in range(2):
        fd(height)
        rt(90)
        fd(width)
        rt(90)
    end_fill()
    restore_state(state)



# DRAWING JARS

def draw_circle(x):
    hop(x, x/2)
    color("black", "black")
    begin_fill()
    circle(x)
    end_fill()

def draw_star(cabinet_w):
    color("black")
    begin_fill()
    for i in range(9):
        fd(cabinet_w)
        lt(200)
    end_fill()

def draw_label(kind, x):
    if kind == "a":
        draw_star(x)
    elif kind == "b":
        draw_circle(x/2)
    # for "c" no label is drawn

def jar(height, width):
    state = get_state()
    col_inside = choice(["hot pink", "pale turquoise", "yellow green", "crimson", "goldenrod2"])
    col_label = choice(["khaki", "thistle2", "papaya whip", "plum3"])
    H = (height - height//7)
    # glass
    rectangle_empty(H, width, "black", 1)
    hop(1, 1)
    # contents
    rectangle_full(0.9 * H, width - 2, col_inside)
    hop(width//4, H//4)
    # label
    rectangle_full(0.5 * H, 0.5 * width, col_label)
    hop(0.5 * width//2, 0.5 * H//3)
    x = min(0.5 * width, 0.5 * H) / 2 # sticker in the middle
    draw_label(choice(["a", "b", "c"]), x)
    restore_state(state)
    # lid
    hop(width//10, H)
    rectangle_full(H//7, 0.8 * width, "gray")
    restore_state(state)



# DRAWING CARROTS

def green_part(height, width):
    H = height//4
    W = width//8
    state = get_state()
    hop(-W//2, 0)
    for i in range(3):
        rectangle_full(H, W, "green")
        restore_state(state)
        if i == 1:
            hop(-W//2, 0)
            lt(40)
        else:
            hop(-W//2, 0)
            rt(40)

def carrot(height, width):
    state = get_state()
    hop(0, 0.75 * height)
    color("orange")
    begin_fill()
    goto(xcor() + width, ycor())
    goto(xcor() - width//2, ycor() - 0.75 * height)
    goto(xcor() - width//2, ycor() + 0.75 * height)
    end_fill()
    restore_state(state)
    hop(0.5 * width, 0.75 * height)
    green_part(height, width)
    restore_state(state)



def draw_supply(kind, height, width):
    if kind == "j":
        jar(height, width)
    elif kind == "c":
        carrot(height, width)


def spacing(no_cabinets, cabinet_w, no_shelves, h_min, h_max, supply):
    """determine where and what kind of supply to draw, depending on the number of shelves
    and their randomly chosen height and width"""
    x = 10
    y = 6
    min_width = (cabinet_w - 4) // x
    min_height = (window_height() // no_shelves) // y

    hop(5, 5)
    c = 0
    while x > 3:
        pensize(1)
        W = randrange(1, 4)
        H = randrange(h_min, h_max)
        if W == 3:
            draw_supply("j", H * min_height, W * min_width)
        else:
            if H >= 4:
                draw_supply(supply, H * min_height, W * min_width)
            else:
                draw_supply("j", H * min_height, W * min_width)
        hop(W * min_width, 0)
        x -= W
        c += 1
    if x <= 3:
        if x == 3:
            new_supply = "j"
        else:
            new_supply = choice(["j", "c"])
        # move by the number of already drawn supplies
        if no_cabinets % 2 == 0:
            draw_supply(new_supply, x * min_height, x * min_width - c)
        else:
            draw_supply(new_supply, x * min_height, x * min_width + c)


def shelves(no_cabinets, cabinet_w, no_shelves):
    state1 = get_state()
    H = window_height() // no_shelves
    fd(H//2)
    for i in range(no_shelves):
        state2 = get_state()
        rt(90)
        fd(cabinet_w)
        restore_state(state2)
        if i != no_shelves - 1:
            spacing(no_cabinets, cabinet_w, no_shelves, 3, 6, choice(["j", "c"]))
            restore_state(state2)
        if i == no_shelves - 1:
            spacing(no_cabinets, cabinet_w, no_shelves, 1, 3, "j")
            restore_state(state2)
        hop(0, H)

    restore_state(state1)


def cabinets():
    no_cabinets = randrange(3, 7)
    unit_w = (window_width() - 8) // no_cabinets  # space for each cabinet
    cabinet_w = unit_w - 12  # width of a shelf in a cabinet

    state = get_state()
    hop(-window_width() // 2, -window_height() // 2)
    pensize(9)
    for i in range(no_cabinets):
        color(choice(["chocolate", "chocolate1", "chocolate2", "chocolate3", "chocolate4"]))
        hop(9, 0)
        for j in range(2):
            fd(window_height())
            hop(cabinet_w, 0)
            rt(180)
        no_shelves = randrange(4, 12)
        shelves(no_cabinets, cabinet_w, no_shelves)
        hop(unit_w - 9, 0)  # so the cabinets don't touch

    restore_state(state)


def main():
    mode("logo")
    speed(0)
    bgcolor("LightGoldenrod1")
    cabinets()

main()
done()