import pygame
import random
import pygame_menu
from pygame_menu import themes

pygame.init()

WIDTH = 800
HEIGHT = 600
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 102)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def our_snake(snake_block, snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], snake_block, snake_block])

def message(msg, color, y_offset=0):
    msg_surface = font_style.render(msg, True, color)
    msg_rect = msg_surface.get_rect(center=(WIDTH/2, HEIGHT/2 + y_offset))
    screen.blit(msg_surface, msg_rect)

def show_score(score):
    value = score_font.render("Счёт: " + str(score), True, YELLOW)
    screen.blit(value, [0, 0])

def game_loop(player_name):
    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    clock = pygame.time.Clock()

    while not game_over:
        while game_close:
            screen.fill(BLUE)
            message("Вы проиграли!", RED, -30)
            message(f"Игрок: {player_name} | Счёт: {length_of_snake - 1}", WHITE, 20)
            message("Нажмите C для повтора или Q для выхода", WHITE, 70)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        return game_loop(player_name)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLUE)

        pygame.draw.rect(screen, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        our_snake(SNAKE_BLOCK, snake_list)
        show_score(length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

def start_game():
    player_name = name_input.get_value()
    if not player_name:
        player_name = "Игрок"
    game_loop(player_name)

def main_menu():
    menu = pygame_menu.Menu(
        title="Змейка",
        width=WIDTH,
        height=HEIGHT,
        theme=themes.THEME_DARK
    )

    global name_input
    name_input = menu.add.text_input(
        "Имя игрока:",
        default="Игрок",
        maxchar=20,


font_size=20
    )
    menu.add.selector(
        "Сложность:",
        [("Нормальная", 15), ("Быстрая", 25), ("Медленная", 10)],
        onchange=lambda _, value: change_speed(value)
    )
    menu.add.button("Старт", start_game)
    menu.add.button("Выход", pygame_menu.events.EXIT)

    menu.mainloop(screen)

def change_speed(new_speed):
    global SNAKE_SPEED
    SNAKE_SPEED = new_speed

if __name__ == "__main__":
    main_menu()