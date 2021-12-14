#init configuration for resources and windows
import pygame
import os
import numpy as np

GravetyConstant = 1;

W, H=800,600;                                                                   #Windows size
FPS=30;                                                                         #Fps
Path_Graph="Data\Graph";                                                        #Graph path
Path_Sound="Data\Sound"                                                         #Sound path

default_bgp = "default_Space"                                                   #Default resources' name and parameters
default_empty = "Empty"
default_Planet = "default_Planet"
default_Cloud = "default_Planet.Clouds"
default_SS = "Index.BG.SpaceShip"
default_item_id = None;
default_image_id = None;
default_select = "Index.Indicator"
default_textbox = "Index.Select.Others"
name_indicator = "INDICATOR"

#The data that give the lower and upper bound of the gaming objects (the items in the play screen's map)
#<----------------------------------------------------------------------------
item_vol_min = 5;
item_vol_max = 60;
item_mass_range = (10, 1000);
item_mass_breaks = (50, 100, 500, 800);
item_tempr_range = (1, 500);
item_tempr_breaks = (200, 300);
#<----------------------------------------------------------------------------

pygame.init();                                                                  #Init the pygame

IMAGES={};                                                                      #Load graphs
image_source=[]
for image in os.listdir(Path_Graph):
    name, extension = os.path.splitext(image);  #提取文件名，后缀(二者分离)
    if extension not in ['.png', '.jpg']:
        continue;
    image_source.append(name);                  #建立字典项
    path=os.path.join(Path_Graph, image);       #读图
    IMAGES[name]=pygame.image.load(path);       #存入字典
    
#<---------------------------------------------------->
# 加载声音资源
# pygame库中关于声音部分的官方文档链接：https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound
# 本部分主要灵感来自：https://github.com/Mio19/Pygame-Magical-Slime
#
# Load sounds
# The instruction about sound model in pygame: https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound
# Citation - inspired by: https://github.com/Mio19/Pygame-Magical-Slime

#Load sound model in pygame
pygame.mixer.init() 
if not pygame.mixer or not pygame.mixer.get_init():
    print("Warning, sound disabled")

#定义两个控制声音的类，所有与声音有关的功能都在这两个类中实现
#游戏有两种声音，一种是背景音乐，需要不断循环播放，另一种是简单的短提示音，播放一遍即可。
#Define two classes for sound playing, one for play looping BGM and another for play brief sound
#
def is_number(nu):                                                              #Define here to avoid loop loading (a same function is in .\py\Tools\Pre.py, but that .py file needs to import this file)
    return type(nu) in [int, float, np.float64];                                #Return True only when the nu is a number

class BackGroudMusic(pygame.mixer.Sound):#Loop playing BGM
    """
    Methods:
        __init__(name = "xxx.wav", volume = 10.0)
        play_music(volume = None) - Play the music - Keep the original vol if given not-number parameter
        stop_music() - Stop the music
        change_volume(volume = None) - Change vol
    """

    def __init__(self, name = "start.wav", volume = 10.0):#Note that the default volume is float type
        global Path_Sound
        fullname = os.path.join(Path_Sound, name)#Whole path of the file
        pygame.mixer.Sound.__init__(self,file = fullname)
        if is_number(volume):
            self.change_volume(volume)
        else:
            self.change_volume(10.0)

    # Use this method to play the music
    def play_music(self, volume = None):
        self.change_volume(volume)
        self.stop_music()
        pygame.mixer.Sound.play(self,loops=-1)
        # 根据pygame的官方文档，loops=-1时，声音将无限循环，直到调用self.stop_music()停止播放。
        # According to official documents, if loops is set to -1, the Sound will loop indefinitely.

    # Use this method to stop the music
    def stop_music(self):
        pygame.mixer.Sound.stop(self)

    # Use this method to change the volume
    def change_volume(self, volume = None):
        if is_number(volume):
            pygame.mixer.Sound.set_volume(self,float(volume))


class ShortMusic(pygame.mixer.Sound):#Only play once at a time
    """
    Methods:
        __init__(name = "xxx.wav", volume = 10.0)
        play_music(volume = None) - Play the music - Keep the original vol if given not-number parameter
        stop_music() - Stop the music
        change_volume(volume = None) - Change vol
    """
    def __init__(self, name = "boom.wav", volume = 10.0):
        global Path_Sound
        fullname = os.path.join(Path_Sound, name)#Whole path of the file
        pygame.mixer.Sound.__init__(self,file = fullname)
        if is_number(volume):
            self.change_volume(volume)
        else:
            self.change_volume(10.0)

    # Use this method to play the music
    def play_music(self, volume = None):
        self.change_volume(volume)
        pygame.mixer.Sound.play(self,loops=0)
        # 根据pygame的官方文档，loops=0时,声音只播放一次
        # According to official documents, if loops is set to 0, the Sound will play only once.

    # Use this method to stop the music
    def stop_music(self):
        pygame.mixer.Sound.stop(self)

    # Use this method to change the volume
    def change_volume(self, volume = None):
        if is_number(volume):
            pygame.mixer.Sound.set_volume(self,float(volume))

#Create the needed BGM and SM, use dict to store.
BGMSet, SESet = {}, {}
BGMSet['start']=BackGroudMusic(name = "start.wav")
BGMSet['8-bit-game-music']=BackGroudMusic(name = "8-bit-game-music.wav")

SESet['boom']=ShortMusic(name = "boom.wav")
SESet['se1']=ShortMusic(name = "se1.mp3")
SESet['se2']=ShortMusic(name = "se2.mp3")
SESet['se.selection']=ShortMusic(name = "se.selection.wav")
SESet['Confirm']=ShortMusic(name = "Confirm.wav")
SESet['reflect']=ShortMusic(name = "reflect.wav")
SESet['collect.packet']=ShortMusic(name = "collect.packet.wav")
SESet['collect.gold']=ShortMusic(name = "collect.gold.wav")
SESet['touch.gold']=ShortMusic(name = "touch.gold.wav")
SESet['launch']=ShortMusic(name = "launch.wav")
SESet['spawn.packet']=ShortMusic(name = "spawn.packet.wav")

#<------------------------------------------------------------------------------------------------->

#SCREEN=pygame.display.set_mode(size = (W,H), flags = pygame.RESIZABLE);          #Create a pygame windows, with flags = pygame.RESIZABLE
SCREEN=pygame.display.set_mode(size = (W,H));                                   #Create a pygame windows
pygame.display.set_caption("Space Miner");                                      #Window's name
pygame.display.set_icon(IMAGES["Icon"]);                                        #Window's icon
CLOCK=pygame.time.Clock();                                                      #Set a clock