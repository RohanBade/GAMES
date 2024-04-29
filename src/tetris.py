import pygame as pg
import random, time

#   COLORS

ORANGE = ( 255, 165, 0)
RED = ( 255, 0, 0 )
LIGHTRED = ( 175, 20, 20 )
WHITE = ( 255, 255, 255 )
BLUE = ( 0, 0, 155 )
LIGHTBLUE = ( 20, 20, 175 )
BLACK = ( 0, 0, 0 )
LIGHTGREEN = ( 20, 175, 20 )
GREEN = ( 0, 255, 0 )
DARKGREEN = ( 0, 155, 0 )
DARKGRAY = ( 40, 40, 40 )
GRAY = ( 185, 185, 185 )
YELLOW = ( 155, 155, 0 )
LIGHTYELLOW = ( 175, 175, 20 )
VIOLET = ( 127, 0, 255 )
PINK = ( 255, 192, 203)

BORDERCOLOR = WHITE
BGCOLOR = BLACK
TEXTCOLOR = GREEN
COLORS = ( BLUE, RED, YELLOW, GREEN )
LIGHTCOLORS = ( LIGHTBLUE, LIGHTRED, LIGHTYELLOW, LIGHTGREEN )

T_SIZE = 5

#   SHAPES

"""

    WE HAVE DIFFERENT SHAPES
    T, S, J, Z, L, I, O
    USING 5 * 5 GRID TO REPRESENT THESE SHAPES
    THE SHAPE CONTAINS ALL THE POSSIBLE SHAPE

"""

T_SHAPE = [
    [
        ".....",
        "..0..",
        ".000.",
        ".....",
        "....."
    ],
    [
        ".....",
        "..0..",
        "..00.",
        "..0..",
        "....."
    ],
    [
        ".....",
        ".....",
        ".000.",
        "..0..",
        "....."
    ],
    [
        ".....",
        "..0..",
        ".00..",
        "..0..",
        "....."
    ],
]

S_SHAPE = [
    [
        ".....",
        ".....",
        "..00.",
        ".00..",
        "....."
    ],
    [
        ".....",
        ".0...",
        ".00..",
        "..0..",
        "....."
    ],
]

J_SHAPE = [
    [
        ".....",
        ".0...",
        ".000.",
        ".....",
        ".....",
    ],
    [
        ".....",
        "..00.",
        "..0..",
        "..0..",
        ".....",
    ],
    [
        ".....",
        ".....",
        ".000.",
        "...0.",
        ".....",
    ],
    [
        ".....",
        "..0..",
        "..0..",
        ".00..",
        ".....",
    ]
]

Z_SHAPE = [
    [
        ".....",
        ".....",
        ".00..",
        "..00.",
        "....."
    ],
    [
        ".....",
        "..0..",
        ".00..",
        ".0...",
        "....."
    ]
]

L_SHAPE = [
    [
        ".....",
        "...0.",
        ".000.",
        ".....",
        "....."
    ],
    [
        ".....",
        "..0..",
        "..0..",
        "..00.",
        ".....",
    ],
    [
        ".....",        
        ".....",        
        ".000.",        
        ".0...",        
        ".....",        
    ],
    [
        ".....",
        ".00..",
        "..0..",
        "..0..",
        ".....",
    ]
]

I_SHAPE = [
    [
        "..0..",
        "..0..",
        "..0..",
        "..0..",
        "..0.."
    ],
    [
        ".....",
        ".....",
        "00000",
        ".....",
        "....."
    ]
]

O_SHAPE = [
    [
        ".....",
        ".....",
        ".00..",
        ".00..",
        "....."
    ]
]

#   DICTIONARY OF KEY: shape, VALUE: matrix form and color

COLORS = [
    RED ,
    ORANGE ,
    BLUE ,
    PINK,
    GREEN,
    YELLOW ,
    VIOLET 
]
SHAPES = [
    T_SHAPE,
    S_SHAPE,
    J_SHAPE,
    Z_SHAPE,
    L_SHAPE,
    I_SHAPE,
    O_SHAPE
]

#   GAME WINDOW

W_WIDTH = 800
W_HEIGHT = 700

#   PLAY WINDOW

P_WIDTH = 300
P_HEIGHT = 600

#   CELL INFORMATION

C_SIZE = 30

C_ROWS = P_HEIGHT // C_SIZE 
C_COLUMNS = P_WIDTH // C_SIZE



#   FRAME POSITIONING

X0 = ( W_WIDTH - P_WIDTH ) // 2
Y0 = ( W_HEIGHT - P_HEIGHT )

class Piece:
    def __init__( self, column, row ):
        self.shape = random.choice( list( SHAPES ) )
        self.index = SHAPES.index( self.shape )
        self.rotation = random.randint( 0, len(  self.shape  ) - 1 )
        self.x = column
        self.y = row
        self.color = COLORS[ self.index ]

class Board:

    def __init__( self ) -> None:

        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode( ( W_WIDTH, W_HEIGHT ) )
        pg.display.set_caption("Tetris")
        pg.display.set_caption( "Tetris Game" )

        self.running = True

        self.font = pg.font.SysFont( "Consolas", 40 )
        self.label = self.font.render("TETRIS", 1 , WHITE )

        self.locked_positions = {}
        self.change_piece = False
        self.current_piece = Piece( 5, 0 )
        self.next_piece = Piece( 5, 0 )
        self.fall_time = 0
        self.fall_speed = 0.27
        self.level_time = 0


    def run( self ):
        while self.running:
        
            self.screen.fill( BLACK )
            self.screen.blit( self.label, ( P_WIDTH // 2 + X0 - self.label.get_width() // 2, 30 ) )

            self.updateGrid( self.locked_positions )
            self.fall_time += self.clock.get_rawtime()
            self.level_time += self.clock.get_rawtime()
            self.clock.tick()

            if self.level_time/1000 > 5:
                self.level_time = 0
                if self.level_time > 0.12:
                    self.level_time -= 0.005

            if self.fall_time/1000 >= self.fall_speed:
                self.fall_time = 0
                self.current_piece.y += 1
                if not ( self.validSpace( self.current_piece )) and self.current_piece.y > 0:
                    self.current_piece.y -= 1
                    self.change_piece = True


            for event in pg.event.get():
                
                if event.type == pg.QUIT:
                    self.running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False

                    if event.key == pg.K_LEFT:
                        self.current_piece.x -= 1
                        if not self.validSpace( self.current_piece ):
                            self.current_piece.x += 1
    
                    elif event.key == pg.K_RIGHT:
                        self.current_piece.x += 1
                        if not self.validSpace( self.current_piece ):
                            self.current_piece.x -= 1

                    elif event.key == pg.K_UP:
                        self.current_piece.rotation = self.current_piece.rotation + 1 % len( self.current_piece.shape )
                        if not self.validSpace( self.current_piece):
                            self.current_piece.rotation = self.current_piece.rotation - 1 % len( self.current_piece.shape )
    
                    if event.key == pg.K_DOWN:
                        self.current_piece.y += 1
                        if not self.validSpace(self.current_piece):
                            self.current_piece.y -= 1

            self.applyColor()
            
            if self.check_lost( ):
                self.draw_text_middle( "YOU LOST!", 80, (255,255,255))
                pg.display.update()
                pg.time.delay(1500)
                self.running = False
        
            boardrect = pg.Rect( X0, Y0, C_COLUMNS * C_SIZE  , C_ROWS * C_SIZE )
            pg.draw.rect( self.screen, GRAY, boardrect)

            # first color then display grid
            self.colorGrid()
            self.drawGrid()

            self.draw_next_shape( )
            pg.display.update()
        self.destroy()
    
    def applyColor( self ):
        shape_pos = self.convert_shape_format( self.current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1: 
                self.grid[y][x] = self.current_piece.color
        if self.change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                self.locked_positions[p] = self.current_piece.color
            self.current_piece = self.next_piece
            self.next_piece = Piece( 5, 0 )
            self.change_piece = False    
            self.clear_rows()


    def draw_text_middle(self, text, size, color):
        font = pg.font.SysFont("comicsans", size, bold=True)
        label = font.render(text, 1, color)
        self.screen.blit(label, (X0 + P_WIDTH /2 - (label.get_width()/2), Y0 + P_HEIGHT/2 - label.get_height()/2))


    def draw_next_shape(self):
        label = self.font.render('Next:', 1, (255,255,255))

        sx = X0 + P_WIDTH + 50
        sy = Y0 + P_HEIGHT/2 - 100
        format = self.next_piece.shape[self.next_piece.rotation % len(self.next_piece.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pg.draw.rect( self.screen, self.next_piece.color, (sx + j*30, sy + i*30, 30, 30), 0)

        self.screen.blit(label, (sx + 10, sy- 30))

    def updateGrid( self, locked_positions = {} ):
        self.grid = [ [ BLACK for x in range( C_COLUMNS ) ] for y in range( C_ROWS ) ]
        for i in range( len( self.grid ) ):
            for j in range( len( self.grid[i] ) ):
                if ( j, i ) in locked_positions:
                    color = locked_positions[ ( j, i ) ]
                    self.grid[i][j] = color

    def clear_rows(self):
        inc = 0
        for i in range(len(self.grid)-1,-1,-1):
            row = self.grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                # add positions to remove from locked
                ind = i
                for j in range(len(row)):
                    try:
                        del self.locked_positions[(j, i)]
                    except:
                        continue
        if inc > 0:
            for key in sorted(list(self.locked_positions), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    self.locked_positions[newKey] = self.locked_positions.pop(key)


    
    def drawGrid( self ):
        #   BORDER
        for i in range( len( self.grid ) ):
            for j in range( len( self.grid[i] ) ):
                pg.draw.rect( self.screen, GRAY, ( X0 + j* C_SIZE, Y0 + i * C_SIZE, C_SIZE, C_SIZE ), 1)
        pg.draw.rect( self.screen, GRAY, ( X0 , Y0, C_COLUMNS* C_SIZE, C_ROWS * C_SIZE ), 1)

    def colorGrid( self ):
        for i in range( len( self.grid ) ):
            for j in range( len( self.grid[i] ) ):
                pg.draw.rect( self.screen, self.grid[i][j], ( X0 + j* C_SIZE, Y0 + i * C_SIZE, C_SIZE, C_SIZE ), 0)

    def validSpace( self, shape):
        accepted_positions = [[(j, i) for j in range(10) if self.grid[i][j] == (0,0,0)] for i in range(20)]
        accepted_positions = [j for sub in accepted_positions for j in sub]
        formatted = self.convert_shape_format(shape)
    
        for pos in formatted:
            if pos not in accepted_positions:
                if pos[1] > -1:
                    return False
    
        return True

    def check_lost( self ):
        for position in self.locked_positions:
            x,y = position
            if y < 1:
                return True
        return False

    def convert_shape_format( self, shape ):
        positions = []
        format = shape.shape[shape.rotation % len( shape.shape )]
    
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))
    
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)
    
        return positions

    def destroy( self ):
        pg.display.quit()
        pg.quit()

    

if __name__ =="__main__":
    board = Board()
    board.run()