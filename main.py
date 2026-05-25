import asyncio
import os
import random
import sys

import pygame

SONG_END = pygame.USEREVENT + 1
DRAG_MOUSE = pygame.USEREVENT + 2
CUSTOMER_LOSE = pygame.USEREVENT + 3
CUSTOMER_WIN = pygame.USEREVENT + 4
CHECK = pygame.USEREVENT + 5
SUBMIT = pygame.USEREVENT + 6
CLEAR = pygame.USEREVENT + 7
fpsClock = pygame.time.Clock()


def resource_path(relative_path):
    try:
        base_path = sys.MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


async def main():
    def load(filename):
        image_path = resource_path(f"{filename}.png")
        return pygame.image.load(image_path).convert_alpha()

    def load_and_scale(filename):
        unscaled = pygame.image.load(resource_path(f"{filename}.png")).convert()
        return pygame.transform.scale(unscaled, (1280, 720))

    pygame.init()
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))
    song0 = "taconnector1.ogg"
    song1 = "taconnector2.ogg"
    song2 = "taconnector3.ogg"
    playlist = [song0, song1, song2]
    pygame.mixer.music.set_endevent(SONG_END)
    pygame.mixer.music.load(song0)
    font = pygame.font.Font("Lato.ttf", 38)
    clear = 0
    to_say = []
    current_index = 0
    background = load_and_scale("background")
    arrow_left = load("arrow_left")
    arrow_right = load("arrow_right")
    submit_button = load("submit_button")
    check_button = load("check_button")
    check_buttonused = load("check_buttonused")
    locked = load("locked")
    tomato = [load("tomato"), load("tomatoicon"), 50, 30, 5, 5, 60, 0, "tomato"]
    dill_pickle = [
        load("dill_pickle"),
        load("dill_pickleicon"),
        5,
        80,
        20,
        70,
        20,
        0,
        "dill_pickle",
    ]
    radicchio = [
        load("radicchio"),
        load("radicchioicon"),
        5,
        10,
        90,
        5,
        15,
        1,
        "radicchio",
    ]
    corned_beef = [
        load("corned_beef"),
        load("corned_beeficon"),
        5,
        5,
        5,
        85,
        90,
        0,
        "corned_beef",
    ]
    pickled_jalapenos = [
        load("pickled_jalapenos"),
        load("pickled_jalapenosicon"),
        10,
        75,
        10,
        55,
        20,
        2,
        "pickled_jalapenos",
    ]
    lemon = [load("lemon"), load("lemonicon"), 10, 90, 30, 0, 0, 0, "lemon"]
    chili_flakes = [
        load("chili_flakes"),
        load("chili_flakesicon"),
        0,
        5,
        15,
        5,
        15,
        3,
        "chili_flakes",
    ]
    guacamole = [
        load("guacamole"),
        load("guacamoleicon"),
        15,
        30,
        15,
        25,
        60,
        0,
        "guacamole",
    ]
    soy_sauce = [
        load("soy_sauce"),
        load("soy_sauceicon"),
        5,
        15,
        35,
        90,
        65,
        0,
        "soy_sauce",
    ]
    honey = [load("honey"), load("honeyicon"), 90, 5, 0, 0, 5, 0, "honey"]
    arrabbiata_sauce = [
        load("arrabbiata_sauce"),
        load("arrabbiata_sauceicon"),
        60,
        40,
        10,
        30,
        65,
        2,
        "arrabbiata_sauce",
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
        "shredded_beef",
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
        "cowboy_candy",
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
        "radicchio_cream",
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
        "soy_pickle",
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
        [locked, locked, locked, locked, locked],
    ]
    all_customers = [
        ["sweet with a little kick", 60, 30, 20, 20, 20, 2],
        ["as bitter as their mood", 0, 20, 70, 20, 20, 1],
        ["salty as the sea, with no spice", 10, 20, 20, 65, 35, -1],
        ["all in on savoury and spicy", 25, 20, 20, 25, 60, 3],
        ["sour with a pleasant aftertaste", 40, 70, 20, 20, 40, 0],
    ]
    current_customer = all_customers[random.randint(0, 4)]
    main_cooking_area = [(440, 300), (840, 700)]
    food_in_cooking_area = []
    cycle_food = int(0)
    foods_shown = all_foods[cycle_food]
    holding_item = None
    running = True
    mouse_released = True
    can_check = 3
    intermission = False
    first_locked_food = 0
    arrabbiata_sauce_unlocked = False
    soy_pickle_unlocked = False
    shredded_beef_unlocked = False
    cowboy_candy_unlocked = False
    radicchio_cream_unlocked = False
    first_click = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = mouse_pos[0] - 32, mouse_pos[1] - 32
        if intermission:
            combining_food = list(set(tuple([x[0][8] for x in food_in_cooking_area])))
            if len(combining_food) == 2:
                combining_food = list(set((combining_food[0], combining_food[1])))
                if (
                    "dill_pickle" in combining_food
                    and "soy_sauce" in combining_food
                    and not soy_pickle_unlocked
                ):
                    all_foods[2][first_locked_food] = soy_pickle
                    first_locked_food += 1
                    combining_food = []
                    soy_pickle_unlocked = True
                elif (
                    "tomato" in combining_food
                    and "chili_flakes" in combining_food
                    and not arrabbiata_sauce_unlocked
                ):
                    all_foods[2][first_locked_food] = arrabbiata_sauce
                    first_locked_food += 1
                    combining_food = []
                    arrabbiata_sauce_unlocked = True
                elif (
                    "lemon" in combining_food
                    and "corned_beef" in combining_food
                    and not shredded_beef_unlocked
                ):
                    all_foods[2][first_locked_food] = shredded_beef
                    first_locked_food += 1
                    combining_food = []
                    shredded_beef_unlocked = True
                elif (
                    "pickled_jalapenos" in combining_food
                    and "honey" in combining_food
                    and not cowboy_candy_unlocked
                ):
                    all_foods[2][first_locked_food] = cowboy_candy
                    first_locked_food += 1
                    combining_food = []
                    cowboy_candy_unlocked = True
                elif (
                    "radicchio" in combining_food
                    and "guacamole" in combining_food
                    and not radicchio_cream_unlocked
                ):
                    all_foods[2][first_locked_food] = radicchio_cream
                    first_locked_food += 1
                    combining_food = []
                    radicchio_cream_unlocked = True
                intermission = False
                pygame.event.post(pygame.event.Event(CLEAR))
                clear = 10
                combining_food = []
                current_customer = all_customers[random.randint(0, 4)]
                to_say = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == CUSTOMER_LOSE:
                can_check = 3
                pygame.event.post(pygame.event.Event(CLEAR))
                clear = 10
                current_customer = all_customers[random.randint(0, 4)]
                to_say = []
            if event.type == CUSTOMER_WIN:
                can_check = 3
                pygame.event.post(pygame.event.Event(CLEAR))
                clear = 10
                current_customer = all_customers[random.randint(0, 4)]
                if (
                    not arrabbiata_sauce_unlocked
                    or not soy_pickle_unlocked
                    or not cowboy_candy_unlocked
                    or not radicchio_cream_unlocked
                    or not shredded_beef_unlocked
                ):
                    to_say = [
                        "put two foods on",
                        "the taco to be",
                        "connected together",
                        "into a new ingredient",
                    ]
                    intermission = True
            if event.type == pygame.MOUSEBUTTONUP:
                clickx, clicky = event.pos
                if (clickx - 610) ** 2 + (clicky - 480) ** 2 <= 210**2:
                    mouse_released = True
                    holding_item = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickx, clicky = event.pos
                if event.button == 1:
                    if first_click:
                        try:
                            first_click = False
                            pygame.mixer.music.play()
                        except Exception:
                            pass
                    if clicky >= 310 and clicky <= 410 and not intermission:
                        if mouse_pos[0] >= 64 and mouse_pos[0] <= 264:
                            if can_check != 0:
                                pygame.event.post(pygame.event.Event(CHECK))
                        if clickx >= 1016 and clickx <= 1216:
                            pygame.event.post(pygame.event.Event(SUBMIT))
                    if (clickx - 610) ** 2 + (clicky - 480) ** 2 <= 210**2:
                        if holding_item is not None:
                            food_in_cooking_area.append((holding_item, mouse_pos))
                        mouse_released = False
                        pygame.time.set_timer(DRAG_MOUSE, 25)
                    if clicky < 237 and clicky > 35:
                        for i, box in enumerate(food_positions):
                            if clickx < box[0] + 201 and clickx >= box[0]:
                                if foods_shown[i] != locked:
                                    holding_item = foods_shown[i]
                    if clicky < 203 and clicky > 61:
                        if clickx >= 0 and clickx < 141:
                            cycle_food -= 1
                            cycle_food = cycle_food % 3
                            foods_shown = all_foods[cycle_food]
                        elif clickx > 1141 and clickx <= 1280:
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
                tolerance = 1
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
                sweet = sweet[0] // max(sweet[1], 1)
                sour = sour[0] // max(sour[1], 1)
                bitter = bitter[0] // max(bitter[1], 1)
                salty = salty[0] // max(salty[1], 1)
                savoury = savoury[0] // max(savoury[1], 1)
                spicy = round(spicy[0] / max(spicy[1], 1))
                flavour_profile = [sweet, sour, bitter, salty, savoury, spicy]
                if flavour_profile[0] > current_customer[1] + 17:
                    tolerance -= 1
                elif flavour_profile[0] < current_customer[1] - 17:
                    tolerance -= 1
                if flavour_profile[1] > current_customer[2] + 17:
                    tolerance -= 1
                elif flavour_profile[1] < current_customer[2] - 17:
                    tolerance -= 1
                if flavour_profile[2] > current_customer[3] + 17:
                    tolerance -= 1
                elif flavour_profile[2] < current_customer[3] - 17:
                    tolerance -= 1
                if flavour_profile[3] > current_customer[4] + 17:
                    tolerance -= 1
                elif flavour_profile[3] < current_customer[4] - 17:
                    tolerance -= 1
                if flavour_profile[4] > current_customer[5] + 17:
                    tolerance -= 1
                elif flavour_profile[4] < current_customer[5] - 17:
                    tolerance -= 1
                if flavour_profile[5] > current_customer[6] + 1:
                    tolerance -= 1
                elif flavour_profile[5] < current_customer[6] - 1:
                    tolerance -= 1
                if tolerance >= 0:
                    pygame.event.post(pygame.event.Event(CUSTOMER_WIN))
                else:
                    pygame.event.post(pygame.event.Event(CUSTOMER_LOSE))
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
                sweet = sweet[0] // max(sweet[1], 1)
                sour = sour[0] // max(sour[1], 1)
                bitter = bitter[0] // max(bitter[1], 1)
                salty = salty[0] // max(salty[1], 1)
                savoury = savoury[0] // max(savoury[1], 1)
                spicy = round(spicy[0] / max(spicy[1], 1))
                flavour_profile = [sweet, sour, bitter, salty, savoury, spicy]
                to_say = []
                if flavour_profile[0] > current_customer[1] + 17:
                    to_say.append("too sweet")
                elif flavour_profile[0] < current_customer[1] - 17:
                    to_say.append("not sweet enough")
                if flavour_profile[1] > current_customer[2] + 17:
                    to_say.append("too sour")
                elif flavour_profile[1] < current_customer[2] - 17:
                    to_say.append("not sour enough")
                if flavour_profile[2] > current_customer[3] + 17:
                    to_say.append("too bitter")
                elif flavour_profile[2] < current_customer[3] - 17:
                    to_say.append("not bitter enough")
                if flavour_profile[3] > current_customer[4] + 17:
                    to_say.append("too salty")
                elif flavour_profile[3] < current_customer[4] - 17:
                    to_say.append("not salty enough")
                if flavour_profile[4] > current_customer[5] + 17:
                    to_say.append("too savoury")
                elif flavour_profile[4] < current_customer[5] - 17:
                    to_say.append("not savoury enough")
                if flavour_profile[5] > current_customer[6] + 1:
                    to_say.append("too spicy")
                elif flavour_profile[5] < current_customer[6] - 1:
                    to_say.append("not spicy enough")
                can_check -= 1
            if event.type == CLEAR:
                food_in_cooking_area = []
                clear -= 1
                if clear != 0:
                    pygame.event.post(pygame.event.Event(CLEAR))
        screen.blit(background, (0, 0))
        screen.blit(taco, main_cooking_area[0])
        screen.blit(arrow_left, (0, 62))
        screen.blit(arrow_right, (1140, 62))
        for i, food in enumerate(foods_shown):
            if food != locked:
                screen.blit(food[0], food_positions[i])
            else:
                screen.blit(
                    locked, (food_positions[i][0] + 32, food_positions[i][1] + 32)
                )
        for i, obj in enumerate(food_in_cooking_area):
            screen.blit(obj[0][1], obj[1])
        if holding_item:
            screen.blit(holding_item[1], mouse_pos)
        if not intermission:
            if can_check != 0:
                screen.blit(check_button, (64, 310))
            else:
                screen.blit(check_buttonused, (64, 310))
            screen.blit(submit_button, (1016, 310))
            screen.blit(
                font.render("The customer wants", True, (255, 255, 255)), (850, 590)
            )
            screen.blit(
                font.render("a taco that is", True, (255, 255, 255)),
                (920, 630),
            )
            screen.blit(
                font.render(current_customer[0], True, (255, 255, 255)), (775, 670)
            )
        for i, text in enumerate(to_say):
            screen.blit(font.render(text, True, (255, 255, 255)), (64, (410 + 50 * i)))
        pygame.display.flip()
        fpsClock.tick(60)
        await asyncio.sleep(0)
    pygame.mixer.music.stop()
    pygame.quit()


asyncio.run(main())
