import os 
import pygame as pg 
import time
from pyrow import pyrow as pr 

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

def get_distance():
    return

def get_data_streams():
    devices = list(pr.find())
    print(f"Found {len(devices)} erg(s)") #Debugging statement
    ergs = [pr.PyErg(device) for device in devices]
    return ergs

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
