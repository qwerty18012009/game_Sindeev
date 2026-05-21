import pygame as pg
import random, time, sys
from pygame.locals import *

fps = 25
window_w, window_h = 600, 500
block, cup_h, cup_w = 20, 20, 10
side_freq, down_freq = 0.15, 0.1
side_margin = int((window_w - cup_w * block) / 2)
top_margin = window_h - (cup_h * block) - 5
fig_w, fig_h = 5, 5
empty = 'o'

colors = ((0, 255, 255), (255, 165, 0), (0, 255, 0), (128, 0, 128), (255, 192, 203), (0, 0, 255), (255, 0, 0))
lightcolors = ((102, 255, 255), (255, 200, 102), (102, 255, 102), (178, 102, 178), (255, 220, 230), (102, 102, 255), (255, 102, 102))

bg_color = (0, 0, 128)
title_color = (255, 255, 0)
text_color = (255, 255, 255)

figures = {
    'T': [['ooooo', 'ooooo', 'oxxxo', 'ooxoo', 'ooooo'],
          ['ooooo', 'ooxoo', 'ooxxo', 'ooxoo', 'ooooo'],
          ['ooooo', 'ooxoo', 'oxxxo', 'ooooo', 'ooooo'],
          ['ooooo', 'ooxoo', 'oxxoo', 'ooxoo', 'ooooo']],
    'S': [['ooooo', 'ooooo', 'ooxxo', 'oxxoo', 'ooooo'],
          ['ooooo', 'ooxoo', 'ooxxo', 'oooxo', 'ooooo']],
    'Z': [['ooooo', 'ooooo', 'oxxoo', 'ooxxo', 'ooooo'],
          ['ooooo', 'oooxo', 'ooxxo', 'ooxoo', 'ooooo']],
    'J': [['ooooo', 'ooxoo', 'ooxoo', 'oxxoo', 'ooooo'],
          ['ooooo', 'ooooo', 'oxxxo', 'oooxo', 'ooooo'],
          ['ooooo', 'ooxxo', 'ooxoo', 'ooxoo', 'ooooo'],
          ['ooooo', 'ooooo', 'oxooo', 'oxxxo', 'ooooo']],
    'L': [['ooooo', 'ooxoo', 'ooxoo', 'ooxxo', 'ooooo'],
          ['ooooo', 'ooooo', 'oooxo', 'oxxxo', 'ooooo'],
          ['ooooo', 'oxxoo', 'ooxoo', 'ooxoo', 'ooooo'],
          ['ooooo', 'ooooo', 'oxxxo', 'oxooo', 'ooooo']],
    'I': [['ooxoo', 'ooxoo', 'ooxoo', 'ooxoo', 'ooooo'],
          ['ooooo', 'ooooo', 'xxxxo', 'ooooo', 'ooooo']],
    'O': [['ooooo', 'ooooo', 'oxxoo', 'oxxoo', 'ooooo']]
}

def main():
    global fps_clock, display_surf, basic_font, big_font
    pg.init()
    fps_clock = pg.time.Clock()
    display_surf = pg.display.set_mode((window_w, window_h))
    basic_font = pg.font.Font('freesansbold.ttf', 18)
    big_font = pg.font.Font('freesansbold.ttf', 45)
    pg.display.set_caption('Тетрис Lite')
    showText('Тетрис Lite')
    while True:
        runTetris()
        pauseScreen()
        showText('Игра закончена')

def runTetris():
    cup = emptycup()
    last_move_down = time.time()
    last_side_move = time.time()
    last_fall = time.time()
    going_down = False
    going_left = False
    going_right = False
    points = 0
    level, fall_speed = calcSpeed(points)
    fallingFig = getNewFig()
    nextFig = getNewFig()

    while True:
        if fallingFig == None:
            fallingFig = nextFig
            nextFig = getNewFig()
            last_fall = time.time()
            if not checkPos(cup, fallingFig):
                return
        
        quitGame()
        
        for event in pg.event.get():
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    pauseScreen()
                    last_fall = time.time()
                    last_move_down = time.time()
                    last_side_move = time.time()
                elif event.key == K_LEFT:
                    going_left = False
                elif event.key == K_RIGHT:
                    going_right = False
                elif event.key == K_DOWN:
                    going_down = False
            
            elif event.type == KEYDOWN:
                if event.key == K_LEFT and checkPos(cup, fallingFig, adjX=-1):
                    fallingFig['x'] -= 1
                    going_left = True
                    going_right = False
                    last_side_move = time.time()
                
                elif event.key == K_RIGHT and checkPos(cup, fallingFig, adjX=1):
                    fallingFig['x'] += 1
                    going_right = True
                    going_left = False
                    last_side_move = time.time()
                
                elif event.key == K_UP:
                    fallingFig['rotation'] = (fallingFig['rotation'] + 1) % len(figures[fallingFig['shape']])
                    if not checkPos(cup, fallingFig):
                        fallingFig['rotation'] = (fallingFig['rotation'] - 1) % len(figures[fallingFig['shape']])
                
                elif event.key == K_DOWN:
                    going_down = True
                    if checkPos(cup, fallingFig, adjY=1):
                        fallingFig['y'] += 1
                    last_move_down = time.time()
                
                elif event.key == K_RETURN:
                    going_down = False
                    going_left = False
                    going_right = False
                    for i in range(1, cup_h):
                        if not checkPos(cup, fallingFig, adjY=i):
                            break
                    fallingFig['y'] += i - 1
        
        if (going_left or going_right) and time.time() - last_side_move > side_freq:
            if going_left and checkPos(cup, fallingFig, adjX=-1):
                fallingFig['x'] -= 1
            elif going_right and checkPos(cup, fallingFig, adjX=1):
                fallingFig['x'] += 1
            last_side_move = time.time()
        
        if going_down and time.time() - last_move_down > down_freq and checkPos(cup, fallingFig, adjY=1):
            fallingFig['y'] += 1
            last_move_down = time.time()
        
        if time.time() - last_fall > fall_speed:
            if not checkPos(cup, fallingFig, adjY=1):
                addToCup(cup, fallingFig)
                points += clearCompleted(cup)
                level, fall_speed = calcSpeed(points)
                fallingFig = None
            else:
                fallingFig['y'] += 1
                last_fall = time.time()
        
        display_surf.fill(bg_color)
        drawTitle()
        gamecup(cup)
        drawInfo(points, level)
        drawnextFig(nextFig)
        if fallingFig != None:
            drawFig(fallingFig)
        pg.display.update()
        fps_clock.tick(fps)

def txtObjects(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def showText(text):
    titleSurf, titleRect = txtObjects(text, big_font, title_color)
    titleRect.center = (int(window_w / 2), int(window_h / 2))
    display_surf.blit(titleSurf, titleRect)
    
    presskeySurf, presskeyRect = txtObjects('Нажмите любую клавишу для продолжения', basic_font, text_color)
    presskeyRect.center = (int(window_w / 2), int(window_h / 2) + 100)
    display_surf.blit(presskeySurf, presskeyRect)
    
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                stopGame()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    stopGame()
                return
        pg.display.update()
        fps_clock.tick()

def pauseScreen():
    pause = pg.Surface((600, 500), pg.SRCALPHA)
    pause.fill((0, 0, 255, 127))
    display_surf.blit(pause, (0, 0))
    
    pauseSurf, pauseRect = txtObjects('ПАУЗА', big_font, (255, 255, 0))
    pauseRect.center = (int(window_w / 2), int(window_h / 2))
    display_surf.blit(pauseSurf, pauseRect)
    
    pg.display.update()
    
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                stopGame()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return
                if event.key == K_ESCAPE:
                    stopGame()

def quitGame():
    for event in pg.event.get(QUIT):
        stopGame()
    for event in pg.event.get(KEYUP):
        if event.key == K_ESCAPE:
            stopGame()
        pg.event.post(event)

def stopGame():
    pg.quit()
    sys.exit()

def calcSpeed(points):
    level = int(points / 10) + 1
    fall_speed = 0.27 - (level * 0.02)
    return level, fall_speed

def getNewFig():
    shape = random.choice(list(figures.keys()))
    newFig = {
        'shape': shape,
        'rotation': random.randint(0, len(figures[shape]) - 1),
        'x': int(cup_w / 2) - int(fig_w / 2),
        'y': -2,
        'color': random.randint(0, len(colors) - 1)
    }
    return newFig

def addToCup(cup, fig):
    for x in range(fig_w):
        for y in range(fig_h):
            if figures[fig['shape']][fig['rotation']][y][x] != empty:
                cup[x + fig['x']][y + fig['y']] = fig['color']

def emptycup():
    cup = []
    for i in range(cup_w):
        cup.append([empty] * cup_h)
    return cup

def incup(x, y):
    return x >= 0 and x < cup_w and y < cup_h

def checkPos(cup, fig, adjX=0, adjY=0):
    for x in range(fig_w):
        for y in range(fig_h):
            if figures[fig['shape']][fig['rotation']][y][x] != empty:
                if not incup(x + fig['x'] + adjX, y + fig['y'] + adjY):
                    return False
                if y + fig['y'] + adjY >= 0:
                    if cup[x + fig['x'] + adjX][y + fig['y'] + adjY] != empty:
                        return False
    return True

def isCompleted(cup, y):
    for x in range(cup_w):
        if cup[x][y] == empty:
            return False
    return True

def clearCompleted(cup):
    removed_lines = 0
    y = cup_h - 1
    while y >= 0:
        if isCompleted(cup, y):
            for pushDownY in range(y, 0, -1):
                for x in range(cup_w):
                    cup[x][pushDownY] = cup[x][pushDownY - 1]
            for x in range(cup_w):
                cup[x][0] = empty
            removed_lines += 1
        else:
            y -= 1
    return removed_lines

def convertCoords(block_x, block_y):
    return (side_margin + (block_x * block)), (top_margin + (block_y * block))

def drawBlock(block_x, block_y, color, pixelx=None, pixely=None):
    if color == empty:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(block_x, block_y)
    pg.draw.rect(display_surf, colors[color], (pixelx + 1, pixely + 1, block - 1, block - 1), 0, 3)
    pg.draw.rect(display_surf, lightcolors[color], (pixelx + 1, pixely + 1, block - 4, block - 4), 0, 3)
    pg.draw.circle(display_surf, colors[color], (pixelx + block / 2, pixely + block / 2), 5)

def drawTitle():
    titleSurf = big_font.render('ТЕТРИС LITE', True, title_color)
    titleRect = titleSurf.get_rect()
    titleRect.topleft = (window_w - 475, 5)
    display_surf.blit(titleSurf, titleRect)

def drawInfo(points, level):
    pointsSurf = basic_font.render('Баллы: %s' % points, True, text_color)
    pointsRect = pointsSurf.get_rect()
    pointsRect.topleft = (window_w - 550, 180)
    display_surf.blit(pointsSurf, pointsRect)
    
    levelSurf = basic_font.render('Уровень: %s' % level, True, text_color)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (window_w - 550, 220)
    display_surf.blit(levelSurf, levelRect)

def drawFig(fig, pixelx=None, pixely=None):
    figToDraw = figures[fig['shape']][fig['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(fig['x'], fig['y'])
    
    for x in range(fig_w):
        for y in range(fig_h):
            if figToDraw[y][x] != empty:
                drawBlock(None, None, fig['color'], pixelx + (x * block), pixely + (y * block))

def drawnextFig(fig):
    nextSurf = basic_font.render('Следующая:', True, text_color)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (window_w - 140, 180)
    display_surf.blit(nextSurf, nextRect)
    drawFig(fig, pixelx=window_w - 140, pixely=220)

def gamecup(cup):
    pg.draw.rect(display_surf, (255, 255, 255), (side_margin - 4, top_margin - 4, (cup_w * block) + 8, (cup_h * block) + 8), 5)
    pg.draw.rect(display_surf, bg_color, (side_margin, top_margin, cup_w * block, cup_h * block))
    for x in range(cup_w):
        for y in range(cup_h):
            drawBlock(x, y, cup[x][y])

if __name__ == '__main__':
    main()