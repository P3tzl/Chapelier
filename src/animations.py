import utils as ut 
import pygame as pg 
import sys 
import time 
import pyrow.pyrow as pr


def render_text(screen:pg.Surface,font:pg.font.Font,text:str,pos:tuple,color:tuple=(255,255,255),rotation:int=0):
    """Render text
    Args:
        text (str): text to display
        pos (tuple): (x,y) position
    """
    text_obj = pg.transform.rotate(font.render(text,True,color),rotation)
    text_rect = text_obj.get_rect(centerx=pos[0],centery=pos[1])
    screen.blit(text_obj,text_rect)

def button(screen:pg.Surface,text:str,font:pg.font.Font,pos:tuple[int],size:tuple[int],color:tuple=(255,255,255)):
    render_text(screen,font,text,(pos[0],pos[1]),color)
    box = pg.Rect(0,0,size[0],size[1])
    box.center = (pos[0],pos[1])
    pg.draw.rect(screen,color,box,7,40)
    return box

def quit():
    pg.display.quit()
    pg.quit()
    sys.exit()


class Background:
    def __init__(self,screen:pg.Surface,image:pg.Surface,speed:int):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.image = image
        self.speed = speed
        
    def blit(self,distance):
        """
        Render the background
        """
        self.screen.blit(self.image,((-distance*self.speed)%-self.image.get_width(),-550),(0,0,self.image.get_width(),self.image.get_height()))
        self.screen.blit(self.image,(self.image.get_width()+(-distance*self.speed)%-self.image.get_width(),-550),(0,0,self.image.get_width(),self.image.get_height()))
        pass

class Boat:
    def __init__(self,screen:pg.Surface,image:pg.Surface,flag:list[pg.Surface],ypos:int):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.image = image
        self.height_image = image.get_height()
        self.width_image = image.get_width()
        self.flag = flag
        self.length = len(flag)
        self.ypos = ypos
        self.count = 0
        
    def blit(self,distance):
        """
        Render the boat
        """
        self.screen.blit(self.image,(distance,self.height//2-self.height_image//2-self.ypos))
        self.screen.blit(self.flag[(self.count)%self.length],(distance-10,self.height//2-self.ypos+13))
        self.count += 1

class AnimatedFlag:
    def __init__(self,screen:pg.Surface,images:list[pg.Surface],position:tuple[int]):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.images = images
        self.length = len(images)
        self.position = position
        self.count = 0
    
    def blit(self):
        """
        Render flag
        """
        self.screen.blit(self.images[(self.count)%self.length],(self.width//2+self.position[0],self.height//2-self.position[1]))
        self.count += 1

class Countdown:
    def __init__(self,screen:pg.Surface,start:float,duration:int,font:pg.font.Font,color:tuple=(255,255,255)):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.start = start
        self.duration = duration
        self.color = color
        self.font = font
    
    def blit(self):
        """
        Render the Countdown
        """
        time_left = self.duration*60-round(time.time()-self.start)
        render_text(self.screen,self.font,
                    (time_left<60*10)*"0"+str(time_left//60)+":"+(time_left%60<10)*"0"+str(time_left%60),
                    (self.width//2,100),self.color)


BLUE = (0,80,239)
BLACK = (0,0,0)
GREEN = (0,138,0)
RED = (229,20,0)
WHITE = (255,255,255)
GOLD = (248,217,73)
SILVER = (170,169,173)

class Menu: 
    def __init__(self,screen: pg.Surface,fonts:list[pg.font.Font],clock:pg.time.Clock,fps:int,background: Background, boat_x: Boat, boat_rma : Boat, flags:list[AnimatedFlag], colorswappers:list[ut.ColorSwapper]):
        self.screen = screen 
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.font_10 = fonts[0]
        self.font_30 = fonts[1]
        self.font_50 = fonts[2]
        self.font_70 = fonts[3]
        self.font_90 = fonts[4]
        self.clock = clock
        self.fps = fps 
        self.background = background
        self.colorswapper_x = colorswappers[0]
        self.colorswapper_rma = colorswappers[1]
        self.flag_x = flags[0]
        self.flag_rma = flags[1]
        self.boat_x = boat_x
        self.boat_rma = boat_rma 
        
        
    def main(self):
        """
        Shows main screen of application
        """
        play_color = quit_color = WHITE 
        self.background.blit(0)
        s = pg.Surface((self.width,self.height))
        s.set_alpha(200)
        s.fill((0,0,0))
        self.screen.blit(s,(0,0))
        self.boat_rma.blit(0)
        self.boat_x.blit(0)
        render_text(self.screen,self.font_10,"Bouzin Prakopetz Vancanneyt (174 POL)",(200,10))
        button(self.screen,"Main Menu",self.font_70,(self.width//2,self.height//2-200),(700,100))
        
        while True:
            play_button = button(self.screen,"Play",self.font_50,(self.width//2,self.height//2-50),(300,75),play_color)
            quit_button = button(self.screen,"Quit",self.font_50,(self.width//2,self.height//2+50),(300,75),quit_color)

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
            self.clock.tick(self.fps)
            
    def play(self):
        user_input = ""
        play_color = WHITE
        back_color = WHITE
        while True:
            self.background.blit(0)
            s = pg.Surface((self.width,self.height))
            s.set_alpha(200)
            s.fill((0,0,0))
            self.screen.blit(s,(0,0))
            self.boat_rma.blit(0)
            self.boat_x.blit(0)
            render_text(self.screen,self.font_10,"Bouzin Prakopetz Vancanneyt (174 POL)",(200,10))
            button(self.screen,"Play Menu",self.font_70,(self.width//2,self.height//2-200),(700,100))
            button(self.screen,"Time: "+user_input+" min",self.font_50,(self.width//2,self.height//2-50),(700,75))
            play_button = button(self.screen,"Connect",self.font_50,(self.width//2+180,self.height//2+50),(340,75),play_color)
            back_button = button(self.screen,"Back",self.font_50,(self.width//2-180,self.height//2+50),(340,75),back_color)
            
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
            self.clock.tick(self.fps)

    def connect(self):
        quit_color = WHITE
        start_color = WHITE
        self.background.blit(0)
        s = pg.Surface((self.width,self.height))
        s.set_alpha(200)
        s.fill((0,0,0))
        self.screen.blit(s,(0,0))
        self.boat_rma.blit(0)
        self.boat_x.blit(0)
        render_text(self.screen,self.font_10,"Bouzin Prakopetz Vancanneyt (174 POL)",(200,10))
        button(self.screen,"Main Menu",self.font_70,(self.width//2,self.height//2-200),(700,100))
        render_text(self.screen,self.font_50,"CONNECT MACHINES",(self.width//2,self.height//2),RED)

        available_machines = []
        while len(available_machines) < 2:
            quit_button = button(self.screen,"Quit",self.font_50,(self.width//2,self.height//2+100),(350,75),quit_color)
            mx,my = pg.mouse.get_pos()
            available_machines = [pr.PyErg(machine) for machine in list(pr.find())]
            machine_colors = len(available_machines)*[WHITE]
            assigned_machines = len(available_machines)//2*2*[None]
            for event in pg.event.get():
                if quit_button.collidepoint(mx,my):
                    quit_color = RED
                    if event.type == pg.MOUSEBUTTONDOWN:
                        return "quit"
                else:
                    quit_color = WHITE
            pg.display.flip()
            self.clock.tick(self.fps)

        self.background.blit(0)
        s = pg.Surface((self.width,self.height))
        s.set_alpha(200)
        s.fill((0,0,0))
        self.screen.blit(s,(0,0))
        self.boat_rma.blit(0)
        self.boat_x.blit(0)
        render_text(self.screen,self.font_10,"Bouzin Prakopetz Vancanneyt (174 POL)",(200,10))
        button(self.screen,"Main Menu",self.font_70,(self.width//2,self.height//2-200),(700,100))

        while True:
            quit_button = button(self.screen,"Quit",self.font_50,(self.width//2+180,self.height//2-50),(300,75),quit_color)
            start_button = button(self.screen,"Start",self.font_50,(self.width//2-180,self.height//2-50),(300,75),start_color)
            machine_buttons = [button(self.screen,machine.get_erg()["serial"],self.font_30,(self.width//2+(-1)**((i+1)%2)*180,self.height*2//3+(i//2-1)*100),(340,75),machine_colors[i]) for i, machine in enumerate(available_machines)]

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
                    if start_button.collidepoint(mx,my):
                        start_color = GREEN
                        if event.type == pg.MOUSEBUTTONDOWN:
                            start = time.time()
                            while time.time() - start < 5:
                                self.background.blit(0)
                                s = pg.Surface((self.width,self.height))
                                s.set_alpha(200)
                                s.fill((0,0,0))
                                self.screen.blit(s,(0,0))
                                self.boat_rma.blit(0)
                                self.boat_x.blit(0)
                                render_text(self.screen,self.font_10,"Bouzin Prakopetz Vancanneyt (174 POL)",(200,10))
                                render_text(self.screen,self.font_90,str(round(5-time.time()-start)),(self.width//2,self.height//2-200))
                                pg.display.flip()
                                self.clock.tick(self.fps)
                            return assigned_machines
                    else:
                        start_color = WHITE

            pg.display.flip()
            self.clock.tick(self.fps)

    def options(self,options_time):
        """
        Shows options screen of application
        """
        continue_color = back_color = WHITE 
        s = pg.Surface((self.width,self.height))
        s.set_alpha(200)
        s.fill((0,0,0))
        self.screen.blit(s,(0,0))
        while True:
            continue_button = button(self.screen,"Continue",self.font_50,(self.width//2,self.height//2-50),(375,75),continue_color)
            back_button = button(self.screen,"Quit",self.font_50,(self.width//2,self.height//2+50),(375,75),back_color)
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
            self.clock.tick(self.fps)
  
    def end(self, scores:list):
        """
        Shows end screen of application
        """
        continue_color = WHITE
        s = pg.Surface((self.width,self.height))
        s.set_alpha(200)
        s.fill((0,0,0))
        self.screen.blit(s,(0,0))
        if scores[0][0] < scores[1][0]:
            scores.reverse()
        render_text(self.screen,self.font_90,"Winner!",(self.width//2,self.height//2-375))
        render_text(self.screen,self.font_50,"1st "+str(round(scores[0][0]))+" m",(self.width//2,self.height//2),GOLD)
        render_text(self.screen,self.font_30,"2nd "+str(round(scores[1][0]))+" m",(self.width//2,self.height//2+75),SILVER)
        old_ypos = scores[0][1].ypos
        while True:
            scores[0][1].ypos = 200
            scores[0][1].blit(self.width//2-scores[0][1].width_image//2)
            continue_button = button(self.screen,"Continue",self.font_50,(self.width//2,self.height//2+200),(375,75),continue_color)
            mx,my = pg.mouse.get_pos()
            for event in pg.event.get():
                if continue_button.collidepoint(mx,my):
                    continue_color = RED
                    if event.type == pg.MOUSEBUTTONDOWN:
                        scores[0][1].ypos = old_ypos
                        return
                else:
                    continue_color = WHITE
            pg.display.flip()
            self.clock.tick(self.fps)
    
    def game(self,total_time:int,machines:list[pr.PyErg]):
        location = lambda x: 1 - 1/(x/200 + 1)
        for machine in machines:
            machine.set_clock()
        machines_rma = machines[:len(machines)//2]
        machines_x = machines[len(machines)//2:]
        countdown = Countdown(self.screen,time.time(),total_time,self.font_50,WHITE)
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

            # Retrieve distances. RMA as reference
            try:
                distance_rma = sum([machine.get_monitor()["distance"] for machine in machines_rma])
                distance_x = sum([machine.get_monitor()["distance"] for machine in machines_x])
                delta = distance_rma-distance_x
            except:
                print("DISTANCE ERROR")

            # Swapping colors
            color_rma = self.colorswapper_rma.swap(distance_rma,400,duration)
            color_x = self.colorswapper_x.swap(distance_x,400,duration)

            # Rendering of elements
            self.background.blit(min(distance_rma,distance_x))
            self.flag_rma.blit()
            self.flag_x.blit()
            self.boat_rma.blit(location(max(0,delta))*self.width)
            self.boat_x.blit(location(max(0,-delta))*self.width)
            countdown.blit()

            render_text(self.screen,self.font_30,"VS",(self.width//2,self.height//2))
            render_text(self.screen,self.font_50,str(round(distance_rma)) + "m",(self.width//2+400,self.height//2),color=color_rma)
            render_text(self.screen,self.font_50,str(round(distance_x)) + "m",(self.width//2-400,self.height//2),color=color_x)
            render_text(self.screen,self.font_10,"Bouzin Prakopetz Vancanneyt (174 POL)",(200,10))

            # Options button
            options_button = button(self.screen,"Options",self.font_30,(self.width-150,50),(250,50),options_color)
            mx,my = pg.mouse.get_pos()
            for event in pg.event.get():
                if options_button.collidepoint(mx,my):
                    options_color = RED
                    if event.type == pg.MOUSEBUTTONDOWN:
                        return_options = self.options(time.time())
                        if return_options == "quit":
                            return return_options
                        else:
                            countdown.start += return_options
                else:
                    options_color = WHITE

            # Pygame stuff
            pg.display.flip()
            self.clock.tick(self.fps)
            self.screen.fill(BLACK)
            count += 1
        return [[distance_rma,self.boat_rma],[distance_x,self.boat_x]]
    