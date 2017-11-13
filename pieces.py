
# The superclass from which all of the pieces(pawn, knight, etc.) inherit from.
# 2 methods are created to make it easier to make the algorithm that changes the letter (letchg) and the
# number (numchg) in relation to where the piece is.
# self.dct is used in the Rook and Bishop classes to restrict those pieces from jumping opponent pieces.

class Piece(object):
    def __init__(self, pos, dct=None):
        self.dct = dct
        self.orig = pos
        self.let = pos[0]
        self.num = pos[1:]
        self.correlation = {}
        for i in range(len("ABCDEFGHIJ")):
            self.correlation["ABCDEFGHIJ"[i]] = i + 1
        self.correlation2 = {v:k for k,v in self.correlation.items()}

    def letchg(self, change):
        return self.correlation2[(self.correlation[self.let] + change)]

    def numchg(self, change):
        return str(int(self.num) + change)
    
# The pawn class returns a list of valid moves for the pawn.
# i.e, left, right, up, etc..
class Pawn(Piece):
    def move(self):
        if self.let != "A" and self.let != "J":
            letup = self.letchg(1)
            letdown = self.letchg(-1)
        elif self.let == "A":
            letup = self.letchg(1)
            letdown = self.let
        else:
            letup = self.let
            letdown = self.letchg(-1)

        if self.num != "10" and self.num != "1":
            numup = self.numchg(1)
            numdown = self.numchg(-1)
        elif self.num == "10":
            numup = self.num
            numdown = self.numchg(-1)
        else:
            numup = self.numchg(1)
            numdown = self.num
    
        left = self.let + numdown
        right = self.let + numup
        up = letdown + self.num
        down = letup + self.num
        nw = letdown + numdown
        ne = letdown + numup
        sw = letup + numdown
        se = letup + numup
        
        return [left, right, up, down, nw, ne, sw, se]

# The knight class returns a list of valid moves for the knight.
# i.e, nw, wn, ne, etc...
class Knight(Piece):
    def move(self):
        nw, wn, ne, en,\
            ws, sw, es, se = ("0" * 8)
        if int(self.num) <= 2:
            wn = self.orig
            ws = self.orig
            if int(self.num) == 1:
                nw = self.orig
                sw = self.orig

        if self.let <= "B":
            nw = self.orig
            ne = self.orig
            if self.let == "A":
                wn = self.orig
                en = self.orig

        if int(self.num) >= 9:
            en = self.orig
            es = self.orig
            if self.num == "10":
                ne = self.orig
                se = self.orig

        if self.let >= "I":
            se = self.orig
            sw = self.orig
            if self.let == "J":
                es = self.orig
                ws = self.orig

        if nw != self.orig:        
            nw = self.letchg(-2) + self.numchg(-1)
        if wn != self.orig:
            wn = self.letchg(-1) + self.numchg(-2)
        if ne != self.orig:
            ne = self.letchg(-2) + self.numchg(1)
        if en != self.orig:
            en = self.letchg(-1) + self.numchg(2)
        if ws != self.orig:
            ws = self.letchg(1) + self.numchg(-2)
        if sw != self.orig:
            sw = self.letchg(2) + self.numchg(-1)
        if es != self.orig:
            es = self.letchg(1) + self.numchg(2)
        if se != self.orig:
            se = self.letchg(2) + self.numchg(1)

        return [nw, wn, ne, en, ws, sw, es, se]
        
    
# The Bishop class returns a list of valid moves for the Bishop
class Bishop(Piece):
    def move(self):
        let = self.let
        num = self.num
        n = 1

        lst = []
        lst.append(let + num)
        while let != "A" and num != "1":
            if (let + num) not in self.dct: 
                let = self.letchg(-n)
                num = self.numchg(-n)
                lst.append(let + num)
                n += 1
            else:
                break
        let = self.let
        num = self.num
        n = 1

        while let != "A" and num != "10":
            if (let + num) not in self.dct: 
                let = self.letchg(-n)
                num = self.numchg(n)
                lst.append(let + num)
                n += 1
            else:
                break

        let = self.let
        num = self.num
        n = 1

        while let != "J" and num != "1":
            if (let + num) not in self.dct: 
                let = self.letchg(n)
                num = self.numchg(-n)
                lst.append(let + num)
                n += 1
            else:
                break
            
        let = self.let
        num = self.num
        n = 1

        while let != "J" and num != "10":
            if (let + num) not in self.dct: 
                let = self.letchg(n)
                num = self.numchg(n)
                lst.append(let + num)
                n += 1
            else:
                break
        return lst

    
# The Rook class returns a list of valid moves for the Rook.
class Rook(Piece):
    def move(self):
        let = self.let
        num = self.num
        n = 1
        lst = []
        lst.append(let + num)

        while let != "A":
            if (let + num) not in self.dct: 
                let = self.letchg(-n)
                lst.append(let + num)
                n += 1
            else:
                break

        let = self.let
        num = self.num
        n = 1

        while let != "J":
            if (let + num) not in self.dct: 
                let = self.letchg(n)
                lst.append(let + num)
                n += 1
            else:
                break

        let = self.let
        num = self.num
        n = 1

        while num != "1":
            if (let + num) not in self.dct: 
                num = self.numchg(-n)
                lst.append(let + num)
                n += 1
            else:
                break

        let = self.let
        num = self.num
        n = 1

        while num != "10":
            if (let + num) not in self.dct: 
                num = self.numchg(n)
                lst.append(let + num)
                n += 1
            else:
                break

        return lst

    
# The Archer subclass returns a list of valid moves for the Archer
# i.e, n, ne, nw, etc...
class Archer(Piece):
    def move(self):
        n, s, e, w, \
           ne, nw, se, sw = ("0" * 8)

        if int(self.num) <= 2:
            w = self.orig
            if self.num == "1":
                sw = self.orig
                nw = self.orig

        if int(self.num) >= 9:
            e = self.orig
            if int(self.num) == 10:
                se = self.orig
                ne = self.orig

        if self.let <= "B":
            n = self.orig
            if self.let == "A":
                ne = self.orig
                nw = self.orig

        if self.let >= "I":
            s = self.orig
            if self.let == "J":
                se = self.orig
                sw = self.orig

        if n != self.orig:
            n = self.letchg(-2) + self.num
        if ne != self.orig:
            ne = self.letchg(-1) + self.numchg(1)
        if nw != self.orig:
            nw = self.letchg(-1) + self.numchg(-1)
        if w != self.orig:
            w = self.let + self.numchg(-2)
        if e != self.orig:
            e = self.let + self.numchg(2)
        if s != self.orig:
            s = self.letchg(2) + self.num
        if se != self.orig:
            se = self.letchg(1) + self.numchg(1)
        if sw != self.orig:
            sw = self.letchg(1) + self.numchg(-1)

        return [n, ne, nw, w, e, s, se ,sw]
                
        
# The Rogue subclass returns a list of valid moves for the Rogue.
# i.e, nw, n, ne, etc...
class Rogue(Piece):
    def move(self):
        n, s, e, w, \
           ne, se, sw, nw = ("0" * 8)

        if int(self.num) <= 2:
            nw = self.orig
            w = self.orig
            sw = self.orig
            
        if int(self.num) >= 9:
            ne = self.orig
            e = self.orig
            se = self.orig

        if self.let == "A" or self.let == "B":
            ne = self.orig
            n = self.orig
            nw = self.orig

        if self.let == "J" or self.let == "I":
            sw = self.orig
            s = self.orig
            se = self.orig

        if sw != self.orig:
            sw = self.letchg(2) + self.numchg(-2)
        if s != self.orig:
            s = self.letchg(2) + self.num
        if se != self.orig:
            se = self.letchg(2) + self.numchg(2)
        if nw != self.orig:
            nw = self.letchg(-2) + self.numchg(-2)
        if w != self.orig:
            w = self.let + self.numchg(-2)
        if sw != self.orig:
            sw = self.letchg(2) + self.numchg(-2)
        if n != self.orig:
            n = self.letchg(-2) + self.num
        if e != self.orig:
            e = self.let + self.numchg(2)
        if ne != self.orig:
            ne = self.letchg(-2) + self.numchg(2)

        return [nw, n, ne, e, se, s, sw, w]

# The name of the square (ei, A1 or F3) is the argument and
# returns the coordinate for the name.
def decode(pos):
    x = x_cord[int(pos[1:])]
    y = y_cord[pos[0]]
    return x, y

# x and y coordinates are the arguments and the name for the
# square is returned.
def encode(x, y):
    letter = {v: k for k, v in y_cord.items()}
    num = {v: k for k, v in x_cord.items()}
    x = int(round(x))
    y = int(round(y))
    pos = letter[y] + str(num[x])
    return pos



n = 20
letters = "BCDEFGHI"

# Makes the dictionary to define each y character.
# For example: A = 20 pixels for y.
y_cord = {letters[a]:(n + (40 * (a+1))) for a in range(8)}
y_cord["A"] = n
y_cord["J"] = 380

# Makes the dictionary for each x value.
# For example: 1 = 20 pixels for x.
x_cord = {x + 1:(n+(40 * x)) for x in range(1,10)}
x_cord[1] = n
x_cord[10] = 380
