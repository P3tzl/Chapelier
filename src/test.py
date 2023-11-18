import pygame as pg
import sys
import os 
import utils as ut
import animations as an

# Standard 
BLUE = (0,80,239)
BLACK = (0,0,0)
GREEN = (0,138,0)
RED = (229,20,0)
WHITE = (255,255,255)
GOLD = (248,217,73)
SILVER = (170,169,173)

def main():
    # Initializing
    pg.init()

    # Importing all images/fonts
    [flag_be, flag_fr, flag_rma, flag_x] = ut.prepare_flags()
    boat = pg.transform.scale(pg.image.load(os.path.join(".", "figures","warship.png")),(375,375))
    boat_be = pg.transform.scale(pg.image.load(os.path.join(".", "figures","warshipbe.png")),(375,375))
    boat_fr = pg.transform.scale(pg.image.load(os.path.join(".", "figures","warshipfr.png")),(375,375))
    background_image = pg.transform.scale(pg.image.load(os.path.join(".", "figures","canal.png")),(4000,2000))
    fonts = [ut.import_fonts(size) for size in [10,30,50,70,90]]

    # Screen parameters
    clock = pg.time.Clock()
    fps = 30
    screen = pg.display.set_mode((1600,900),pg.SCALED)
    pg.display.set_caption("Chapelié")
    pg.display.set_icon(boat)

    # Assigning all utilites
    speed = 4
    colorswapper_rma = ut.ColorSwapper([WHITE,GREEN],.2,10)
    colorswapper_x = ut.ColorSwapper([WHITE,GREEN],.2,10)
    background = an.Background(screen,background_image,speed)
    boat_rma = an.Boat(screen,boat_be,flag_be,175)
    boat_x = an.Boat(screen,boat_fr,flag_fr,-75)
    flag_rma = an.AnimatedFlag(screen,flag_rma,(-100-flag_rma[0].get_width(),flag_rma[0].get_height()//2))
    flag_x = an.AnimatedFlag(screen,flag_x,(100,flag_x[0].get_height()//2))

    game = an.Menu(screen,fonts,clock,fps,background,boat_x,boat_rma,[flag_x,flag_rma],[colorswapper_x,colorswapper_rma])

    while True:
        return_menu = game.main()
        if return_menu == "play":
            return_play = game.play()
            if type(return_play) == int:
                return_connect = game.connect()
                if type(return_connect) == list:
                    return_game = game.game(return_play,return_connect)
                    if return_game == "quit":
                        continue
                    else:
                        game.end(return_game)
                else:
                    continue
            else:
                continue
        else:
            pg.display.quit()
            pg.quit()
            sys.exit()
            
if __name__ == '__main__':
    main()