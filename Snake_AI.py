import numpy as np
import pygame
import random
import GameConfig
import time
import sys
import tensorflow as tf

class my_snake:
    def __init__(self):
        self.w=10
        self.h=10
        self.x=game.width/2
        self.y=game.height/2
        self.color=(5,5,5)
        self.speed=1
        self.score=0
        self.x_change=0
        self.y_change=0
        self.speed_help= 1

    def show_snake(self):
        pygame.draw.rect(game.my_screen,self.color,[self.x,self.y,self.w,self.h])

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

    def move_autom(self,snake, direction):
        if direction == 'right':
            snake.x_change = 1
            snake.y_change = 0
        elif direction == 'left':
            snake.x_change = -1
            snake.y_change = 0
        elif direction == 'up':
            snake.x_change = 0
            snake.y_change = -1
        elif direction == 'down':
            snake.x_change = 0
            snake.y_change = 1
        snake.move_snake()


class Apple:
    def __init__(self):
        self.r=10
        self.x=random.randint(3,game.width-10)
        self.y=random.randint(3,game.height-10)
        # self.color=(255,0,0)
        self.image_apple=pygame.image.load('apple.png')

    def show_apple(self):
        game.my_screen.blit(self.image_apple,[self.x,self.y])


def get_data():
    w0 = snake.y   # up
    w1 = game.width - snake.x  # right
    w2 = game.height - snake.y  # down
    w3 = snake.x   # left

    if snake.y > apple.y:
        a0 = 1
        a1,a2,a3 = 0,0,0

    elif snake.x < apple.x:
        a1 = 1
        a0, a2, a3 = 0, 0, 0

    elif snake.y < apple.y:
        a2 = 1
        a1, a0, a3 = 0, 0, 0

    elif snake.x > apple.x:
        a3 = 1
        a1, a2, a0 = 0, 0, 0

    return np.array([w0,w1,w2,w3,a0,a1,a2,a3])


class Game:
    def __init__(self):
        self.width = 900
        self.height = 600
        self.my_screen = pygame.display.set_mode((self.width, self.height))
        self.bg = pygame.image.load('background.jpg')
        pygame.mixer.init()
        pygame.mixer.music.load("sound.wav")
        pygame.mixer.music.play()
        self.clock = pygame.time.Clock()

        self.my_screen.fill((3, 200, 0))
        self.x_min=np.load('x_train_min.npy')
        self.x_max = np.load('x_train_max.npy')

    def play(self, model):
        global apple, snake
        apple = Apple()
        snake = my_snake()
        self.my_screen.blit(self.bg, (0, 0))
        snake.show_snake()
        apple.show_apple()

        while True:
            pygame.display.set_caption('python game made by zahra     score:%d' % snake.score)
            X = get_data()
            X = X.reshape(1, -1)
            X[:,:4]=np.subtract(X[:,:4],self.x_min)/(self.x_max - self.x_min)
            y_pred = model.predict(X)
            y_pred=np.argmax(y_pred)
            y_pred_dic = {0: 'up',1: 'right',2:'down',3:'left'}
            direction = y_pred_dic[y_pred]
            snake.move_autom(snake, direction)

            if self.width <= snake.x or snake.x < 0 or self.height < snake.y or snake.y < 0 or snake.score == 200:
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

            self.my_screen.blit(self.bg, (0, 0))
            snake.show_snake()
            apple.show_apple()
            pygame.display.update()
            self.clock.tick(30)



if __name__ == "__main__":
    config = GameConfig
    game=Game()
    model = tf.keras.models.load_model('save.h5')
    game.play(model)


