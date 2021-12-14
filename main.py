#test displaying
import pygame

import Config_Resource as cr                                                    #Import game resources, including graphs, sounds, and some parameters
import py.Screen as sb                                                          #Import .\py\Screen\Basic.py

#Import all the files in .\py\Control
#Each file generates the spawnning of a Screen
from py.Control import HeadIndexScreen as ch
from py.Control import DifficultyIndexScreen as cd
from py.Control import PauseIndexScreen as cp
from py.Control import EndIndexScreen as ce
from py.Control import AboutIndexScreen as ca
from py.Control import GalleryIndexScreen as cg

from py.Control import BasicPlayScreen as cb

from py.Control import StoryShortScreen as css
from py.Control import GuideShortScreen as cgs
from py.Control import InfoShortScreen as cis

#Get graphs, and original pygame screen
IMAGES=cr.IMAGES;
SCREEN=cr.SCREEN;
w_SCREEN=pygame.display.get_surface();

def showplanet():                                                               #Loop, run cr.FPS times in a second
    while True:                                                                 #The Main Loop, generating the pygame.event operation and the basic updating and showing actions in each frams
        #Detect the events and translate them into different commands
        for event in pygame.event.get([pygame.QUIT,pygame.KEYDOWN,pygame.KEYUP,pygame.VIDEORESIZE,pygame.USEREVENT]):
            if event.type == pygame.QUIT:                                       #Quit the game
                pygame.quit();
            if event.type == pygame.KEYDOWN:                                    #Detect the keydown action
                win_screen.get_command(pygame.KEYDOWN);                         #Give the command with command key: pygame.KEYDOWN
                win_screen.get_command(event.key);                              #Give the command with command key: event.key
                win_screen.get_command((pygame.KEYDOWN, event.key));            #Give the command with command key: (pygame.KEYDOWN, event.key)
            if event.type == pygame.KEYUP:                                      #Detect the keyup action
                win_screen.get_command((pygame.KEYUP, event.key));              #key: (pygame.KEYUP, event.key)
            #if event.type == pygame.VIDEORESIZE:                                #Detect the changing size action (not needed for now)
                #win_screen.update(UpSize=True);
            if event.type == pygame.USEREVENT:                                  #Detect the event created by the program itself
                if event.name == 'win_screen_command':                          #Identify the event information
                    win_screen.get_command(event.value);
                    #win_screen.update(UpSize=True);                             #Update the Screen's size (not needed for now)
                if event.name == 'default_command':                             
                    win_screen.get_command(event.value);
        
        win_screen.update(UpItems=True);                                        #Update the main surface (and all of the marked containnings)
        win_screen.show();                                                      #Show the main surface
        
        pygame.display.update();                                                #Update pygame program
        cr.CLOCK.tick(cr.FPS);                                                  #Wait until the next fram
        #<----------------------------

if __name__ == "__main__":

    winrect=pygame.display.get_surface().get_rect();                            #创建窗口 Create The main surface (The structure that generate the index screen and play screen)
    win_screen = sb.WinScreen(show_id = 'GuideShortScreen');                    #Set the main surface to show the guide short screen (ID: 'GuideShortScreen')
    
    win_screen.add_command('Quit', 'pygame.quit()');                            #Add the 'Quit' command
    #|The program uses str to give command to each Screens, and any other Indicator class
    #|The command is basicly stored by a dict structure in Indicator class(.\py\Tools\Indicator.py),associated with a key and a value of str type.
    #|In order to call a command, user should import the Indicator class and give the key of this command, after a key is successfully given, the Indicator will puts the value into eval() function and exercutes it.
    #|More explaination of concept command and class Indicator is written in .\py\Tools\Indicator.py
    
    #<------
    
    #<------Initialize all the Screens
    ch.return_screen(win_screen);                                               #生成标题界面 Create The Head Index Screen
    ca.return_screen(win_screen);                                               #生成关于界面 Create The About Index Screen
    cd.return_screen(win_screen);                                               #生成关卡界面 Create The Difficulty Index Screen
    cb.return_screen(win_screen);                                               #生成游戏界面 Create The Play Screen
    cp.return_screen(win_screen);                                               #生成暂停界面 Create The Pause Index Screen
    ce.return_screen(win_screen);                                               #生成结束界面 Create The End Index Screen
    cg.return_screen(win_screen);                                               #生成导览界面 Create The Guide Index Screen
    #<------
    #生成过渡界面 Create The Short PPT Screen
    css.return_screen(win_screen);
    cgs.return_screen(win_screen);
    cis.return_screen(win_screen);
    
    win_screen.get_command(command_key = 'GuideShortScreen')                     #Switch to the guide short screen (ID: 'GuideShortScreen') - not needed but to ensure the setting is correct.
    
    showplanet();                                                               #Go to the message loop