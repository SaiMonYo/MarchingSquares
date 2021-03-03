import pygame
from pygame import gfxdraw
import random
from noise import snoise2
import time

WHITE = (255,255,255)
BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)
GREY  = ( 30, 30, 30)

#class for the individual dots
class dot():
    def __init__(self, x, y, value, win):
        #initialisation
        self.x = x
        self.y = y
        self.value = value
        self.win = win
    
    #drawing solid circle if value is 1, 1==True
    def draw(self):
        if self.value:
            gfxdraw.filled_circle(self.win, self.x, self.y, 2, WHITE)
            return
        gfxdraw.aacircle(self.win, self.x, self.y, 3, WHITE)

class dotContainer():
    #container to hold and generate the dots
    def __init__(self, WIDTH, HEIGHT, res):
        self.sqaureWidth = WIDTH // res
        #list comprehension
        seed = random.random() * random.random() * 1000
        print(seed)
        self.dots = dots = [[dot(j * res, i * res, self.genVal(i, j, seed), win) for j in range(0,WIDTH//res + 1)] for i in range(0,HEIGHT//res + 1)]

    def drawDots(self):
        for row in self.dots:
            for d in row:
                d.draw()

    def genVal(self, x, y, seed):
        #returning 1 or 0 depending on random function
        #higher chance of being 1
        #return 0 if random.uniform(0,10) > 6.3 else 1

        return 1 if (self.getNoise(x, y, seed)+1) * 10 > 12.5 else 0

    def getNoise(self, x, y, seed):
        #print(snoise2(x,y))
        #print(snoise2(x,y))
        #print("\n")
        return snoise2(x, y, base=seed)
        
        
        

class marchingSquare():
    def __init__(self, dotsCont, win, res):
        #inits
        self.dotsCont = dotsCont
        self.win = win
        self.res = res

        #centre of the edges of the square
        self.a = [0.5, 0  ]
        self.b = [1  , 0.5]
        self.c = [0.5, 1  ]
        self.d = [0  , 0.5]

        #lookup table to see which lines to draw
        self.lookup = [[[None, None],[None,None]],
                       [[self.d,self.c],[None,None]],
                       [[self.c,self.b],[None,None]],
                       [[self.d,self.b],[None,None]],
                       [[self.a,self.b],[None,None]],
                       [[self.d,self.a],[self.c,self.b]],
                       [[self.a,self.c],[None,None]],
                       [[self.d,self.a],[None,None]],
                       [[self.d,self.a],[None,None]],
                       [[self.a,self.c],[None,None]],
                       [[self.d,self.c],[self.a,self.b]],
                       [[self.a,self.b],[None,None]],
                       [[self.d,self.b],[None,None]],
                       [[self.c,self.b],[None,None]],
                       [[self.d,self.c],[None,None]],
                       [[None, None],[None,None]]]

    def getValue(self, y, x, b = True):
        x //= self.res
        y //= self.res
        '''
        if x + 1 >= len(self.dotsCont.dots) or x + 1 >= len(self.dotsCont.dots):
            return None
        '''
        #binary number from square
        '''
        a---->b
              |
              |
              v
        d<----c
        '''
        a = self.dotsCont.dots[x  ][y  ]
        b = self.dotsCont.dots[x  ][y+1]
        c = self.dotsCont.dots[x+1][y+1]
        d = self.dotsCont.dots[x+1][y  ]

        return (a.value * 8) + (b.value * 4) + (c.value * 2) + d.value

    #draw the lines using look-up table
    def drawline(self, y, x):
        #value of the square
        v = self.getValue(x, y)
        data = self.lookup[v]

        #first line
        if data[0][0] == None:
            return
        firstPosx = data[0][0][0]
        firstPosy = data[0][0][1]
        secPosx =   data[0][1][0]
        secPosy =   data[0][1][1]

        gfxdraw.line(self.win, int(x + firstPosx * self.res), int(y + firstPosy * self.res), int(x + secPosx * self.res), int(y + secPosy * self.res), WHITE)

        #second line
        if data[1][0] == None:
            return 
        firstPosx = data[1][0][0]
        firstPosy = data[1][0][1]
        secPosx =   data[1][1][0]
        secPosy =   data[1][1][1]

        gfxdraw.line(self.win, int(x + firstPosx * self.res), int(y + firstPosy * self.res), int(x + secPosx * self.res), int(y + secPosy * self.res), WHITE)
        

            
#screen dimensions       
WIDTH = 1000
HEIGHT = WIDTH
res = 20

#pygame window inits
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()
clock = pygame.time.Clock()
win.fill(BLACK)

def main():
    #clearing screen
    win.fill(BLACK)
    pygame.display.update()
    dots = dotContainer(WIDTH, HEIGHT, res)
    ''' COMMENT LINE BELOW IF DOTS DONT WANT TO BE DRAWN '''
    #time.sleep(0.5)
    dots.drawDots()
    pygame.display.update()
    #time.sleep(0.5)
    square = marchingSquare(dots, win, res)

    #drawing lines for all the squares
    for y in range(len(dots.dots)-1):
        for x in range(len(dots.dots[y])-1):
            square.drawline(dots.dots[y][x].x, dots.dots[y][x].y)
        pygame.display.update()
    time.sleep(0.5)

while True:
    main()
