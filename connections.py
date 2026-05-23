import asyncio
import os

import pygame

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
pygame.mixer.music.load("taconnector1.wav")
pygame.mixer.music.play()  # Loop indefinitely
pygame.mixer.music.queue("taconnector2.wav")
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
fps = 60
fpsClock = pygame.time.Clock()


async def main():
    def load(filename):
        filename = pygame.image.load(os.path.join(f"{filename}.png")).convert_alpha()
        return filename

    tomato = [load("tomato"), 50, 30, 5, 5, 60, 0]
    dill_pickle = [load("dill_pickle"), 5, 80, 5, 70, 20, 0]
    radicchio = [load("radicchio"), 5, 10, 90, 5, 15, 1]
    corned_beef = [load("corned_beef"), 5, 5, 5, 85, 90, 0]
    pickled_jalapenos = [None, 10, 75, 10, 55, 20, 2]
    lemon = [load("lemon"), 10, 90, 25, 0, 0, 0]
    chili_flakes = [load("chili_flakes"), 0, 5, 15, 5, 15, 3]
    guacamole = [load("guacamole"), 10, 30, 5, 25, 55, 0]
    soy_sauce = [None, 5, 15, 10, 90, 65, 0]
    honey = [None, 90, 5, 0, 0, 5, 0]
    arrabbiata_sauce = [
        load("arrabbiata_sauce"),
        60,
        40,
        10,
        30,
        65,
        2,
        tomato,
        chili_flakes,
    ]
    carne_deshebrada = [
        load("carne_deshebrada"),
        13,
        70,
        10,
        65,
        85,
        0,
        corned_beef,
        lemon,
    ]
    cowboy_candy = [None, 80, 60, 15, 50, 30, 2, pickled_jalapenos, honey]
    radicchio_cream = [None, 15, 15, 70, 35, 55, 1, radicchio, guacamole]
    shoyuzuke = [None, 25, 65, 10, 80, 80, 0, dill_pickle, soy_sauce]
    taco = load("taco")
    food_positions = [
        (140, 36),
        (340, 36),
        (540, 36),
        (740, 36),
        (940, 36),
    ]  # food size + space in between should be 200 pixels
    all_foods = [
        [tomato, dill_pickle, radicchio, corned_beef, pickled_jalapenos],
        [chili_flakes, lemon, guacamole, soy_sauce, honey],
        [arrabbiata_sauce, carne_deshebrada, cowboy_candy, radicchio_cream, shoyuzuke],
    ]
    main_cooking_area = [(440, 300), (840, 700)]
    food_in_cooking_area = []
    foods_shown = all_foods[0]
    holding_item = False
    running = True

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    """this is the left click handler, mouse pos is now a (x,y) tuple"""
                    if holding_item:
                        if (
                            mouse_pos[0] >= main_cooking_area[0][0]
                            and mouse_pos[0] <= main_cooking_area[1][0]
                        ):
                            if (
                                mouse_pos[1] >= main_cooking_area[0][1]
                                and mouse_pos[1] <= main_cooking_area[1][1]
                            ):
                                food_in_cooking_area.append(holding_item)
                                holding_item = False
                                print(
                                    "To implement: add sprites and put down a sprite in this case"
                                )
                    if mouse_pos[1] < 237 and mouse_pos[1] > 35:
                        for box in food_positions:
                            if mouse_pos[0] < box[1] + 201 and mouse_pos[0] >= box[0]:
                                holding_item = foods_shown[food_positions.index(box)]

        screen.blit(taco, main_cooking_area[0])
        pygame.display.flip()
        fpsClock.tick(fps)
        await asyncio.sleep(0)
    pygame.quit()


asyncio.run(main())
