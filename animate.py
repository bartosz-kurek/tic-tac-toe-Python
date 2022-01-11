import time
import os
import random

anim_output = False
anim_state = False


def cls():
    '''cls/clear function'''
    os.system('cls' if os.name == 'nt' else 'clear')


def anim_init(output):
    out_list = []
    out_state = []
    for x in output.split("\n"):
        tmp = []
        tmp2 = []
        for y in list(x):
            tmp.append(y)
            tmp2.append(0)
        out_list.append(tmp)
        out_state.append(tmp2)

    global anim_output
    global anim_state
    anim_output = out_list
    anim_state = out_state


def render():
    global anim_output
    global anim_state

    cls()
    raster = []
    for x, row in enumerate(anim_state):
        ln_out = []
        for y, line in enumerate(row):
            if line == 0:
                ln_out.append(" ")
            elif line == 1:
                ln_out.append("-")
            elif line == 2:
                ln_out.append("+")
            else:
                ln_out.append(anim_output[x][y])
        raster.append("".join(ln_out))
    print("\n".join(raster))


# anim_init("""  +---+---+---+
# 3 |   |   |   |
#  +---+---+---+
# 2 |   |   |   |
#  +---+---+---+
# 1 |   |   |   |
#  +---+---+---+
#    A   B   C  """)


def animate():
    global anim_state
    global anim_output

    width = len(anim_state[0])
    height = len(anim_state)

    anim_order = []
    for x in range(width*height):
        anim_order.append(x)

    for x in range(width*height):
        x2 = random.randint(0, width*height-1)
        a = anim_order[x]
        b = anim_order[x2]
        anim_order[x2] = a
        anim_order[x] = b

    for anim_pos in range(len(anim_order)+200):

        if anim_pos < len(anim_order):
            tmp = anim_order[anim_pos]
            x = tmp % width
            y = tmp // width
            x = min(len(anim_state[y])-1, x)
            anim_state[y][x] = 1

        if anim_pos - 100 >= 0 and anim_pos < len(anim_order)+100:
            tmp = anim_order[anim_pos-100]
            x = tmp % width
            y = tmp // width
            x = min(len(anim_state[y])-1, x)
            anim_state[y][x] = 2

        if anim_pos - 200 >= 0:
            tmp = anim_order[anim_pos-200]
            x = tmp % width
            y = tmp // width
            x = min(len(anim_state[y])-1, x)
            anim_state[y][x] = 3

        if anim_pos % 20 == 0:
            render()
            time.sleep(0.01)

    render()
