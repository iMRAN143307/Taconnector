import asyncio
import os

import pygame

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.mixer.music.load("taconnector1.wav")
pygame.mixer.music.play(-1)  # Loop indefinitely
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
fps = 60
fpsClock = pygame.time.Clock()


async def main():
    def load(filename):
        filename = pygame.image.load(os.path.join(f"{filename}.png")).convert_alpha()
        return filename

    tomato = [load("tomato")]
    dill_pickle = [load("dill_pickle")]
    radicchio = [load("radicchio")]
    corned_beef = [load("corned_beef")]
    pickled_jalapenos = [None]
    lemon = [load("lemon")]
    chili_flakes = [load("chili_flakes")]
    guacamole = [load("guacamole")]
    soy_sauce = [None]
    honey = [None]
    arrabbiata_sauce = [load("arrabbiata_sauce"), tomato, chili_flakes]
    carne_deshebrada = [load("carne_deshebrada"), corned_beef, lemon]
    cowboy_candy = [None, pickled_jalapenos, honey]
    radicchio_cream = [None, radicchio, guacamole]
    shoyuzuke = [None, dill_pickle, soy_sauce]
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
