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

def import_fonts(fontsize:int):
    return pg.font.Font(os.path.join(ROOT_PATH,"figures","fonts","04B_30__.TTF"), fontsize)

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

def render_text(screen:pg.Surface,font:pg.font.Font,text:str,pos:tuple,color:tuple=(255,255,255),rotation:int=0):
    """Render text
    Args:
        text (str): text to display
        pos (tuple): (x,y) position
    """
    text_obj = pg.transform.rotate(font.render(text,True,color),rotation)
    text_rect = text_obj.get_rect(centerx=pos[0],centery=pos[1])
    screen.blit(text_obj,text_rect)

def get_distance():
    return

def get_data_streams():
    devices = list(pr.find())
    print(f"Found {len(devices)} erg(s)") #Debugging statement
    ergs = [pr.PyErg(device) for device in devices]
    return ergs

def calibrate_ergs(ergs):
    print("Row the Belgian boat")
    while True:
        for erg in ergs:
            data1 = erg.get_monitor()['distance']
            if data1 > 0:
                belgian_erg = erg
                french_erg = [erg for erg in ergs if erg != french_erg][0]
                print("Boats are calibrated")
                return [belgian_erg, french_erg]

class ColorSwapper:
    def __init__(self,colors:list[tuple],r:int,n:int):
        """
            colors (list[tuple]): The two colors to swap between
            r (int): The rate at which to swap (#/s)
            n (int): Maximal amount of swaps
        """
        self.colors = colors
        self.rate = r
        self.count = n
        self.max = n
        
    def swap(self,distance:int|float,start_dist:int,time:int):
        """Swap colors

        Args:
            distance (int | float): Current distance
            start_dist (int): Distance to start swapping (repetitive)
        Returns:
            tuple: RGB
        """
        if distance%start_dist < start_dist//2:
            if self.count < self.max:
                self.count += 1
                if time%self.rate < self.rate/2:
                    return self.colors[1]
                else:
                    return self.colors[0]
            else:
                return self.colors[0]
        else:
            self.count = 0
            return self.colors[0]

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

class DistanceMarkers:
    #! Not functional. Scaling is wrong. Will not finish.
    def __init__(self,screen:pg.Surface,font:pg.font.Font,interval:int,speed:int,ypos:int,color:tuple=(255,255,255)):
        """
        Args:
            interval (int): Interval between each marker (m)
            ypos (int): Vertical position on the screen, with the center as reference
        """
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.font = font
        self.color = color
        self.interval = interval
        self.speed = speed
        self.ypos = ypos
    
    def blit(self,distance:int):
        """
        Render the distance marker
        """
        for i in range(distance//self.interval-distance//1000,distance//self.interval-distance//1000+3):
            render_text(self.screen,
                        self.font,
                        str(i*self.interval/1e3)+"km",
                        (i*self.interval*5-distance*self.speed,self.height//2-self.ypos),
                        color=self.color,
                        rotation=-90)
            render_text(self.screen,
                        self.font,"_____",
                        (i*self.interval*5-distance*self.speed+40,self.height//2-self.ypos),
                        color=self.color,
                        rotation=-90)