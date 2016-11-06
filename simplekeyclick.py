import pyautogui

foldx, foldy = pyautogui.locateCenterOnScreen('ps/fold.png')

def players():
    players_in_hand = list(pyautogui.locateAllOnScreen('images/cardbacks.png'))
    print len(players_in_hand)

def fold():
    pyautogui.click(foldx, foldy)
    return

def call():
    pyautogui.click(foldx + 130, foldy)
    return

def raise_standard():
    pyautogui.click(foldx + 260, foldy)
    return

def raise_pot():
    pyautogui.click(foldx + 240, foldy - 70)
    return

def raise_max():
    pyautogui.click(foldx + 300, foldy - 70)
    return


try:
    call()
except:
    fold()
#fold()
call()
#raise_bet()
#raise_pot()
#raise_max()
#players()


