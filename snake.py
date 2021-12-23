import pygame, sys
import random
from pygame.locals import *


class Point():
    col = 0
    row = 0

    def __init__(self, col, row):
        self.col = col
        self.row = row

    def copy(self):  #复制头坐标
        return Point(col=self.col, row=self.row)


pygame.init()  #初始化
W = 800
H = 600
COL = 40
ROW = 30
size = (W, H)
window = pygame.display.set_mode(size)  #屏幕大小
title = pygame.display.set_caption("贪吃蛇v0.1版")
head = Point(int(COL / 2), int(ROW / 2))  #头坐标
head_color = (0, 128, 128)
#身体坐标
bodies = [
    Point(col=head.col - 1, row=head.row),
    Point(col=head.col - 2, row=head.row),
    Point(col=head.col - 3, row=head.row)
]
bodies_color = (200, 200, 200)


def rect(point, color):  #绘制小格子
    cell_width = W / COL
    cell_height = H / ROW
    left = point.col * cell_width
    top = point.row * cell_height
    pygame.draw.rect(window, color, (left, top, cell_width, cell_height))


def reshow_food():  #食物随机出生
    while True:
        re_position = Point(col=random.randint(0, COL - 1),
                            row=random.randint(0, ROW - 1))
        is_seem = False
        if head.col == re_position.col and head.row == re_position.row:
            is_seem = True
        for body in bodies:
            if body.col == re_position.col and body.row == re_position.row:
                is_seem = True
                break
        if not is_seem:
            break
    return re_position


food = reshow_food()
food_color = (255, 255, 0)

keep = True
FPS = 8  #帧率
WHITE = (255, 255, 255)  #背景色
clock = pygame.time.Clock()
direct = random.choice(['up', 'right', 'down'])  #初始方向

while keep:
    events = pygame.event.get()  #获取事件列表
    for event in events:
        if event.type == pygame.QUIT:
            keep = False
            print('已退出')
        elif event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                if direct == 'left' or 'right':
                    direct = 'up'
                elif direct == 'down':
                    direct = 'down'
            if event.key == K_RIGHT:
                if direct == 'up' or 'down':
                    direct = 'right'
                elif direct == 'left':
                    direct = 'left'
            if event.key == K_DOWN:
                if direct == 'left' or 'right':
                    direct = 'down'
                elif direct == 'up':
                    direct = 'up'
            if event.key == K_LEFT:
                if direct == 'up' or 'down':
                    direct = 'left'
                elif direct == 'right':
                    direct = 'right'
            if event.key == K_ESCAPE:
                #退出pygame
                pygame.quit()
                print('按ESC退出！')
                #退出系统
                sys.exit()

    eat = (head.row == food.row and head.col == food.col)  #判断食物是否被吃
    if eat:
        food = reshow_food()
    bodies.insert(0, head.copy())  #将头添加到身体的第一个格子
    if not eat:
        bodies.pop()  #删除最后一个格子

    if direct == "left":  #移动
        head.col -= 1
    elif direct == "right":
        head.col += 1
    elif direct == "up":
        head.row -= 1
    elif direct == "down":
        head.row += 1
    dead = False
    if head.row < 0 or head.row >= ROW or head.col < 0 or head.col >= COL:
        print('超出边界')
        dead = True
    for body in bodies:
        if head.col == body.col and head.row == body.row:
            print('碰到自己身体了')
            dead = True
            break
    if dead:
        pygame.quit()
        print('Game Over')
        sys.exit()
    pygame.draw.rect(window, WHITE, (0, 0, W, H))
    rect(head, head_color)
    rect(food, food_color)
    for body in bodies:
        rect(body, bodies_color)
    #pygame.display.update()
    pygame.display.flip()  #更新屏幕显示
    clock.tick(FPS)
