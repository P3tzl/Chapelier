import pygame as pg
import sys
import os 
import time 
import utils as ut
import pyrow.pyrow as pr
from threading import Thread

# Standard 
BLUE = (0,80,239)
BLACK = (0,0,0)
GREEN = (0,138,0)
RED = (229,20,0)
WHITE = (255,255,255)
GOLD = (248,217,73)
SILVER = (170,169,173)

# Initializing
pg.init()

# Importing all images/fonts
[flag_be, flag_fr, flag_rma, flag_x] = ut.prepare_flags()
boat = pg.transform.scale(pg.image.load(os.path.join(".", "figures","warship.png")),(375,375))
background_image = pg.transform.scale(pg.image.load(os.path.join(".", "figures","canal.png")),(4000,2000))
[font_10, font_30, font_50, font_70, font_90] = [ut.import_fonts(size) for size in [10,30,50,70,90]]

# Screen parameters
clock = pg.time.Clock()
fps = 30
screen = pg.display.set_mode((1600,900),pg.SCALED)
width = screen.get_width()
height = screen.get_height()
pg.display.set_caption("Chapelié")
pg.display.set_icon(boat)

# Assigning all utilites
speed = 4
colorswapper_rma = ut.ColorSwapper([WHITE,GREEN],.2,10)
colorswapper_x = ut.ColorSwapper([WHITE,GREEN],.2,10)
background = ut.Background(screen,background_image,speed)
boat_rma = ut.Boat(screen,boat,flag_be,175)
boat_x = ut.Boat(screen,boat,flag_fr,-75)
flag_rma = ut.AnimatedFlag(screen,flag_rma,(-100-flag_rma[0].get_width(),flag_rma[0].get_height()//2))
flag_x = ut.AnimatedFlag(screen,flag_x,(100,flag_x[0].get_height()//2))

# Distance to screen x location
location = lambda x: 1 - 1/(x/1000 + 1)

def button(text:str,font:pg.font.Font,pos:tuple[int],size:tuple[int],color:tuple=WHITE):
    ut.render_text(screen,font,text,(pos[0],pos[1]),color)
    box = pg.Rect(0,0,size[0],size[1])
    box.center = (pos[0],pos[1])
    pg.draw.rect(screen,color,box,7,40)
    return box

def quit():
    pg.display.quit()
    pg.quit()
    sys.exit()
    
def options(options_time:int):
    continue_color = WHITE
    back_color = WHITE
    s = pg.Surface((width,height))
    s.set_alpha(200)
    s.fill((0,0,0))
    screen.blit(s,(0,0))
    while True:
        continue_button = button("Continue",font_50,(width//2,height//2-50),(375,75),continue_color)
        back_button = button("Quit",font_50,(width//2,height//2+50),(375,75),back_color)
        mx,my = pg.mouse.get_pos()
        for event in pg.event.get():
            if continue_button.collidepoint(mx,my):
                continue_color = RED
                if event.type == pg.MOUSEBUTTONDOWN:
                    return time.time() - options_time
            else:
                continue_color = WHITE
            if back_button.collidepoint(mx,my):
                back_color = RED
                if event.type == pg.MOUSEBUTTONDOWN:
                    return "quit"
            else:
                back_color = WHITE
        pg.display.flip()
        clock.tick(fps)

def game(total_time:int,machines:list[pr.PyErg]):
    for machine in machines:
        machine.set_clock()
    machines_rma = machines[:len(machines)//2]
    machines_x = machines[len(machines)//2:]
    countdown = ut.Countdown(screen,time.time(),total_time,font_50,WHITE)
    options_color = WHITE
    count = 0
    distance_rma = 0
    distance_x = 0
    delta = 0
    start = time.time()
    duration = 0
    while duration < total_time:
        # Time
        duration = time.time()-start

        # Retrieve distances. Distance difference with rma as reference
        try:
            distance_rma = sum([machine.get_monitor()["distance"] for machine in machines_rma])
            distance_x = sum([machine.get_monitor()["distance"] for machine in machines_x])
            delta = distance_rma-distance_x
        except:
            print("DISTANCE ERROR")

        # Swapping colors
        color_rma = colorswapper_rma.swap(distance_rma,400,duration)
        color_x = colorswapper_x.swap(distance_x,400,duration)

        # Rendering of elements
        background.blit(min(distance_rma,distance_x))
        flag_rma.blit()
        flag_x.blit()
        boat_rma.blit(location(max(0,delta))*width)
        boat_x.blit(location(max(0,-delta))*width)
        countdown.blit()

        ut.render_text(screen,font_30,"VS",(width//2,height//2))
        ut.render_text(screen,font_50,str(round(distance_rma)) + "m",(width//2+400,height//2),color=color_rma)
        ut.render_text(screen,font_50,str(round(distance_x)) + "m",(width//2-400,height//2),color=color_x)
        ut.render_text(screen,font_10,"Bouzin Philippot Prakopetz Vancanneyt (174 POL)",(200,10))

        # Options button
        options_button = button("Options",font_30,(width-150,50),(250,50),options_color)
        mx,my = pg.mouse.get_pos()
        for event in pg.event.get():
            if options_button.collidepoint(mx,my):
                options_color = RED
                if event.type == pg.MOUSEBUTTONDOWN:
                    return_options = options(time.time())
                    if return_options == "quit":
                        return return_options
                    else:
                        countdown.start += return_options
            else:
                options_color = WHITE
        
        # Pygame stuff
        pg.display.flip()
        clock.tick(fps)
        screen.fill(BLACK)
        count += 1
    return [[distance_rma,boat_rma],[distance_x,boat_x]]

def connect_menu():
    quit_color = WHITE
    background.blit(0)
    s = pg.Surface((width,height))
    s.set_alpha(200)
    s.fill((0,0,0))
    screen.blit(s,(0,0))
    boat_rma.blit(0)
    boat_x.blit(0)
    ut.render_text(screen,font_10,"Bouzin Philippot Prakopetz Vancanneyt (174 POL)",(200,10))
    button("Main Menu",font_70,(width//2,height//2-200),(700,100))

    available_machines = [pr.PyErg(machine) for machine in list(pr.find())]
    machine_colors = len(available_machines)*[WHITE]
    assigned_machines = len(available_machines)//2*2*[None]
    while True:
        quit_button = button("Quit",font_50,(width//2,height//2-50),(300,75),quit_color)        
        machine_buttons = [button(machine.get_erg()["serial"],font_30,(width//2+(-1)**((i+1)%2)*180,height*2//3+(i//2-1)*100),(340,75),machine_colors[i]) for i, machine in enumerate(available_machines)]
        
        if assigned_machines.index(None) >= len((available_machines))//2:
            current_color = BLUE
        else:
            current_color = RED
            
        mx,my = pg.mouse.get_pos()
        for event in pg.event.get():
            for i, machine in enumerate(machine_buttons):
                if machine.collidepoint(mx,my):
                    if available_machines[i] in assigned_machines:
                        if event.type == pg.MOUSEBUTTONDOWN:
                            assigned_machines[assigned_machines.index(available_machines[i])] = None
                            machine_colors[i] = WHITE
                    else:
                        machine_colors[i] = current_color
                        if event.type == pg.MOUSEBUTTONDOWN:
                            assigned_machines[assigned_machines.index(None)] = available_machines[i]
                            
                elif available_machines[i] not in assigned_machines:
                    machine_colors[i] = WHITE

            if quit_button.collidepoint(mx,my):
                quit_color = RED
                if event.type == pg.MOUSEBUTTONDOWN:
                    return "quit"
            else:
                quit_color = WHITE
            
            if None not in assigned_machines:
                return assigned_machines

        pg.display.flip()
        clock.tick(fps)

def main_menu():
    play_color = WHITE
    quit_color = WHITE
    background.blit(0)
    s = pg.Surface((width,height))
    s.set_alpha(200)
    s.fill((0,0,0))
    screen.blit(s,(0,0))
    boat_rma.blit(0)
    boat_x.blit(0)
    ut.render_text(screen,font_10,"Bouzin Philippot Prakopetz Vancanneyt (174 POL)",(200,10))
    button("Main Menu",font_70,(width//2,height//2-200),(700,100))
    
    while True:
        play_button = button("Play",font_50,(width//2,height//2-50),(350,75),play_color)
        quit_button = button("Quit",font_50,(width//2,height//2+50),(350,75),quit_color)

        mx,my = pg.mouse.get_pos()
        for event in pg.event.get():
            if play_button.collidepoint(mx,my):
                play_color = RED
                if event.type == pg.MOUSEBUTTONDOWN:
                    return "play"
            else:
                play_color = WHITE
                    
            if quit_button.collidepoint(mx,my):
                quit_color = RED
                if event.type == pg.MOUSEBUTTONDOWN:
                    return "quit"
            else:
                quit_color = WHITE
            
        pg.display.flip()
        clock.tick(fps)

def play_menu():
    user_input = ""
    play_color = WHITE
    back_color = WHITE
    while True:
        background.blit(0)
        s = pg.Surface((width,height))
        s.set_alpha(200)
        s.fill((0,0,0))
        screen.blit(s,(0,0))
        boat_rma.blit(0)
        boat_x.blit(0)
        ut.render_text(screen,font_10,"Bouzin Philippot Prakopetz Vancanneyt (174 POL)",(200,10))
        button("Play Menu",font_70,(width//2,height//2-200),(700,100))
        button("Time: "+user_input+" min",font_50,(width//2,height//2-50),(700,75))
        play_button = button("Connect",font_50,(width//2+180,height//2+50),(340,75),play_color)
        back_button = button("Back",font_50,(width//2-180,height//2+50),(340,75),back_color)
        
        mx,my = pg.mouse.get_pos()
        for event in pg.event.get():
            if back_button.collidepoint(mx,my):
                back_color = RED
                if event.type == pg.MOUSEBUTTONDOWN:
                    return
            else:
                back_color = WHITE
            
            if play_button.collidepoint(mx,my):
                play_color = RED
                if event.type == pg.MOUSEBUTTONDOWN:
                    if len(user_input) > 0:
                        if int(user_input) > 0:
                            return int(user_input)
            else:
                play_color = WHITE
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.unicode.isnumeric() and int(user_input+event.unicode) < 60*9:
                    user_input += event.unicode
                    user_input = user_input[:4]
                
        pg.display.flip()
        clock.tick(fps)

def end_menu(scores:list):
    continue_color = WHITE
    s = pg.Surface((width,height))
    s.set_alpha(200)
    s.fill((0,0,0))
    screen.blit(s,(0,0))
    if scores[0][0] < scores[1][0]:
        scores.reverse()
    ut.render_text(screen,font_90,"Winner!",(width//2,height//2-375))
    ut.render_text(screen,font_50,"1st "+str(round(scores[0][0]))+" m",(width//2,height//2),GOLD)
    ut.render_text(screen,font_30,"2nd "+str(round(scores[1][0]))+" m",(width//2,height//2+75),SILVER)
    while True:
        scores[0][1].ypos = 200
        scores[0][1].blit(width//2-scores[0][1].width_image//2)
        continue_button = button("Continue",font_50,(width//2,height//2+200),(375,75),continue_color)
        mx,my = pg.mouse.get_pos()
        for event in pg.event.get():
            if continue_button.collidepoint(mx,my):
                continue_color = RED
                if event.type == pg.MOUSEBUTTONDOWN:
                    return
            else:
                continue_color = WHITE
        pg.display.flip()
        clock.tick(fps)

def main():
    while True:
        return_menu = main_menu()
        if return_menu == "play":
            return_play = play_menu()
            if type(return_play) == int:
                return_connect = connect_menu()
                if return_connect == tuple[pr.PyErg]:
                    return_game = game(return_play[0],return_play[1],return_connect)
                    if return_game == "quit":
                        continue
                    else:
                        end_menu(return_game)
                else:
                    continue
            else:
                continue
        else:
            quit()

main()