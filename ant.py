#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import pygame as pg
import pygame_menu
from pygame.locals import *

# initialize
pg.init()

# Ant speed
Antspeed = [15, 20 ,25]

#
# Highest numder of step
Highest = "step.txt"

# Get window's size
screen = pg.display.Info()
WIDTH = screen.current_w
HEIGHT = screen.current_h

# Width and height of the cells and ant
Cell_size = 10

# Ensuring that the cell fit perfectly in the window
assert WIDTH % Cell_size == 0, "Window width must be a multiple of cell size(20).\nPlease Reset the WIDTH"
assert HEIGHT % Cell_size == 0, "Window height must be a multiple of cell size(20).\nPlease Reset the HEIGHT"

# Numder of Cells in Width
Cell_W = int(WIDTH / Cell_size)
# Number of Cells in Height
Cell_H = int(HEIGHT / Cell_size)

# Defining element colours
WHITE = (255, 225, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (40, 40, 40)
DARKGREEN = (0, 155, 0)

# Background Colour
BGC = BLACK

# Display font
DISPLAYFONT = pg.font.Font('freesansbold.ttf', 18)

# Default setting
Colour = 'Black'
cvaule = BLACK
Speed = 'Normal'
svalue = 2

# Block
block = []

# Message of About
ABOUT = ['Langton\'s Ant',
         'Langton\'s ant is a two-dimensional universal Turing machine with',
         'a very simple set of rules but complex emergent behavior.  It was',
         'invented by Chris Langton in 1986 and runs on a square lattice of',
         'black and white cells.The universality of Langton\'s ant was proven',
         'in 2000. The idea has been generalized in several different ways,',
         'such as turmites which add more colors and more states.',
         '\n',
         'Rules',
         'Squares on a plane are colored variously either black or white.We',
         'arbitrarily identify one square as the " ant " . The ant can travel   ',
         'in any of the four cardinal directions at each step it takes . The    ',
         '" ant " moves according to the rules below:                                    ',
         '·At a white square, turn 90° clockwise, flip the color of the square, move forward one unit',
         '·At a black square, turn 90° counter-clockwise, flip the color of the square, move forward one unit',
         'Langton\'s ant can also be described as a cellular automaton,where',
         'the grid is colored black or white and the "ant" square has one of',
         'eight different colors assigned to encode the combination of black',
         'or white state and the current direction of motion of the ant.    ',
         '\n',
         '—— Wikipedia']



def main():
    global FPSClock, DISPLAYSURF

    FPSClock = pg.time.Clock()
    DISPLAYSURF = pg.display.set_mode((WIDTH, HEIGHT), flags= pg.FULLSCREEN | pg.NOFRAME)
    pg.display.set_caption('Langton\'s Ant')
    pg.display.set_icon(pg.image.load("ant.png"))
    showStartScreen()
    Setting()


def terminate():
    pg.quit()
    sys.exit()


def checkForKeyPress():
    if len(pg.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pg.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

#
def load_data():
    with open(Highest, "r") as f:
        high = int(f.read())
        return high


def set_speed(value = (('Default', 2), 1), speed = '2') :
    global Speed, svalue

    tuplet, index = value
    Speed = tuplet[0]
    svalue = speed
    print('Chose Speed:', index)


def cell_colour(value = (('Black', BLACK), 1), colour = BLACK) :
    global Colour, cvaule

    tuplet, index = value
    Colour = tuplet[0]
    cvaule = colour
    print('Chose Colour:', index)


def drawGrid():
    # draw vertical lines
    for x in range(0, WIDTH, Cell_size):
        pg.draw.line(DISPLAYSURF, GRAY, (x, 0), (x, HEIGHT))
    # draw horizontal lines
    for y in range(0, HEIGHT, Cell_size):
        pg.draw.line(DISPLAYSURF, GRAY, (0, y), (WIDTH, y))


def drawAnt(coord):
    global x, y

    x = coord['x'] * Cell_size
    y = coord['y'] * Cell_size
    AntSegmentRect = pg.Rect(x, y, Cell_size, Cell_size)
    pg.draw.rect(DISPLAYSURF, DARKGREEN, AntSegmentRect)
    AntArrowSegment = pg.Rect(x + 1, y + 1, Cell_size - 4, Cell_size - 4)
    pg.draw.rect(DISPLAYSURF, GREEN, AntArrowSegment)
    AntInnerSegment = pg.Rect(x + 2, y + 2, Cell_size - 4, Cell_size - 4)
    pg.draw.rect(DISPLAYSURF, DARKGREEN, AntInnerSegment)
    AntCoreSegment = pg.Rect(x + 4, y + 4, Cell_size - 7, Cell_size - 7)
    pg.draw.rect(DISPLAYSURF, GREEN, AntCoreSegment)


def drawBBlock():
    for i in block:
        blockRect = pg.Rect(i['x'] * Cell_size, i['y'] * Cell_size, Cell_size, Cell_size)
        pg.draw.rect(DISPLAYSURF, BLACK, blockRect)


def drawWBlock():
    for i in block:
        blockRect = pg.Rect(i['x'] * Cell_size, i['y'] * Cell_size, Cell_size, Cell_size)
        pg.draw.rect(DISPLAYSURF, WHITE, blockRect)


def run():
    pg.display.update()

    startx = int(Cell_W / 2)
    starty = int(Cell_H / 2)
    coord = {'x': startx, 'y': starty}
    print(coord)

    direction = 0
    directions = ((0, +1), (+1, 0), (0, -1), (-1, 0))

    step = 0

    while True:
        # event handling loop
        for event in pg.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
        DISPLAYSURF.fill(Colour)
        drawGrid()
        drawAnt(coord)
        print(direction)

        if Colour == 'Black':
            drawWBlock()
            if coord in block:
                block.remove(coord)
                direction += 1
                startx += directions[direction % 4][0]
                starty += directions[direction % 4][1]
                coord = {'x': startx, 'y': starty}
                print('draw', startx, starty, coord)
            else:
                block.append(coord)
                direction -= 1
                if direction < 0:
                    direction = 4 + direction
                startx += directions[direction % 4][0]
                starty += directions[direction % 4][1]
                coord = {'x': startx, 'y': starty}
                print('run', startx, starty, coord)
        if Colour == 'White':
            drawBBlock()
            if coord in block:
                block.remove(coord)
                direction -= 1
                if direction < 0:
                    direction = 4 + direction
                startx += directions[direction % 4][0]
                starty += directions[direction % 4][1]
                coord = {'x': startx, 'y': starty}
                print('draw', startx, starty, coord)
            else:
                block.append(coord)
                direction += 1
                startx += directions[direction % 4][0]
                starty += directions[direction % 4][1]
                coord = {'x': startx, 'y': starty}
                print('run', startx, starty, coord)




        pg.display.update()
        FPSClock.tick(Antspeed[svalue - 1])


def start_the_game():
    print('Colour:', Colour,'[', cvaule, ']\n' + 'Speed:', Speed, '[', svalue, ']')
    print('==================================================\n')
    while True:
        run()
        #terminate() # Used for testing


# Press key message
def drawPressKeyMsg():
    pressKeySurf = DISPLAYFONT.render('Press a key to play or press Esc to exit.', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WIDTH - 350, HEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def showStartScreen():
    STARTFONT = pg.font.Font('freesansbold.ttf', 90)
    Anttitle = STARTFONT.render('Langton\'sAnt', True, WHITE, DARKGREEN)
    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGC)
        rotatedSurf1 = pg.transform.rotate(Anttitle, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WIDTH / 2, HEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        drawPressKeyMsg()

        if checkForKeyPress():
            pg.event.get()  # clear event queue
            return
        pg.display.update()
        FPSClock.tick(Antspeed[1]) # Title speed
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def Setting():

    print('\n======================Setting=====================')

    menu = pygame_menu.Menu('Welcome.This is Setting Menu', WIDTH, HEIGHT,
                            theme=pygame_menu.themes.THEME_GREEN)

    menu.add.label('Author : Icefyre', align=pygame_menu.locals.ALIGN_CENTER, font_size=30)

    about_theme = pygame_menu.themes.THEME_GREEN.copy()
    about_theme.widget_margin = (0, 0)

    about_menu = pygame_menu.Menu(
        height=HEIGHT,
        theme=about_theme,
        title='About',
        width=WIDTH
    )

    for m in ABOUT:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=25)
    about_menu.add.vertical_margin(30)
    about_menu.add.button('Return to menu', pygame_menu.events.BACK)
    menu.add.button('About', about_menu)

    menu.add.selector('Speed :', [('Default', 2), ('Slow', 1), ('Quick', 3)], onchange = set_speed, selector_id='select_speed')
    menu.add.selector('Cell colour :', [('Black', BLACK), ('White', WHITE)], onchange = cell_colour, selector_id='select_colour')
    menu.add.button('Start', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(DISPLAYSURF)
    #pass # Used for testing








if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
