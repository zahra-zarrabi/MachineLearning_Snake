import random
import time
import pygame
import sys
import GameConfig
import pandas as pd


class my_snake:
    def __init__(self):
        self.w=10
        self.h=10
        self.x=width/2
        self.y=height/2
        self.color=(5,5,5)
        self.speed=1
        self.score=0
        self.x_change=0
        self.y_change=0
        self.speed_help= 1

    def show_snake(self):
        pygame.draw.rect(my_screen,self.color,[self.x,self.y,self.w,self.h])

    def move_snake(self):
        if self.x_change == -1:
            self.x -= self.speed
        elif self.x_change == 1:
            self.x += self.speed
        elif self.y_change == -1:
            self.y -= self.speed
        elif self.y_change == 1:
            self.y += self.speed
        self.speed = self.speed_help

    def eatapple(self):
        if (apple.x-apple.r <= self.x <= apple.x + apple.r) and (apple.y - apple.r <= self.y <= apple.y + apple.r):
            return True
        else:
            return False


class Apple:
    def __init__(self):
        self.r=10
        self.x=random.randint(3,width-10)
        self.y=random.randint(3,height-10)
        # self.color=(255,0,0)
        self.image_apple=pygame.image.load('apple.png')

    def show_apple(self):
        my_screen.blit(self.image_apple,[self.x,self.y])

def move_autom(snake, direction):
    if direction == 'right':
        snake.x_change = 1
        snake.y_change = 0
    elif direction == 'left':
        snake.x_change = -1
        snake.y_change = 0
    elif direction=='up':
        snake.x_change = 0
        snake.y_change = -1
    elif direction=='down':
        snake.x_change = 0
        snake.y_change = 1
    snake.move_snake()


def add_data(df, snake_data, direction):
    w0 = snake_data.y   # up
    w1 = GameConfig.width - snake_data.x  # right
    w2 = GameConfig.height - snake_data.y  # down
    w3 = snake_data.x  # left

    if direction == 'up':
        a0 = 1
        a1, a2, a3 = 0, 0, 0
    elif direction == 'right':
        a1 = 1
        a0, a2, a3 = 0, 0, 0
    elif direction == 'down':
        a2 = 1
        a0, a1, a3 = 0, 0, 0
    else:
        a3 = 1
        a0, a1, a2 = 0, 0, 0

    rd= random.random()

    direction = direction
    if rd > 0.5:
        dic= {'w0':str(w0), 'w1': str(w1), 'w2':str(w2), 'w3':str(w3), 'a0':str(a0), 'a1':str(a1), 'a2':str(a2), 'a3':str(a3), 'direction':str(direction)}
        df = df.append(dic,ignore_index=True)

    return df


if __name__=="__main__":
    width=900
    height=600
    my_screen=pygame.display.set_mode((width,height))
    bg = pygame.image.load('background.jpg')
    pygame.mixer.init()
    snake = my_snake()
    apple=Apple()
    pygame.mixer.music.load("sound.wav")
    pygame.mixer.music.play()
    clock=pygame.time.Clock()
    my_screen.fill((3,200,0))
    df = pd.DataFrame(columns=['w0','w1','w2','w3','a0','a1','a2','a3','direction'])

    while True:
        pygame.display.set_caption('python game made by zahra     score:%d' % snake.score)

        while snake.x < apple.x:
            if snake.x + snake.speed > apple.x:
                snake.speed = apple.x - snake.x
                move_autom(snake, direction='right')
                df = add_data(df, snake, 'right')
                my_screen.blit(bg, (0, 0))
                snake.show_snake()
                apple.show_apple()
                pygame.display.update()
                clock.tick(30)
                break
            move_autom(snake, direction='right')
            df = add_data(df, snake, 'right')
            my_screen.blit(bg, (0, 0))
            snake.show_snake()
            apple.show_apple()
            pygame.display.update()
            clock.tick(30)

        while snake.x > apple.x:
            if snake.x - snake.speed < apple.x:
                snake.speed = snake.x - apple.x
                move_autom(snake, direction='left')
                df = add_data(df, snake, 'left')
                my_screen.blit(bg, (0, 0))
                snake.show_snake()
                apple.show_apple()
                pygame.display.update()
                clock.tick(30)
                break
            move_autom(snake, direction='left')
            df = add_data(df, snake, 'left')
            my_screen.blit(bg, (0, 0))
            snake.show_snake()
            apple.show_apple()
            pygame.display.update()
            clock.tick(30)

        while snake.y > apple.y:
            if snake.y - snake.speed < apple.y:
                snake.speed = snake.y - apple.y
                move_autom(snake, direction='up')
                df = add_data(df, snake, 'up')
                my_screen.blit(bg, (0, 0))
                snake.show_snake()
                apple.show_apple()
                pygame.display.update()
                clock.tick(30)
                break
            move_autom(snake, direction='up')
            df = add_data(df, snake, 'up')
            my_screen.blit(bg, (0, 0))
            snake.show_snake()
            apple.show_apple()
            pygame.display.update()
            clock.tick(30)

        while snake.y < apple.y:
            if snake.y + snake.speed > apple.y:
                snake.speed = apple.y - snake.y
                move_autom(snake, direction='down')
                df = add_data(df, snake, 'down')
                my_screen.blit(bg, (0, 0))
                snake.show_snake()
                apple.show_apple()
                pygame.display.update()
                clock.tick(30)
                break
            move_autom(snake, direction='down')
            df = add_data(df, snake, 'down')
            my_screen.blit(bg, (0, 0))
            snake.show_snake()
            apple.show_apple()
            pygame.display.update()
            clock.tick(30)

        if width <= snake.x or snake.x < 0 or height < snake.y or snake.y < 0 or snake.score==200:
            time.sleep(1)
            print('gameover')
            pygame.quit()
            sys.exit()
        if snake.eatapple() == True:
            sound = pygame.mixer.Sound("soundeat.wav")
            pygame.mixer.Sound.play(sound)
            snake.h += 2
            snake.speed += 1
            snake.speed_help = snake.speed
            snake.score += 1
            apple = Apple()

        my_screen.blit(bg, (0, 0))
        snake.show_snake()
        apple.show_apple()

        pygame.display.update()
        clock.tick(30)
        df.to_csv('dataset2.csv')



