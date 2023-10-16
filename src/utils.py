import os 
import pygame as pg 

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
    for flag in flags:
        globals()[flag] = import_flag(flag)
    flag_rma = scale_flag(flag_rma, 105)
    flag_x = scale_flag(flag_x, 105)
    flag_be = flip_flag(flag_be, 40)
    flag_fr = flip_flag(flag_fr, 40)
    return [flag_be, flag_fr, flag_x, flag_rma]