from Tkinter import *
from pieces import *
import subprocess
import os
import threading


class Board(Canvas):
    '''
     -self.coord_dict keeps track of first clicked square if it has a
      piece on it.
     -self.piece_img correlates pictures with pieces
     -self.player keeps track of player status
     -self.avail becomes a list that contains all valid moves for
      the piece in self.coord_dict
     -self.clk and self.ps are used in the firstclk method to provide
      a condition so that clicking in the same spot a second time unselects
      and unhighlights the clicked square.
     -self.n is to prevent a simple click to signal next turn after a move and to prevent
      players from abusing the timer so that the timer does not reset every time
      space or enter are pressed.
     -self.t is the timer threaded into the code.
    '''    
    def __init__(self, master):
        Canvas.__init__(self, master, bg = "white")
        self.pack(fill = BOTH, expand = 1)
        self.t = threading.Timer(10.0, self.refresh)
        self.n = None
        self.piece_img = {}
        self.coord_dict = {}
        self.player = 1
        self.avail = None
        self.clk = None
        self.ps = None
        self.bind("<Button-1>", self.clickcords)
        self.bind_all("<Return>", self.fresh)
        self.bind_all("<space>", self.fresh)
        
    # Primarily made since binding "<Return>" and "<space>" to a method requires the method
    # to have an argument.
    def fresh(self, event):
        self.refresh()

    # Made to bind the timer to a method that will automatically reset n, call the play
    # method, and update the board.
    def re(self):
        self.n = None
        self.play()
        self.refresh()

    # Updates the board, launches "Lights.py" as a subprocess so that the GPIO can run while
    # the game is being played, also terminates "Lights.py" to reset the visual timer, it also
    # sets and resets the internal timer that ends a turn automatically.
    def refresh(self):
        if self.n != 1:
            
            self.t.cancel()
            self.t = threading.Timer(10.0, self.re)
            # If not using raspberry pi, skip.
            try:
                import GPIO
                # If the subprocess not already running, skip.
                try:
                    Board.pid.terminate()
                except:
                    pass
                Board.pid = subprocess.Popen(["python", "Lights.py"])
            except:
                pass
            self.t.start()
            if 'coord1' not in self.coord_dict:
                self.board()
            self.n = 1
            
    # Creates a list of pieces for each player.
    # Creates two dictionaries for each player that will keep track of each piece position.
    # One dictionary uses pieces as keys to pull position (piece_dict) and the other uses position as keys
    # to pull pieces (pos_dict).
    def init_pos(self):
        Board.pieces = []
        Board.pieces2 = []
        for i in range(20):
            if i < 10:
                Board.pieces.append("Piece" + str(i + 1))
                Board.pieces2.append("Piece" + str(i + 11))
            else:
                Board.pieces.append("Pawn" + str(i - 9))
                Board.pieces2.append("Pawn" + str(i + 1))
        Board.piece_dict = {a:encode(self.coords(a)[0], self.coords(a)[1]) for a in Board.pieces}
        Board.piece_dict2 = {a:encode(self.coords(a)[0], self.coords(a)[1]) for a in Board.pieces2}
        Board.pos_dict = {v: k for k,v in Board.piece_dict.items()}
        Board.pos_dict2 = {v: k for k,v in Board.piece_dict2.items()}

    # Changes the position that each piece is currently at to the opposite of that position.
    # Also updates the current player.
    # This method is the key to flipping the board after each turn.
    def play(self):
        for k,v in Board.piece_dict.items():
            Board.piece_dict[k] = opp[v]

        for k,v in Board.piece_dict2.items():
            Board.piece_dict2[k] = opp[v]

        Board.pos_dict = {v: k for k,v in Board.piece_dict.items()}
        Board.pos_dict2 = {v: k for k,v in Board.piece_dict2.items()}

        if self.player == 1:
            self.player += 1
        else:
            self.player -= 1
        
    # Draws the board
    def board(self, pos = None):
        num = 0
        for i in range(10):
            for n in range(10-i):
                if i == 0:
                    self.create_rectangle(40 * n, 40 * n, 40 * (n + 1), 40 * (n + 1),
                                          outline="white", fill = "gray")
                else:
                    if i % 2 == 1:
                        color = "magenta"
                    else:
                        color = "gray"
                    

                    x1 = 40 * (n + num)
                    y1 = 40 * n
                    x2 = 40 * (n + num + 1)
                    y2 = 40 * (n + 1)
                    self.create_rectangle(x1, y1, x2, y2,
                                          outline="deepskyblue", fill= color,
                                          tags = "square")

                    self.create_rectangle(y1, x1, y2, x2,
                                          outline="deepskyblue", fill= color,
                                          tags = "square")

                    # Highlights the squares when a square is clicked on
                    if pos != None:
                        x, y = decode(pos)
                        self.create_rectangle(x-20, y-20, x+20, y+20, outline="orange", fill="lightblue")

                        # Highlights the squares that the selected piece can move to.
                        if "coord1" in self.coord_dict:
                            for sq in self.avail:
                                if self.player == 1:
                                    if sq not in Board.pos_dict:
                                        x, y = decode(sq)
                                        self.create_rectangle(x-20, y-20, x+20, y+20, outline="blue", fill="white")
                                else:
                                    if sq not in Board.pos_dict2:
                                        x, y = decode(sq)
                                        self.create_rectangle(x-20, y-20, x+20, y+20, outline="blue", fill="white")
                                
            num += 1

        self.setimage()

    # Sets images for each piece.
    # Places the images of the pieces on the board   
    def setimage(self):
        n = 0
        Board.piece=PhotoImage(file="rook.gif")
        Board.piece2=PhotoImage(file="bishop.gif")
        Board.piece3=PhotoImage(file="knight.gif")
        Board.piece4=PhotoImage(file="archer.gif")
        Board.piece5=PhotoImage(file="rogue.gif")
        Board.piece6=PhotoImage(file="rook2.gif")
        Board.piece7=PhotoImage(file="bishop2.gif")
        Board.piece8=PhotoImage(file="knight2.gif")
        Board.piece9=PhotoImage(file="archer2.gif")
        Board.piece10=PhotoImage(file="rogue2.gif")
        
        Board.pawn=PhotoImage(file="pawn.gif")
        Board.pawn2=PhotoImage(file="pawn2.gif")
        
        board_list1 = [Board.piece, Board.piece2, Board.piece3, Board.piece4,
        Board.piece5]
        
        board_list2 = [Board.piece6, Board.piece7, Board.piece8, Board.piece9,
        Board.piece10]
    
        try:
            # If piece_img dict is empty, build it.
            # Dictionary associates pieces with images.
            if len(self.piece_img) == 0:

                # Throws an exception if Board.pieces list is not made yet
                # Therefore, only after initial setup will this code run.
                for piece in Board.pieces:
                    if piece == "Piece1" or piece == "Piece10":
                        self.piece_img[piece] = Board.piece
                    elif piece == "Piece2" or piece == "Piece9":
                        self.piece_img[piece] = Board.piece2
                    elif piece == "Piece3" or piece == "Piece8":
                        self.piece_img[piece] = Board.piece3
                    elif piece == "Piece4" or piece == "Piece7":
                        self.piece_img[piece] = Board.piece4
                    elif piece == "Piece5" or piece == "Piece6":
                        self.piece_img[piece] = Board.piece5
                    else:
                        self.piece_img[piece] = Board.pawn

                for piece in Board.pieces2:
                    if piece == "Piece11" or piece == "Piece20":
                        self.piece_img[piece] = Board.piece6
                    elif piece == "Piece12" or piece == "Piece19":
                        self.piece_img[piece] = Board.piece7
                    elif piece == "Piece13" or piece == "Piece18":
                        self.piece_img[piece] = Board.piece8
                    elif piece == "Piece14" or piece == "Piece17":
                        self.piece_img[piece] = Board.piece9
                    elif piece == "Piece15" or piece == "Piece16":
                        self.piece_img[piece] = Board.piece10
                    else:
                        self.piece_img[piece] = Board.pawn2

            # Populates the board using the position for each piece in Board.piece_dict.
            for piece in Board.pieces:
                self.delete(piece)
                Board.image = self.create_image(decode(Board.piece_dict[piece]),\
                                                image=self.piece_img[piece],\
                                                tags=(piece))
            for piece in Board.pieces2:
                self.delete(piece)
                Board.image = self.create_image(decode(Board.piece_dict2[piece]),\
                                                image=self.piece_img[piece],\
                                                tags=(piece))
            
            

        except:
            # Builds initial piece setup on board.
            for p in board_list1:
                Board.image = self.create_image(20 + (40 * n), 380, image=p,\
                                                tags=("Piece" + str(n + 1)))
                n += 1
            for p in board_list1[::-1]:
                Board.image = self.create_image(20 + (40 * n), 380, image=p, \
                                                tags=("Piece" + str(n + 1)))
                n += 1

            n = 0
            for p in board_list2:
                Board.image = self.create_image(20 + (40 * n), 20, image=p, \
                                                tags=("Piece" + str(n + 11)))
                n += 1
            for p in board_list2[::-1]:
                Board.image = self.create_image(20 + (40 * n), 20, image=p, \
                                                tags=("Piece" + str(n + 11)))
                n += 1

            n = 0
            for p in range(10):
                Board.image = self.create_image(20 + (40 * n), 340, image=Board.pawn,\
                                                tags=("Pawn" + str(p + 1)))
                n += 1

            n = 0
            for p in range(10):
                Board.image = self.create_image(20 + (40 * n), 60, image=Board.pawn2, \
                                                tags=("Pawn" + str(p + 11)))
                n += 1

            # Creates the lists and dictionaries used in the try block.
            self.init_pos()
        

    # Method ran every time something is clicked within the window.
    def clickcords(self, event):
        # This condition prohibits the method to execute if the player has already moved a piece.
        if self.n == 1:
            letter = "ABCDEFGHIJ"
            z = 0
            a = 1
            d1 = 0
            # x and y coords clicked are reassigned to the center coord of whichever square the x and y coords
            # resides in.
            for i in range(1,11):
                for n in letter:
                    distance = self.dist(event.x, x_cord[i], event.y, y_cord[n]) 
                    if distance <= 20:
                        x = x_cord[i]
                        y = y_cord[n]
                        z = 1
                        break
                    if distance <= (20**2 + 20**2)**0.5:
                        if a == 1:
                            x = x_cord[i]
                            y = y_cord[n]
                            a += 1
                            d1 = distance
                        if distance < d1:
                            x = x_cord[i]
                            y = y_cord[n]
                            d1 = distance
                if z == 1:
                    break

            # pos is assigned to the square name the x and y coords reside in.
            pos = encode(x,y)

            # Updates piece and position dictionary for each player.
            # The conditions are the same for each player but dictionaries affected
            # are changed.
            if self.player == 1:
                
                # Checks if you initially clicked on a piece.
                # Checks to see if the second click is not on a piece
                # Checks to see if self.avail is a list
                if "coord1" in self.coord_dict and self.avail != None and pos not in Board.pos_dict:
                    # Checks to see if the second place clicked is a valid space to move to.
                    # If valid, dictionaries are changed to reflect the desired new position for
                    # the selected piece.
                    # If not valid, self.coord_dict becomes empty and the piece will be deselected.
                    if pos in self.avail:
                        pos1 = Board.piece_dict[self.coord_dict["coord1"]]                
                        Board.piece_dict[self.coord_dict["coord1"]] = pos
                        Board.pos_dict[pos] = self.coord_dict["coord1"]
                        del Board.pos_dict[pos1]
                        del self.coord_dict["coord1"]
                        # If the desired new position is already occupied by a piece owned by the opponent,
                        # the opponent's piece is deleted from all dictionaries and lists containing that piece.
                        if pos in Board.pos_dict2:
                            del Board.pieces2[Board.pieces2.index(Board.pos_dict2[pos])]
                            del Board.piece_dict2[Board.pos_dict2[pos]]
                            del Board.pos_dict2[pos]
                            
                                        
                                                            
                        self.board()
                        self.avail = None
                        self.ps = None
                        self.n = None
                        self.play()
                        self.t.cancel()
                        # If the variable is not defined, skip.
                        try:
                            Board.pid.terminate()
                        except:
                            pass

                        # If there are no more main pieces owned by the opponent, trigger the win condition
                        for k in Board.pieces2:
                            if k[:5] == "Piece":
                                break
                            else:
                                rev = Board.pieces2[::-1]
                                if k == rev[0]:
                                    print "Congrats, Player 1 Wins!" 
                                    self.t.cancel()
                                    os._exit(0)

                        
                    else:
                        del self.coord_dict["coord1"]
                        self.board(pos)
                        self.ps = pos
                else:
                    self.firstclk(pos)

            else:
                if "coord1" in self.coord_dict and self.avail != None and pos not in Board.pos_dict2:
                    if pos in self.avail:
                        pos1 = Board.piece_dict2[self.coord_dict["coord1"]]                
                        Board.piece_dict2[self.coord_dict["coord1"]] = pos
                        Board.pos_dict2[pos] = self.coord_dict["coord1"]
                        del Board.pos_dict2[pos1]
                        del self.coord_dict["coord1"]
                        if pos in Board.pos_dict:
                            del Board.pieces[Board.pieces.index(Board.pos_dict[pos])]
                            del Board.piece_dict[Board.pos_dict[pos]]
                            del Board.pos_dict[pos]
                            
                                        
                                                                                                 
                            
                        self.board()
                        self.avail = None
                        self.ps = None
                        self.n = None
                        self.play()
                        self.t.cancel()
                        try:
                            Board.pid.terminate()
                        except:
                            pass
                         
                        for k in Board.pieces:
                            if k[:5] == "Piece":
                                break
                            else:
                                rev = Board.pieces[::-1]
                                if k == rev[0]:
                                    print "Congrats, Player 2 Wins!" 
                                    self.t.cancel()
                                    os._exit(0)
                                    
                        
                    else:
                        del self.coord_dict["coord1"]
                        self.board(pos)
                        self.ps = pos

                else:
                    self.firstclk(pos)

    # This method is called on the first click a player makes on the board,
    # or when the player clicks on a square not occupied by a piece.
    def firstclk(self, pos):
        
        # Assigns self.avail to a list that contains all valid spaces
        # the selected piece can move to.
        # If position clicked is not occupied by a piece, an
        # exception is thrown and the except block will run.
        try:
            if self.player == 1:
                pos1 = Board.pos_dict[pos]
                dct = Board.pos_dict2
            else:
                pos1 = Board.pos_dict2[pos]
                dct = Board.pos_dict

            if self.ps != pos:
                if pos1[:4] == "Pawn":
                    self.avail = Pawn(pos)
                    self.avail = self.avail.move()

                if pos1 == "Piece3" or pos1 == "Piece8" or \
                   pos1 == "Piece13" or pos1 == "Piece18":
                    self.avail = Knight(pos)
                    self.avail = self.avail.move()

                if pos1 == "Piece2" or pos1 == "Piece9" or \
                   pos1 == "Piece12" or pos1 == "Piece19":
                    self.avail = Bishop(pos, dct)
                    self.avail = self.avail.move()

                if pos1 == "Piece1" or pos1 == "Piece10" or \
                   pos1 == "Piece11" or pos1 == "Piece20":
                    self.avail = Rook(pos, dct)
                    self.avail = self.avail.move()

                if pos1 == "Piece5" or pos1 == "Piece6" or \
                   pos1 == "Piece15" or pos1 == "Piece16":
                    self.avail = Rogue(pos)
                    self.avail = self.avail.move()

                if pos1 == "Piece4" or pos1 == "Piece7" or \
                   pos1 == "Piece14" or pos1 == "Piece17":
                    self.avail = Archer(pos)
                    self.avail = self.avail.move()
                        
                self.coord_dict["coord1"] = pos1
                self.board(pos)
                self.ps = pos

            # If player clicked on the same piece a second time, the piece is deselected and the squares are not highlighted.
            else:
                del self.coord_dict["coord1"]
                self.board()
                self.ps = None
    
        except:
            # First time the empty square is clicked, highlight it, else unhighlight it.
            if self.clk == None or pos != self.ps:
                self.board(pos)
                self.clk = 1
                self.ps = pos
            else:
                self.board()
                self.clk = None
        
        
    # Calculates the distance between two points
    def dist(self, x1, x2, y1, y2):
        return ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5

n = 20
letters = "BCDEFGHI"

# Makes the dictionary to define each y character.
# For example: A = 35 pixels for y.
y_cord = {letters[a]:(n + (40 * (a+1))) for a in range(8)}
y_cord["A"] = n
y_cord["J"] = 380

# Makes the dictionary for each x value.
# For example: 1 = 35 pixels for x.
x_cord = {x + 1:(n+(40 * x)) for x in range(1,10)}
x_cord[1] = n
x_cord[10] = 380

# Creates the a dictionary that correlates each position with its opposite position
# i.e, A1 with J10, A2 with J9 etc...
opp = {}
letters = "ABCDEFGHIJ"
for let in letters:
    for n in range(1, 11):
        opp[let + str(n)] = letters[9 - letters.index(let)] + str(11-n)









        
