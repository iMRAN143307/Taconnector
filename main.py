import asyncio
import os
import random

import pygame

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
song0 = "taconnector1.wav"
song1 = "taconnector2.wav"

playlist = [song0, song1]
pygame.mixer.music.load(song0)
pygame.mixer.music.play()
SONG_END = pygame.USEREVENT + 1
DRAG_MOUSE = pygame.USEREVENT + 2
CUSTOMER_LOSE = pygame.USEREVENT + 3
CUSTOMER_WIN = pygame.USEREVENT + 4
CHECK = pygame.USEREVENT + 5
SUBMIT = pygame.USEREVENT + 6
pygame.mixer.music.set_endevent(SONG_END)
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
fps = 60
fpsClock = pygame.time.Clock()


async def main():
    def load(filename):
        filename = pygame.image.load(os.path.join(f"{filename}.png")).convert_alpha()
        return filename

    def load_and_scale(filename):
        unscaled = pygame.image.load(os.path.join(f"{filename}.png")).convert()
        return pygame.transform.scale(unscaled, (1280, 720))

    current_index = 0
    background = load_and_scale("background")
    arrow_left = load("arrow_left")
    arrow_right = load("arrow_right")
    tomato = [load("tomato"), load("tomatoicon"), 50, 30, 5, 5, 60, 0]
    dill_pickle = [load("dill_pickle"), load("dill_pickleicon"), 5, 80, 20, 70, 20, 0]
    radicchio = [load("radicchio"), load("radicchioicon"), 5, 10, 90, 5, 15, 1]
    corned_beef = [load("corned_beef"), load("corned_beeficon"), 5, 5, 5, 85, 90, 0]
    pickled_jalapenos = [
        load("pickled_jalapenos"),
        load("pickled_jalapenosicon"),
        10,
        75,
        10,
        55,
        20,
        2,
    ]
    lemon = [load("lemon"), load("lemonicon"), 10, 90, 30, 0, 0, 0]
    chili_flakes = [load("chili_flakes"), load("chili_flakesicon"), 0, 5, 15, 5, 15, 3]
    guacamole = [load("guacamole"), load("guacamoleicon"), 10, 30, 5, 25, 55, 0]
    soy_sauce = [load("soy_sauce"), load("soy_sauceicon"), 5, 15, 35, 90, 65, 0]
    honey = [load("honey"), load("honeyicon"), 90, 5, 0, 0, 5, 0]
    arrabbiata_sauce = [
        load("arrabbiata_sauce"),
        load("arrabbiata_sauceicon"),
        60,
        40,
        10,
        30,
        65,
        2,
        tomato,
        chili_flakes,
    ]
    shredded_beef = [
        load("shredded_beef"),
        load("shredded_beeficon"),
        15,
        70,
        30,
        65,
        85,
        0,
        corned_beef,
        lemon,
    ]
    cowboy_candy = [
        load("cowboy_candy"),
        load("cowboy_candyicon"),
        80,
        60,
        15,
        50,
        30,
        2,
        pickled_jalapenos,
        honey,
    ]
    radicchio_cream = [
        load("radicchio_cream"),
        load("radicchio_creamicon"),
        15,
        15,
        70,
        35,
        55,
        1,
        radicchio,
        guacamole,
    ]
    soy_pickle = [
        load("soy_pickle"),
        load("soy_pickleicon"),
        25,
        65,
        30,
        80,
        80,
        0,
        dill_pickle,
        soy_sauce,
    ]
    taco = load("taco")
    food_positions = [
        (140, 36),
        (340, 36),
        (540, 36),
        (740, 36),
        (940, 36),
    ]
    all_foods = [
        [tomato, dill_pickle, radicchio, corned_beef, pickled_jalapenos],
        [chili_flakes, lemon, guacamole, soy_sauce, honey],
        [arrabbiata_sauce, shredded_beef, cowboy_candy, radicchio_cream, soy_pickle],
    ]
    all_customers = [
        ["Sweet with a little kick", 60, 30, 20, 20, 20, 2],
        ["As bitter as their mood", 0, 20, 70, 20, 20, 0],
        ["Salty as the sea, with no spice", 10, 20, 20, 65, 35, -1],
        ["All in on savoury and spicy", 25, 20, 20, 25, 60, 3],
        ["Sour with a pleasant aftertaste", 40, 70, 20, 20, 40, 0],
    ]
    current_customer = all_customers[random.randint(0, 4)]
    main_cooking_area = [(440, 300), (840, 700)]
    food_in_cooking_area = []
    cycle_food = int(0)
    foods_shown = all_foods[cycle_food]
    holding_item = False
    running = True
    mouse_released = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = mouse_pos[0] - 32, mouse_pos[1] - 32
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if (mouse_pos[0] - 610) ** 2 + (mouse_pos[1] - 480) ** 2 <= 210**2:
                    mouse_released = True
                    holding_item = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (mouse_pos[0] - 610) ** 2 + (mouse_pos[1] - 480) ** 2 <= 210**2:
                        if holding_item is not None:
                            food_in_cooking_area.append((holding_item, mouse_pos))
                        mouse_released = False
                        pygame.time.set_timer(DRAG_MOUSE, 25)
                    if mouse_pos[1] < 237 and mouse_pos[1] > 35:
                        for i, box in enumerate(food_positions):
                            if mouse_pos[0] < box[0] + 201 and mouse_pos[0] >= box[0]:
                                holding_item = foods_shown[i]
                    if mouse_pos[1] < 203 and mouse_pos[1] > 61:
                        if mouse_pos[0] >= 0 and mouse_pos[0] < 141:
                            cycle_food -= 1
                            cycle_food = cycle_food % 3
                            foods_shown = all_foods[cycle_food]
                        elif mouse_pos[0] > 1141 and mouse_pos[0] <= 1280:
                            cycle_food += 1
                            cycle_food = cycle_food % 3
                            foods_shown = all_foods[cycle_food]
            if event.type == SONG_END:
                current_index = (current_index + 1) % len(playlist)
                pygame.mixer.music.load(playlist[current_index])
                pygame.mixer.music.play()
            if event.type == DRAG_MOUSE:
                if (mouse_pos[0] - 610) ** 2 + (mouse_pos[1] - 480) ** 2 <= 210**2:
                    if not mouse_released:
                        if holding_item is not None:
                            food_in_cooking_area.append((holding_item, mouse_pos))
                        pygame.time.set_timer(DRAG_MOUSE, 25)
            if event.type == SUBMIT:
                pass
            if event.type == CHECK:
                sweet = [0, 0]
                sour = [0, 0]
                bitter = [0, 0]
                salty = [0, 0]
                savoury = [0, 0]
                spicy = [0, 0]
                for obj in food_in_cooking_area:
                    obj = obj[0]
                    sweet[0] += obj[2]
                    sweet[1] += 1
                    sour[0] += obj[3]
                    sour[1] += 1
                    bitter[0] += obj[4]
                    bitter[1] += 1
                    salty[0] += obj[5]
                    salty[1] += 1
                    savoury[0] += obj[6]
                    savoury[1] += 1
                    spicy[0] += obj[7]
                    spicy[1] += 1
                sweet = sweet[0] // sweet[1]
                sour = sour[0] // sour[1]
                bitter = bitter[0] // bitter[1]
                salty = salty[0] // salty[1]
                savoury = savoury[0] // savoury[1]
                spicy = round(spicy[0] / spicy[1])
                flavour_profile = [sweet, sour, bitter, salty, savoury, spicy]
                if flavour_profile[0] > current_customer[1] + 10:
                    print("too sweet")
                elif flavour_profile[0] < current_customer[1] - 10:
                    print("not sweet enough")
                if flavour_profile[1] > current_customer[2] + 10:
                    print("too sour")
                elif flavour_profile[1] < current_customer[2] - 10:
                    print("not sour enough")
                if flavour_profile[2] > current_customer[3] + 10:
                    print("too bitter")
                elif flavour_profile[2] < current_customer[3] - 10:
                    print("not bitter enough")
                if flavour_profile[3] > current_customer[4] + 10:
                    print("too salty")
                elif flavour_profile[3] < current_customer[4] - 10:
                    print("not salty enough")
                if flavour_profile[4] > current_customer[5] + 10:
                    print("too savoury")
                elif flavour_profile[4] < current_customer[5] - 10:
                    print("not savoury enough")
                if flavour_profile[5] > current_customer[6] + 1:
                    print("too spicy")
                elif flavour_profile[5] < current_customer[6] - 1:
                    print("not spicy enough")
        screen.blit(background, (0, 0))
        screen.blit(taco, main_cooking_area[0])
        screen.blit(arrow_left, (0, 62))
        screen.blit(arrow_right, (1140, 62))
        for i, food in enumerate(foods_shown):
            screen.blit(food[0], food_positions[i])
        for i, obj in enumerate(food_in_cooking_area):
            screen.blit(obj[0][1], obj[1])
        if holding_item:
            screen.blit(holding_item[1], mouse_pos)
        pygame.display.flip()
        fpsClock.tick(fps)
        await asyncio.sleep(0)
    pygame.mixer.music.stop()
    pygame.quit()


asyncio.run(main())
