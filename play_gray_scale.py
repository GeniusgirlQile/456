# encoding: utf-8

import os, sys, random
import pygame 
from pygame.locals import *

from drew import *

# 視窗大小.
canvas_width = 800
canvas_height = 600

# 顏色.
color_red           = (255, 0, 0)
color_gray          = (107,130,114)
color_gray_block    = (20,31,23)

# 磚塊數量串列.
bricks_list = []

# 移動速度.
dx =  8
dy = -8

# 遊戲狀態.
# 0:等待開球
# 1:遊戲進行中
game_mode = 0


def showFont( text, x, y, color):
    global canvas    
    text = font.render(text, True, color) 
    canvas.blit( text, (x,y))


def isCollision( x, y, boxRect):
    if (x >= boxRect[0] and x <= boxRect[0] + boxRect[2] and y >= boxRect[1] and y <= boxRect[1] + boxRect[3]):
        return True;          
    return False;  


def resetGame():
    # 宣告使用全域變數.
    global game_mode, brick_num, bricks_list, dx, dy

    # 磚塊
    for bricks in bricks_list:
        # 磚塊顏色
        bricks.color = color_gray_block        
        # 開啟磚塊.
        bricks.visivle = True
    # 0:等待開球
    game_mode = 0
    # 磚塊數量.
    brick_num = 99    
    # 移動速度.
    dx =  8
    dy = -8

# 初始.
pygame.init()
# 顯示Title.
pygame.display.set_caption(u"打磚塊遊戲")
# 建立畫佈大小.
canvas = pygame.display.set_mode((canvas_width, canvas_height))
# 時脈.
clock = pygame.time.Clock()

# 設定字型.
font = pygame.font.SysFont("simsunnsimsun", 18)

# 底板.
paddle_x = 0
paddle_y = (canvas_height - 48)
paddle = Box(pygame, canvas, "paddle", [paddle_x, paddle_y, 100, 24], color_gray_block)

# 球.
ball_x = paddle_x
ball_y = paddle_y
ball   = Circle(pygame, canvas, "ball", [ball_x, ball_x], 8, color_gray_block)

# 建立磚塊
brick_num = 0
brick_x = 70
brick_y = 60
brick_w = 0
brick_h = 0
for i in range( 0, 99):
    if((i % 11)==0):
        brick_w = 0
        brick_h = brick_h + 18        
    bricks_list.append (Box(pygame, canvas, "brick_"+str(i), [  brick_w + brick_x, brick_h+ brick_y, 58, 16], color_gray_block))
    brick_w = brick_w + 60
# 初始遊戲.
resetGame()


running = True
while running:
    
    for event in pygame.event.get():
        # 離開遊戲.
        if event.type == pygame.QUIT:
            running = False
        # 判斷按下按鈕
        if event.type == pygame.KEYDOWN:
            # 判斷按下ESC按鈕
            if event.key == pygame.K_ESCAPE:
                running = False
                
        # 判斷Mouse.
        if event.type == pygame.MOUSEMOTION:
            paddle_x = pygame.mouse.get_pos()[0] - 50
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(game_mode == 0):
                game_mode = 1

       
    # 清除畫面.
    canvas.fill(color_gray)
    
    # 磚塊
    for bricks in bricks_list:
        # 球碰磚塊.
        if(isCollision( ball.pos[0], ball.pos[1], bricks.rect)):
            if(bricks.visivle):                
                # 扣除磚塊.
                brick_num = brick_num -1
                # 初始遊戲.
                if(brick_num <= 0):
                    resetGame()
                    break
                # 球反彈.
                dy = -dy; 
            # 關閉磚塊.
            bricks.visivle = False

        # 更新磚塊.        
        bricks.update()
            
    #顯示磚塊數量.
    showFont( u"磚塊數量:"+str(brick_num), 8, 20, (255, 0, 0))

    # 秀板子.
    paddle.rect[0] = paddle_x
    paddle.update()

    # 碰撞判斷-球碰板子.
    if(isCollision( ball.pos[0], ball.pos[1], paddle.rect)):        
        # 球反彈.
        dy = -dy;         
            
    # 球.
    # 0:等待開球
    if(game_mode == 0):
        ball.pos[0] = ball_x = paddle.rect[0] + ( (paddle.rect[2] - ball.radius) >> 1 )
        ball.pos[1] = ball_y = paddle.rect[1] - ball.radius        
    # 1:遊戲進行中
    elif(game_mode == 1):
        ball_x += dx
        ball_y += dy
        #判斷死亡.
        if(ball_y + dy > canvas_height - ball.radius):
            game_mode = 0        
        # 右牆或左牆碰撞.
        if(ball_x + dx > canvas_width - ball.radius or ball_x + dx < ball.radius):
            dx = -dx
        # 下牆或上牆碰撞
        if(ball_y + dy > canvas_height - ball.radius or ball_y + dy < ball.radius):        
            dy = -dy
        ball.pos[0] = ball_x
        ball.pos[1] = ball_y

    # 更新球.
    ball.update()

    # 顯示中文.
    showFont( u"FPS:" + str(int(clock.get_fps())), 8, 2, (255, 0, 0))
    
    # 更新畫面.
    pygame.display.update()
    clock.tick(60)

# 離開遊戲.
pygame.quit()
quit()