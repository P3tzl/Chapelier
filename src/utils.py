import os 
import pygame as pg 
import time

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ )))

def import_flag(flag):
    if flag not in {"flag_be", "flag_fr", "flag_x", "flag_rma"}:
        raise ValueError("Flag must be in {flag_be, flag_fr, flag_x, flag_rma}")
    flag_files = [f for f in os.listdir(os.path.join(ROOT_PATH, "figures",str(flag))) if not f.startswith('.')]
    flag_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    flag_requested = [pg.image.load(os.path.join(ROOT_PATH, "figures",str(flag),file)) for file in flag_files]
    return flag_requested

def scale_flag(flag,value):
    """Transforms a set of given flag files with a given value

    Args:
        flag (array): array of flag files 
        value (int): integer to use in the formula 
        
    Output: 
        Array of transformed flag files
        Width of the flag 
        Height of the flag
    """
    new_flag = [pg.transform.scale(f, (f.get_width()/f.get_height()*value, value)) for f in flag]
    return new_flag

def flip_flag(flag,value):
    new_flag = [pg.transform.flip(pg.transform.scale(image,(image.get_width()/image.get_height()*value,value)),flip_x=True,flip_y=False) for image in flag]
    return new_flag 

def import_fonts():
    font_30 = pg.font.Font(os.path.join(ROOT_PATH,"figures","fonts","04B_30__.TTF"), 30)
    font_50 = pg.font.Font(os.path.join(ROOT_PATH,"figures","fonts","04B_30__.TTF"), 50)
    font_70 = pg.font.Font(os.path.join(ROOT_PATH,"figures","fonts","04B_30__.TTF"), 70)
    return [font_30, font_50, font_70]

def prepare_flags():
    country_flags = ["flag_be", "flag_fr"]
    school_flags = ["flag_x", "flag_rma"]
    flags = country_flags + school_flags
    [flag_be, flag_fr, flag_x, flag_rma] = [import_flag(flag) for flag in flags]
    flag_rma = scale_flag(flag_rma, 105)
    flag_x = scale_flag(flag_x, 105)
    flag_be = flip_flag(flag_be, 40)
    flag_fr = flip_flag(flag_fr, 40)
    return [flag_be, flag_fr, flag_x, flag_rma]


class Countdown:
    """
    Countdown element
    """
    def __init__(self,screen:pg.Surface,start:float,duration:int,font:pg.font.Font,color:tuple=(255,255,255)):
        self.screen = screen
        self.start = start
        self.duration = duration
        self.color = color
        self.font = font
    
    def blit(self):
        """
        Render the Countdown
        """
        time_left = self.duration*60-round(time.time()-self.start)
        timer = self.font.render((time_left<60*10)*"0"+str(time_left//60)+":"+(time_left%60<10)*"0"+str(time_left%60),True,self.color)
        timer_rect = timer.get_rect()
        timer_rect.center = (self.screen.get_width()//2,100)
        self.screen.blit(timer,timer_rect)
      
  
class Distancemarkers:
    """
    Distance markers
    """
    def __init__(self,screen:pg.Surface,font:pg.font.Font,interval:int,ypos:int,color:tuple = (255,255,255)):
        """
        Args:
            interval (int): Interval between each marker (m)
            ypos (int): Vertical position on the screen, with the center as reference
        """
        self.screen = screen
        self.font = font
        self.color = color
        self.interval = interval
        self.ypos = ypos
    
    def blit(self,distance:int):
        """
        Render the distance marker
        """
        for i in range(distance//self.interval-distance//1000,distance//self.interval-distance//1000+3):
            distance_marker = pg.transform.rotate(self.font.render(str(i*self.interval/1e3)+"km", True, self.color),-90)
            distance_marker_rect = distance_marker.get_rect()
            distance_marker_rect.midleft = (i*self.interval*5-distance*4,self.screen.get_height()//2-self.ypos)
            self.screen.blit(distance_marker,distance_marker_rect)