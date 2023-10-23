import utils as ut 
import pygame as pg 
import sys 
import time 



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
    ut.render_text(screen,font,text,(pos[0],pos[1]),color)
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
        ut.render_text(self.screen,self.font,
                    (time_left<60*10)*"0"+str(time_left//60)+":"+(time_left%60<10)*"0"+str(time_left%60),
                    (self.width//2,100),self.color)


WHITE = (255,255,255)
RED = (229,20,0)
GOLD = (248,217,73)
SILVER = (170,169,173)
class Menu: 
    def __init__(self,screen: pg.Surface,fonts:list[pg.font.Font],clock:pg.time.Clock,fps:int,background: Background, boat_x: Boat, boat_rma : Boat,options_time:int):
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
        self.boat_x = boat_x
        self.boat_rma = boat_rma 
        self.options_time = options_time #TODO: Look at what happens if this changes
        
        
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
        ut.render_text(self.screen,self.font_10,"Bouzin Philippot Prakopetz Vancanneyt (174 POL)",(200,10))
        button("Main Menu",self.font_70,(self.width//2,self.height//2-200),(600,100))
        
        while True:
            play_button = button("Play",self.font_50,(self.width//2,self.height//2-50),(300,75),play_color)
            quit_button = button("Quit",self.font_50,(self.width//2,self.height//2+50),(300,75),quit_color)

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
        
    def options(self):
        """
        Shows options screen of application
        """
        continue_color = back_color = WHITE 
        s = pg.Surface((self.width,self.height))
        s.set_alpha(200)
        s.fill((0,0,0))
        self.screen.blit(s,(0,0))
        while True:
            continue_button = button("Continue",self.font_50,(self.width//2,self.height//2-50),(375,75),continue_color)
            back_button = button("Quit",self.font_50,(self.width//2,self.height//2+50),(375,75),back_color)
            mx,my = pg.mouse.get_pos()
            for event in pg.event.get():
                if continue_button.collidepoint(mx,my):
                    continue_color = RED
                    if event.type == pg.MOUSEBUTTONDOWN:
                        return time.time() - self.options_time
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
        
    
    def calibrate():
        #TODO: fill in later with screen to pick boats from serial numbers 
        pass 
        
    def game():
        pass 
    
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
        ut.render_text(self.screen,self.font_90,"Winner!",(self.width//2,self.height//2-375))
        ut.render_text(self.screen,self.font_50,"1st "+str(round(scores[0][0]))+" m",(self.width//2,self.height//2),GOLD)
        ut.render_text(self.screen,self.font_30,"2nd "+str(round(scores[1][0]))+" m",(self.width//2,self.height//2+75),SILVER)
        while True:
            scores[0][1].ypos = 200
            scores[0][1].blit(self.width//2-scores[0][1].width_image//2)
            continue_button = button("Continue",self.font_50,(self.width//2,self.height//2+200),(375,75),continue_color)
            mx,my = pg.mouse.get_pos()
            for event in pg.event.get():
                if continue_button.collidepoint(mx,my):
                    continue_color = RED
                    if event.type == pg.MOUSEBUTTONDOWN:
                        return
                else:
                    continue_color = WHITE
            pg.display.flip()
            self.clock.tick(self.fps)
    


