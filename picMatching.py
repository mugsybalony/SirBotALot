import cv2
import numpy as np
from PIL import Image
import time
import os
#import pyscreenshot as ImageGrab

def find_templates_on_screen(template,screenshot):
    res = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)
    loc = np.where(res <= 0.005)
    ##0.005 for card faces
    w, h = template.shape[1],template.shape[0]
    #Qprint(loc)
    #print(type(loc))
    y = None
    for x1 in range(len(loc[0])):
        y = (loc[1][x1],loc[0][x1])
        cv2.rectangle(screenshot, y, (y[0] + w, y[1] + h), (0, 0, 255), 2)

    for pt in zip(*loc[::-1]):
        #print(pt)
        cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        cv2.imwrite('cards.png', screenshot)

        return pt

#find_templates_on_screen(template=template,screenshot=screenshot)
def cards_on_screen(screenshotpath):
    """
    :param screenshotpath: path to the screenshot
    :return: the list of cards appearing on the table with their locations
    """
    values = "23456789TJQKA"
    suites = "CDHS"

    t0 = time.time()
    screenshot1 = Image.open(screenshotpath)
    screenshot = cv2.cvtColor(np.array(screenshot1), cv2.COLOR_BGR2RGB)
    cards =[]

    for i in values:
        for j in suites:

            template1 = Image.open('ps/'+i+j+".png")
            template= cv2.cvtColor(np.array(template1), cv2.COLOR_BGR2RGB)
            c = find_templates_on_screen(template=template, screenshot=screenshot)
            cards.append((i+j, c))
            #print("card: "+i+j,c)

    t1 = time.time()
    print('Cards found in %s Seconds' % (round((t1 - t0), 2)))
    #print( len(cards))
    #print(cards)

    return [cards[a] for a in range(len(cards)) if cards[a][1] != None]

def find_hidden_on_screen(template,screenshot):
    res = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)
    if os.name != "nt":
        loc = np.where(res <= 0.1)
    else:
        loc = np.where(res <= 0.025)

    w, h = template.shape[1],template.shape[0]


    y = None
    numplayers = 0
    for x1 in range(len(loc[0])):
        y = (loc[1][x1],loc[0][x1])
        numplayers +=1
        cv2.rectangle(screenshot, y, (y[0] + w, y[1] + h), (0, 0, 255), 2)

    cv2.imwrite('cards.png', screenshot)

    return numplayers



def find_dealer(screenpath):
    dealerbutton = 'ps/dealerbutton.png'
    screen = Image.open(screenpath)
    screensh= cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2RGB)
    x,y, w ,h = pyautogui.locate(dealerbutton,screen)
    #print box around dealer to show that it has been found
    cv2.rectangle(screensh, ((x),(y)), (x+w,y+h), (0, 0, 255), 2)
    cv2.imwrite('dealerfound.png', screensh)


    return x,y #return x,y coordinates of dealer button




"""
os.system("screencapture screen.png")
img = ImageGrab.grab()
img.crop((260,222,543,295))
img.save('smallscreen.png')
import testwindow
screen = "screen.png"
#img = cv2.imread("screen.png")
#print type(img)
#print img.shape
#crop_img = img[260:560,222:300,:]
#cv2.imshow('cropped',img)
#cv2.imwrite('smallscreen.png',crop_img)
cs = cards_on_screen('smallscreen.png')


print(cs)


cardpath = 'ps/backofcards2.png'

screenshot1 = Image.open(screen)
screenshot = cv2.cvtColor(np.array(screenshot1), cv2.COLOR_BGR2RGB)

card = Image.open(cardpath)
coveredcard = cv2.cvtColor(np.array(card), cv2.COLOR_BGR2RGB)


t1 = time.time()
x = find_hidden_on_screen(coveredcard,screenshot)
t2 = time.time()
t = t2-t1
print ("number of player is: %s found in %s second" %(x,t))

#dealerx, dealery = find_dealer(screen)
"""
#print "dealer found at %s %s" %(dealerx,dealery)

