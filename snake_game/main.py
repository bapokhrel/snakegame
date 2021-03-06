import pygame
from pygame.locals import *
"""pygame.locals imports certain global variables. Consult pygame documentation for details"""
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)
START_CELL = 3


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * random.randint(0, 23)
        self.y = SIZE * random.randint(0, 13)
    
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        """deriving value of x and y by dividing our screen size 1000 and 800"""
        self.x = random.randint(0, 23) * SIZE
        self.y = random.randint(0, 13) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'

        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def draw(self):
        """Event Loop. Until press ESC for example, continue the process"""
        for i in range(self.length):
            """Draw a block using blit function at coordinates block_x and block_y"""
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        """flip() in pygame.display.flip means update the screen always after anything is updated"""
        pygame.display.flip()

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Cidebasucs Snake and Apple Game")
        self.surface = pygame.display.set_mode((960, 560))

        pygame.mixer.init()
        self.play_background_music()
        """color value is rgb only"""
        self.surface.fill((110, 110, 5))
        self.snake = Snake(self.surface, START_CELL)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length - START_CELL}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        """Draw background from coordinate 0,0"""
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Snake colliding with the Apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # Snake colliding itself
        for i in range(START_CELL - 1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise Exception

        # Snake colliding with the wall
        if not (0 <= self.snake.x[0] <= 960 and 0 < self.snake.y[0] <= 560):
            self.play_sound("crash")
            raise Exception("You hit the boundary waall")


    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your Score is {self.snake.length - START_CELL}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play  again press Enter. To exit press ESC", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, START_CELL)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        """In pygame.event, event listens for keyboard / mouse inputs"""
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.3)


if __name__ == "__main__":
    game = Game()
    game.run()
