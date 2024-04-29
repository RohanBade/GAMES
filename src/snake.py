import pygame as pg
import random 

#   COLORS

RED = ( 255, 0, 0 )
WHITE = ( 255, 255, 255 )
BLACK = ( 0, 0, 0 )
GREEN = ( 0, 255, 0 )
DARKGREEN = ( 0, 155, 0 )
DARKGRAY = ( 40, 40, 40 )
BGCOLOR = "Black"

#   KEYBOARD COMMANDS

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

#   GAME WINDOW

W_WIDTH = 640
W_HEIGHT = 480

#   CELL INFORMATION

C_SIZE = 20
C_WIDTH = int( W_WIDTH / C_SIZE )
C_HEIGHT = int( W_HEIGHT / C_SIZE )



class gamefield:

    def __init__(self) -> None:

        """
            PYGAME INITIALIZATIONS
            CLOCK
            FRAMERATE....
        """

        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode( ( W_WIDTH, W_HEIGHT ) )
        self.FPS = 10
        pg.display.set_caption( "Snake Game" )

        #   FONTS

        self.font_ = pg.font.SysFont( "Consolas", 40 )
        self.font_points = pg.font.SysFont( "Consolas", 20 )
    
        #   GAME INFOS

        self.running = True
        self.apple_count = 0
        self.game_states = [ 0, 1, 2 ]
        self.game_current_state = 0
        self.screen_fade = pg.Surface( ( W_WIDTH, W_HEIGHT ) )
        self.screen_fade.fill( ( 0, 0, 0 ) )
        self.screen_fade.set_alpha( 140 )
        self.snake = snake()
        self.randomApple()

        """
            0 -------> INITIAL SCREEN
            1 -------> GAME RUNNING
            2 -------> GAME OVER
        """

        self.screen.fill( BLACK )
    
    def display_points( self ):
        
        points = self.font_points.render( "POINTS", True, GREEN )
        value = self.font_points.render( f"{ str( self.apple_count ) }", True, GREEN )
        self.screen.blit( points , ( 550, 20 ) )
        self.screen.blit( value , ( 600, 40 ) )


    def randomApple( self ):

        self.apple = { 'x': random.randint( 0, C_WIDTH -1 ), 'y': random.randint( 0, C_HEIGHT - 1 ) }

        while True:

            if self.apple in self.snake.coordinates :
                self.apple = { 'x': random.randint( 0, C_WIDTH -1 ), 'y': random.randint( 0, C_HEIGHT - 1 ) }

            else:
                break



    def run( self ):

        while self.running :

            for event in pg.event.get():
                
                if event.type == pg.QUIT:
                    self.running = False

                if event.type == pg.KEYDOWN:

                    if event.key == pg.K_ESCAPE:
                        self.running = False

                    if event.key == pg.K_SPACE and self.game_current_state == 0:
                        self.game_current_state = 1

                    if event.key == pg.K_RETURN and self.game_current_state == 2:
                        self.snake = snake()
                        self.game_current_state = 0

                    #   KEYBOARD PROMPTS

                    if ( event.key == pg.K_LEFT or event.key == pg.K_a) and self.snake.direction != RIGHT :
                        self.snake.direction = LEFT
                        
                    if ( event.key == pg.K_RIGHT or event.key == pg.K_d) and self.snake.direction != LEFT :
                        self.snake.direction = RIGHT

                    if ( event.key == pg.K_UP or event.key == pg.K_w) and self.snake.direction != DOWN :
                        self.snake.direction = UP

                    if ( event.key == pg.K_DOWN or event.key == pg.K_s) and self.snake.direction != UP :
                        self.snake.direction = DOWN

            collision = self.checkCollision()

            if collision :
                self.game_current_state = 2 

            if self.game_current_state == 0:
                self.showInitialScreen()
                
            elif self.game_current_state == 1:
                self.showRunning()

            else:
                self.showGameOver()

            pg.display.update()

        self.destroy()

    def drawSnake( self ):

        for coordinate in self.snake.coordinates :
            x = coordinate[ 'x' ] * C_SIZE
            y = coordinate[ 'y' ] * C_SIZE
            snakerect = pg.Rect( x, y, C_SIZE, C_SIZE )
            pg.draw.rect( self.screen, DARKGREEN, snakerect)

    def drawApple( self ):

        x, y = self.apple[ 'x' ] * C_SIZE, self.apple[ 'y' ] * C_SIZE
        snakerect = pg.Rect( x, y, C_SIZE, C_SIZE )
        pg.draw.rect( self.screen, RED, snakerect)


    #   AGAINST WALL AND SNAKE BODY

    def checkCollision( self ):

        if ( self.snake.coordinates[ self.snake.HEAD ]['x'] == -1 or self.snake.coordinates[ self.snake.HEAD ]['y'] == -1 or self.snake.coordinates[ self.snake.HEAD ]['x'] == C_WIDTH or self.snake.coordinates[ self.snake.HEAD ]['y'] == C_HEIGHT  ):
            return True

        for snake_body in self.snake.coordinates[ 1: ] :

            if self.snake.coordinates[ self.snake.HEAD ]['x'] == snake_body['x'] and self.snake.coordinates[ self.snake.HEAD ]['y'] == snake_body['y']:
                return True

        return False

    def checkEatApple( self ):

        if self.snake.coordinates[ self.snake.HEAD ][ 'x' ] == self.apple[ 'x' ] and self.snake.coordinates[ self.snake.HEAD ][ 'y' ] == self.apple[ 'y' ] :
            self.apple_count += 1 
            return True

        return False

    def showInitialScreen( self ):
        
        self.screen.fill( BLACK )
        self.drawSnake()
        self.drawApple()
        
        #   ADD TRANSPARENT LAYER
        self.screen.blit( self.screen_fade, (0, 0) )

        text = self.font_.render( "PRESS SPACE TO BEGIN!!!", True, WHITE )
        self.screen.blit( text , ( 50, 200 ) )

    def showRunning( self ):

        self.screen.fill( BLACK )
        new_head = None

        if self.snake.direction == UP :
            new_head = { 'x' : self.snake.coordinates[ self.snake.HEAD ][ 'x' ], 'y' : self.snake.coordinates[ self.snake.HEAD ][ 'y' ] - 1 }
        
        elif self.snake.direction == DOWN :
            new_head = { 'x' : self.snake.coordinates[ self.snake.HEAD ][ 'x' ], 'y' : self.snake.coordinates[ self.snake.HEAD ][ 'y' ] + 1 }
        
        elif self.snake.direction == RIGHT :
            new_head = { 'x' : self.snake.coordinates[ self.snake.HEAD ][ 'x' ] + 1, 'y' : self.snake.coordinates[ self.snake.HEAD ][ 'y' ] }
        
        elif self.snake.direction == LEFT :
            new_head = { 'x' : self.snake.coordinates[ self.snake.HEAD ][ 'x' ] - 1, 'y' : self.snake.coordinates[ self.snake.HEAD ][ 'y' ] }

        self.snake.coordinates.insert( 0, new_head )
        del self.snake.coordinates[ -1 ]
        
        self.screen.fill( BLACK )
        self.drawSnake()
        self.drawApple()
        self.display_points()
        
        if self.checkEatApple() :
            second_last, last = self.snake.coordinates[ -2 ], self.snake.coordinates[ -1 ]

            if second_last[ 'x' ] == last[ 'x' ]:
                self.snake.coordinates.append( { 'x' : last['x'] , 'y' : last['y'] + 1 } )
                
            else:
                self.snake.coordinates.append( { 'x' : last['x'] + 1, 'y' : last['y'] } )
                
            self.randomApple()
            self.drawApple()

        pg.display.update()
        self.clock.tick( self.FPS ) 

    def showGameOver( self ):

        gameover = self.font_.render( "GAME OVER!!", True, RED )
        play_again = self.font_.render( "PRESS ENTER TO RESTART!!", True, WHITE )
        self.screen.fill( BLACK )
        self.drawSnake()
        self.screen.blit( self.screen_fade, (0, 0) )
        self.display_points()
        self.screen.blit( gameover, ( 200, 100 ) )
        self.screen.blit( play_again, ( 35, 200 ) )

    def destroy( self ):

        pg.quit()

class snake:

    def __init__(self) -> None:

        self.HEAD = 0
        self.direction = UP
        self.get_random()
    
    def get_random( self ):

        self.start_x = random.randint( 10, C_WIDTH - 10 )
        self.start_y = random.randint( 10, C_HEIGHT - 10 )
        self.coordinates = [
            { 'x' : self.start_x, 'y' : self.start_y },
            { 'x' : self.start_x - 1 , 'y' : self.start_y },
            { 'x' : self.start_x - 2 , 'y' : self.start_y }
        ]


if __name__ == "__main__":
    
    g = gamefield()
    g.run()