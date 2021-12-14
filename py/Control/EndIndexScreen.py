#Game over surface

import pygame
from py.Screen.IndexScreen.End import EndIndexScreen
from py.Screen import IndexScreen as si

screenID = 'EndScreen';
bgpScreenID = 'PlayScreen';
bgpName = 'Space1';

def init_indexscreen(win_screen = None):                                        #Implement about surface initialization
    winrect = pygame.display.get_surface().get_rect();                          #Get the size of the surface
    
    global indexscreen;                                                         #Define indexscreen as global variable
    indexscreen = EndIndexScreen(size= winrect.size, scale_rate=1);
    
    icon_image = si.Icon_Image(name = 'Index.BG.GO');                           #Add a decorative layer
    icon_image.move_to(location = (400,120), Center = True);                    #Move the image to the specified coordinate
    indexscreen.add_images(icon_image, imageSetID='bg');
    indexscreen.showImageID += ['bg'];                                          #Set list ('bg') visible
    icon_image = si.Icon_Image(name = 'Index.BG.LyingIronblock');               #Add a decorative layer
    icon_image.move_to(location = (400,300), Center = True);                    #Move the image to the specified coordinate
    indexscreen.add_images(icon_image, imageSetID='bg');
    indexscreen.showImageID += ['bg'];                                          #Set list ('bg') visible
    icon_image = si.Icon_Image(name = 'Index.BG.PB');                           #Add a decorative layer
    icon_image.move_to(location = (400,300), Center = True);                    #Move the image to the specified coordinate
    indexscreen.add_images(icon_image, imageSetID='bg');
    indexscreen.showImageID += ['bg'];                                          #Set list ('bg') visible
    
    try:
        indexscreen.change_bgp(win_screen = win_screen, bgpScreenID = bgpScreenID); #Try to use PlayScreen surface as background
    except NameError:
        indexscreen.change_bgp(name = bgpName);                                     #IF error, use the default image as the background
    
    #<-------------------------------------------------------------------------
    #增加指令
    indexscreen.add_command(pygame.KEYDOWN, "self.return_newcID('InfoShortScreen.Reset')"); #Add a command, press any key to return to the infoshortscreen


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