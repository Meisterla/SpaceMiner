#Pause surface
import pygame
from py.Screen import IndexScreen as si

screenID = 'PauseScreen';
bgpScreenID = 'PlayScreen';
bgpName = 'Space1';

def init_indexscreen(win_screen = None):                                        #Implement pause surface initialization
    winrect = pygame.display.get_surface().get_rect();                          #Get the size of the surface
    
    global indexscreen;                                                         #Define indexscreen as global variable
    indexscreen = si.IndexScreen(size= winrect.size, scale_rate=1);             #Initialize the indexscreen
    
    icon_image = si.Icon_Image(name = 'Index.Select.HalfContinue', Command_ID = 'PlayScreen');              #Create option image
    indexscreen.add_images(icon_image, imageSetID='icon');                                                  #Add image
    icon_image = si.Icon_Image(name = 'Index.Select.HalfLevel', Command_ID = 'DifficultyScreen.BGM');       #Create option image
    indexscreen.add_images(icon_image, imageSetID='icon');                                                  #Add image
    icon_image = si.Icon_Image(name = 'Index.Select.HalfRestart', Command_ID = 'PlayScreen.Reset');         #Create option image
    indexscreen.add_images(icon_image, imageSetID='icon');                                                  #Add image
    icon_image = si.Icon_Image(name = 'Index.Select.HalfBack', Command_ID = 'IndexScreen.Reset');           #Create option image
    indexscreen.add_images(icon_image, imageSetID='icon');                                                  #Add image
    indexscreen.set_icon_location(ShowMode='|');                                #Set the arrangement mode of option images
    indexscreen.showImageID += ['icon'];                                        #Tag the icons visible
    
    
    indexscreen.set_indicator(indicator_name='Index.Indicator');                #Initialize the option arrow
    
    
    icon_image = si.Icon_Image(name = 'Index.BG.Ironblock');                    #Add background image
    icon_image.move_to(location = winrect.center, Center = True);
    indexscreen.add_images(icon_image, imageSetID='bg');
    indexscreen.showImageID += ['bg'];                                          #Tag the background visible
    
    
    try:
        indexscreen.change_bgp(win_screen = win_screen, bgpScreenID = bgpScreenID); #Try yo use the surface of bgpScreenID in win_screen as the background
    except NameError:
        indexscreen.change_bgp(name = bgpName);                                     #IF error, use the default image as the background
    
    #<-------------------------------------------------------------------------
    #增加指令
    indexscreen.add_command((pygame.KEYUP, pygame.K_ESCAPE), "self.return_newcID('PlayScreen')"); #Add a command, press esc to switch to the playscreen

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