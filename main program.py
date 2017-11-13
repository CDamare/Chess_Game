################################################
# Name: Alex Faucheux and Christopher Damare
# Date: 11/13/2017
################################################



from Tkinter import *
from board_local import *
from time import sleep

print
print
print
print "\t       Welcome to the most amazing game ever created!!!!"
print "\n\t     The rules are fairely simple... Kill all main pieces."
print "\n\t             Player 1 is RED and Player 2 is BLUE"
print "\n\t    All players have exactly 10 seconds to take their turns!"
print "\n\t  Once you kill all the pieces on the board that are not pawns,"
print "\n\t                          YOU WIN."
print



sleep(10)
    
window = Tk()
window.wm_geometry("400x400") # Size of the board.
window.title("Chess DEATHMATCH")
p = Board(window)    
p.refresh() # Calls the refresh function inside the class Board
window.mainloop()

