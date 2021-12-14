#Information display surface

import pygame
import py.Screen.ShortScreen as ss

screenID = 'StoryShortScreen';
bgpName = 'Space3';

def init_indexscreen(win_screen = None):                                        #Implement StoryShort surface initialization
    winrect = pygame.display.get_surface().get_rect();                          #Get the size of the surface
    
    global indexscreen;                                                         #Define indexscreen as global variable
    indexscreen = ss.ShortScreen(nextScreenID = 'DifficultyScreen.Reset', intervaltime = 1, size= winrect.size, scale_rate=1);      #Initialize the indexscreen
    
    indexscreen.graphlist = ['Index.Info.Story1', 'Index.Info.Story1', 'Index.Info.Story2', 'Index.Info.Story2', 'Empty'];          #Set the list of stories
    indexscreen.graphitem.scale_to(size=(600,600));                                                                                 #Set the size of graphitem
    indexscreen.graphitem.move_to((400,250), Center=True)                                                                           #Move the item to location
    
    indexscreen.change_bgp(name = bgpName);                                     #Set the background


def return_screen(win_screen, Reset = False):                                   #Surface ouput function
    if Reset:                                                                   #Automatic initialization indexscreen
        init_indexscreen(win_screen);                                           #Parameter Reset controls whether to force initialization
    else:
        try:
            indexscreen
        except NameError:
            init_indexscreen(win_screen);
        
    try:
        win_screen.add_screens(indexscreen, screen_id = screenID);              #Put indexscreen into win_screen(Screen_Basic.WinScreen)
    except AttributeError:
        pass;