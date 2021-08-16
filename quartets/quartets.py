import random

import pygame
import math

# region consts
COLORS = ["orange", "purple", "cyan", "green"]  # , "", "", ""]
SHAPES = ["pentagon", "rectangle", "triangle", "circle"]
CARDS = ["card", "card_back"]
JOKER = "joker"
QUESTION = "question"
CARD = "card"

WIDTH = 800
HEIGHT = 600
PX = math.sqrt(math.sqrt(WIDTH * HEIGHT)) * 2
PLAYER_COUNT = 4
#endregion

pygame.init()
player_id = 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))


def setup_deck():
    """
    The function returns a deck.
    :return: list of dicts.
    """
    li = []
    for color in COLORS:
        for shape in SHAPES:
            li.append({"pos": (0, 0), "show": True, "color": color, "shape": shape, "type": CARD})
        li.append({"pos": (0, 0), "show": True, "color": color, "shape": JOKER, "type": CARD})
    return li


def setup_images():
    """
    The function returns a dictionary with all of the images loaded.
    :return: dict.
    """
    out = {}
    for asset in COLORS + SHAPES + [JOKER, QUESTION] + CARDS:
        # load and rescale the pixel art
        out[asset] = pygame.transform.scale(pygame.image.load(f"assets/{asset}.png"), (int(PX), int(1.4 * PX)))
    return out


def setup_hands():
    """
    The function setups 4 hands.
    :return: hands list of lists of cards.
    """
    out = []
    for i in range(PLAYER_COUNT):  # 4 is the number of players
        out.append([deck.pop(0)])
        for j in range(PLAYER_COUNT - 1):
            out[i].append(deck.pop(0))
    return out


def setup_questions():
    out = []
    for i in range(PLAYER_COUNT):
        if i % 2 == 0:
            out.append({"pos": (WIDTH/2 - PX*0.5, HEIGHT + (-1 * bool(i)) * (1.4*PX*1.5)), "type": QUESTION, "size": (PX, PX)})
        else:
            out.append({"pos": (WIDTH + (-1 * bool(i)) * (1.4*PX*1.5), HEIGHT/2 - PX*0.7), "type": QUESTION, "size": (PX, PX)})
    return out


imgs = setup_images()
clickables = []
questions = setup_questions()


def show_card(card):
    """
    The function shows a card.
    :param card: dict.
    """
    if card["show"]:
        screen.blit(imgs["card"], card["pos"])
        screen.blit(imgs[card["color"]], card["pos"])
        screen.blit(imgs[card["shape"]], card["pos"])
    else:
        screen.blit(imgs["card_back"], card["pos"])


def show_hands():
    """
    The function shows the cards of hands
    :return:
    """
    for i in range(len(hands)):
        for j in range(len(hands[i])):
            card = hands[i][j]

            """
            if i == player_id:
                card["show"] = True
            else:
                card["show"] = False"""

            if i % 2 == 0:
                card["pos"] = (int(WIDTH/2 - PX*len(hands[i])/2 + j*PX + j*PX*0.2), int((HEIGHT - PX*1.4) * bool(i)))
            else:
                card["pos"] = (int((WIDTH - PX) * bool(i-1)), int(HEIGHT/2 - PX*1.4*len(hands[i])/2 + j*PX*1.4 + j*PX*1.4*0.2))
            show_card(card)


def pick_from_list(li):
    """
    The function shows the player his options.
    :param li: a list.
    """
    global clickables
    item = None
    clickables = []
    for i in range(len(li)):
        w = PX
        h = PX * 1.4
        x = int(WIDTH/2 - w * ((len(li)/2 - i) * 1.2) + i * 0.2 * w)  # 1.2 for margin
        y = int(HEIGHT - h*2)
        clickables.append({"type": CARD, "show": True, "color": li[i], "shape": li[i], "pos": (x, y), "size": (w, h)})
        show_card(clickables[i])


def draw_card(player):
    hands[player].append(deck.pop(0))


def end_turn(player):
    global choice, turn
    turn += 1
    turn %= PLAYER_COUNT
    choice = {"player": -1, "color": None, "shape": None}


def onclick():
    global clickables
    for ca in clickables:
        if ca["pos"][0] < mouse_pos[0] < ca["pos"][0] + ca["size"][0]:
            if ca["pos"][1] < mouse_pos[1] < ca["pos"][1] + ca["size"][1]:
                if ca["type"] == QUESTION:
                    choice["player"] = questions.index(ca)
                elif ca["color"] in COLORS:
                    choice["color"] = ca["color"]
                    if not any(card["color"] == ca["color"] for card in hands[choice["player"]]):
                        draw_card(choice["player"])
                        end_turn(choice["player"])

                    # detect joker
                    for card in hands[choice["player"]]:
                        if card["shape"] == JOKER and card["color"] == choice["color"]:
                            hands[turn].append(hands[choice["player"]].pop(hands[choice["player"]].index(card)))
                            end_turn(turn)
                            break
                elif ca["shape"] in SHAPES:
                    choice["shape"] = ca["shape"]
                clickables = []

deck = setup_deck()
deck_place = (WIDTH/2, HEIGHT/2 - PX*1.4/2)
random.shuffle(deck)

mouse_pos = None
hands = setup_hands()
turn = 2
choice = {"player": -1, "color": None, "shape": None}


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            onclick()

    screen.fill((50, 100, 50))

    if len(deck) > 0:
        show_card({"show": False, "pos": deck_place})

    show_hands()

    for ca in clickables:
        if ca["type"] == CARD:
            show_card(ca)
        elif ca["type"] == QUESTION:
            screen.blit(imgs[ca["type"]], ca["pos"])

    if turn == player_id and len(clickables) == 0:
        if choice["player"] == -1:
            for q in questions:
                clickables.append(q)
        elif choice["color"] is None:
            pick_from_list(COLORS)
        elif choice["shape"] is None:
            pick_from_list(SHAPES)
        else:
            for card in hands[choice["player"]]:
                if card["shape"] == choice["shape"] and card["color"] == choice["color"]:
                    hands[turn].append(hands[choice["player"]].pop(hands[choice["player"]].index(card)))
    pygame.display.update()


pygame.quit()
