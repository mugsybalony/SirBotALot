import pyautogui
import time
from PIL import Image

class table():
    """
    class to describe the current state of the table.

    The idea is that a loop is running and constantly updating this information,
    so that when a decision is made it can be logged with a record of what the table was like at that point.
    """

    """
    self.board #what cards are showing on the board
    self.playerhand #what hands are in the players
    self.state #pr-flop; flop ; turn; river
    self.potsize
    self.bigblind
    self.oddsofwinning
    slef.numplayers

    self.actionoptions #check, call, fold, raise

    """


im1 = pyautogui.screenshot()

tablepic = "ps/screenshot3.png"
x = pyautogui.locate(tablepic, im1)

print x
