"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.
"""
import random
from random import choice
from turtle import *

from freegames import floor, vector

pac_speed = 10
ghost_speed = 5
pixels_per_tile = 20
tiles_per_line = 20
x_offset = 200
y_offset = 180
ghost_number = 6

# 20 * 20
# fmt: off
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

debug = True
state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)


def get_random_valid_pos():
    max_try = 20
    idx = random.randint(0, len(tiles) - 1)
    try_times = 0
    while tiles[idx] == 0 and try_times < max_try:
        idx = random.randint(0, len(tiles))
        try_times = try_times + 1
    if try_times >= max_try:
        return 0
    else:
        return idx


def offset(point):
    """Return offset of point in tiles."""
    x = (floor(point.x, pixels_per_tile) + x_offset) / pixels_per_tile
    y = (y_offset - floor(point.y, pixels_per_tile)) / pixels_per_tile
    index = int(x + y * tiles_per_line)
    return index


def point_x(index):
    x = (index % tiles_per_line) * tiles_per_line - x_offset
    return x


def point_y(index):
    y = y_offset - (index // tiles_per_line) * tiles_per_line
    return y


ghosts = []
for i in range(ghost_number):
    valid_idx = get_random_valid_pos()
    if valid_idx > 0:
        pos_aim = [vector(point_x(valid_idx), point_y(valid_idx)), vector(ghost_speed, 0)]
        ghosts.append(pos_aim)

aim = vector(pac_speed, 0)
valid_idx = get_random_valid_pos()
pacman = vector(point_x(valid_idx), point_y(valid_idx))


# fmt: on


def square(x, y):
    """Draw square using path at (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()

    path.color('blue')
    path.begin_fill()

    for count in range(4):
        path.forward(pixels_per_tile)
        path.left(90)

    path.end_fill()
    if debug:
        path.color('white')
        if x == -1 * y_offset:
            path.write(y)
        else:
            path.write(x)


def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + pixels_per_tile - 1)

    if tiles[index] == 0:
        return False

    return point.x % pixels_per_tile == 0 or point.y % pixels_per_tile == 0


def world():
    """Draw world using path."""
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = point_x(index)
            y = point_y(index)
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + pixels_per_tile / 2, y + pixels_per_tile / 2)
                path.dot(3, 'white')


def move():
    """Move pacman and all ghosts."""
    writer.undo()
    writer.write(state['score'])

    clear()

    pacman_valid = valid(pacman + aim)
    print("pos:%s, aim:%s, valid:%s" % (pacman, aim, pacman_valid))
    if pacman_valid:
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = point_x(index)
        y = point_y(index)
        square(x, y)

    up()
    goto(pacman.x + pixels_per_tile / 2, pacman.y + pixels_per_tile / 2)
    dot(pixels_per_tile, 'yellow')

    for idx in range(len(ghosts)):
        point, course = ghosts[idx]
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(ghost_speed, 0),
                vector(-1 * ghost_speed, 0),
                vector(0, ghost_speed),
                vector(0, -1 * ghost_speed),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + pixels_per_tile / 2, point.y + pixels_per_tile / 2)
        dot(pixels_per_tile, 'red')
        write(idx, align="center")

    update()

    for point, course in ghosts:
        if abs(pacman - point) < pixels_per_tile:
            return

    ontimer(move, 100)


def change(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


def reborn():
    print()


setup(520, 600, 0, 0)
hideturtle()
tracer(False)
writer.goto(200, 200)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(pac_speed, 0), 'Right')
onkey(lambda: change(-1 * pac_speed, 0), 'Left')
onkey(lambda: change(0, pac_speed), 'Up')
onkey(lambda: change(0, -1 * pac_speed), 'Down')
world()
move()
done()
