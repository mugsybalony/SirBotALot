import time
import pygame
import os
import cv2
from PIL import Image
import numpy as np
from picMatching import find_hidden_on_screen
from picMatching import cards_on_screen
import pyautogui
from Monte_Carlo import run_sim
from pytesseract import image_to_string
import pytesseract
import re

if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
else:
    pass


def find_stuff():
    no_players = 0
    hand = []
    #take a screenshot
    #os.system("screencapture screen.png")

    #screen = 'screen.png'
    if os.name != "nt":
        cardpath = 'ps/backofcards2.png'
    else:
        cardpath = 'ps/backcardswayne.png'

    #take a screenshot of the area where the baord is and find the board
    img = pyautogui.screenshot(region=(260, 219, 275, 50))
    img.save('smallscreen.png')
    cards = []
    cards = cards_on_screen('smallscreen.png')
    #returns cards and their coordinates so we need to extract just the cards
    try:
        cards = [cards[x][0] for x in range(len(cards))]
    except:
        pass

    #find our hand
    img = pyautogui.screenshot(region=(347, 375, 100, 50))
    img.save('hand.png')
    hand = []
    hand = cards_on_screen('hand.png')
    try:
        hand = [hand[x][0] for x in range(len(hand))]
    except:
        pass


    #find the pot and convert the image to text
    img = pyautogui.screenshot(region=(350, 191, 100, 30))
    img.save('pot.png')
    pot = image_to_string(Image.open('pot.png'))
    #conver the por to string
    non_dec = re.compile(r'[^\d.]+')
    pot = non_dec.sub('', pot)
    print 'pot is %s ' %pot

    #find the number of opponents
    #screenshot1 = Image.open(screen) - commented out 06/11
    screenshot1 = pyautogui.screenshot('screen.png')
    screenshot = cv2.cvtColor(np.array(screenshot1), cv2.COLOR_BGR2RGB)
    card = Image.open(cardpath)
    coveredcard = cv2.cvtColor(np.array(card), cv2.COLOR_BGR2RGB)
    no_players = find_hidden_on_screen(coveredcard, screenshot)

    return no_players, cards, hand, pot


def update_gui(no_players, cards, hand, prob, equity):
    screen.fill(background_colour) #use this if you need to wipe the whole background
    font = pygame.font.Font(None,20)


    text1 = font.render("Number of players %s" %no_players, 1, (0,0,0),(255,255,255))
    textpos = text1.get_rect()
    screen.blit(text1,textpos)

    text2 = font.render("Cards on the board %s" % cards, 1, (50, 50, 50),(255,255,255))
    textpos = text2.get_rect()
    screen.blit(text2, (0,font.get_height()))

    text3 = font.render("Probability of winning is: %s" % prob, 1, (50, 50, 50), (255, 255, 255))
    textpos = text3.get_rect()
    screen.blit(text3, (0, font.get_height()*2))

    text4 = font.render("your hand is: %s" % hand, 1, (50, 50, 50), (255, 255, 255))
    textpos = text4.get_rect()
    screen.blit(text4, (0, font.get_height() * 3))

    text5 = font.render("Odds * pot = : %s" % equity, 1, (50, 50, 50), (255, 255, 255))
    textpos = text5.get_rect()
    screen.blit(text5, (0, font.get_height() * 4))

    text6 = font.render("Pot = : %s" % pot, 1, (50, 50, 50), (255, 255, 255))
    textpos = text6.get_rect()
    screen.blit(text6, (0, font.get_height() * 5))

    pygame.display.flip()


def calc_odds(player1_hand, no_players, cards, percentile):


    percentile = 20
    board = cards

    wins = 0.0
    percentile = 0
    t0 = time.time()
    for i in range(0, 1500):
        winornot = run_sim(player1_hand, no_players, board, percentile)
        wins += winornot
    odds = (wins/1500)
    t1 = time.time()
    t = t1-t0
    print 'odds found in %s seconds' %t
    print odds

    return odds


def equity_calc(prob,pot):
    try:
        equity = float(pot)*prob
    except:
        equity = 0
    return equity

def init_window():
    global screen, background_colour

    pygame.init()
    (width, height) = (500, 200)
    background_colour = (200, 200, 255)

    screen = pygame.display.set_mode((width, height))
    screen.fill(background_colour)
    pygame.display.flip()
    pygame.display.set_caption('PokeyBotty')

    global running
    running = True



#initialise the window for rendering output
init_window()

while running:
    #event handling section of the while loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    no_players, cards, hand,pot = find_stuff()
    prob = calc_odds(hand, no_players, cards, 0)
    equity = equity_calc(prob,pot)

    update_gui(no_players,cards, hand, prob,equity)

    print 'looped'


