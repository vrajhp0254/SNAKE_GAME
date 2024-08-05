import pygame
import random
import os

pygame.mixer.init()

pygame.init()

# Colors
white = (255, 255, 255)
red = (225, 0, 0)
black = (0, 0, 0)


screen_width = 900
screen_height = 600
gamewindow = pygame.display.set_mode((screen_width, screen_height))

bgimg=pygame.image.load("gianpaolo-antonucci-gt7C42J1P6g-unsplash.jpg")
bgimg =pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

pygame.display.set_caption("snake game")
pygame.display.update()


clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gamewindow.blit(screen_text, [x, y])


def plot_snake(gamewindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gamewindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gamewindow.fill(white)
        text_screen("Welcome to my game! ", red, 200, 250)
        text_screen("Press spacebar to play", red, 200, 300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
#                     pygame.mixer.music.load("back.mp3")
#                     pygame.mixer.music.play()
                    gameloop()
        pygame.display.update()
        clock.tick(60)


def gameloop():
    snake_x = 45
    snake_y = 55

    velocity_x = 0
    velocity_y = 0

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)

    snake_size = 20
    score = 0
    init_velocity = 4
    fps = 60

    snk_list = []
    snk_length = 1

    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0")
    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    exit_game = False
    game_over = False
    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            text_screen("game over press enter to restart", red, 200, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_t:
                        score += 100

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score += 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 5

            if score > int(hiscore):
                hiscore = score

            gamewindow.fill(white)
            gamewindow.blit(bgimg,(0,0))
            text_screen(
                "score = " + str(score) + "hiscore=" + str(hiscore), red, 375, 550
            )
            pygame.draw.rect(gamewindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if (
                snake_x < 0
                or snake_x > screen_width
                or snake_y < 0
                or snake_y > screen_height
            ):
                game_over = True
#                 pygame.mixer.music.load("back.mp3")
#                 pygame.mixer.music.play()

            if head in snk_list[:-1]:
                game_over = True
#                 pygame.mixer.music.load("back.mp3")
#                 pygame.mixer.music.play()

        plot_snake(gamewindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
