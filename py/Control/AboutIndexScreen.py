#The screen fo 'About us'
import pygame
import numpy as np
import py.Tools.Images as ti
import py.Tools.Items as tit
from py.Screen import IndexScreen as si
from py.Screen.IndexScreen import Difficulty as sid

screenID = 'AboutScreen';
bgpName = 'Space1';

def init_indexscreen():                                                         #Implement about surface initialization
    winrect = pygame.display.get_surface().get_rect();                          #Get the size of the surface
    
    global indexscreen;                                                         #Define indexscreen as global variable
    
    indexscreen = sid.DiffIndexScreen(size= winrect.size, scale_rate=1);        #Initialize the indexscreen
    
    icon_image = si.Icon_Image(name = 'Index.Select.Name.HZ', AdditionInfo = ('Index.Info.SignGraph.HZ',));     #Create option image, parameter
    indexscreen.add_images(icon_image, imageSetID='icon');                                                      #AdditionInfo include the information of pictures on display
    icon_image = si.Icon_Image(name = 'Index.Select.Name.CJ', AdditionInfo = ('Index.Info.SignGraph.CJ',));     #Create option image
    indexscreen.add_images(icon_image, imageSetID='icon');
    icon_image = si.Icon_Image(name = 'Index.Select.Name.LQ', AdditionInfo = ('Index.Info.SignGraph.LQ',));     #Create option image
    indexscreen.add_images(icon_image, imageSetID='icon');
    icon_image = si.Icon_Image(name = 'Index.Select.Name.HB',  AdditionInfo = ('Index.Info.SignGraph.HB',));    #Create option image
    indexscreen.add_images(icon_image, imageSetID='icon');
    icon_image = si.Icon_Image(name = 'Index.Select.Name.QS',  AdditionInfo = ('Index.Info.SignGraph.QS',));    #Create option image
    indexscreen.add_images(icon_image, imageSetID='icon');
    indexscreen.set_icon_location(ShowMode='O', anglerange = (0, -np.pi * 144/180), radius = 260);              #Set the arrangement mode of option images,Arrange the icons according to the size of the interface,
                                                                                                                #The number of icons to be displayed and the rules of the input display mode
    icon_image = si.Icon_Image(name = 'Index.Select.Back', Command_ID = 'IndexScreen',  AdditionInfo = ('CargoSS.Details',));       #Add an image
    icon_image.move_to((638,438),Center = True);
    indexscreen.add_images(icon_image, imageSetID='icon');
    
    indexscreen.showImageID += ['icon'];                                        #Tag the icons visible
    
    IconImage = ti.InteractImage('PlayScreen.BG.Room');                         #Create background
    indexscreen.add_images(IconImage, imageSetID='bg');
    IconImage = ti.InteractImage('Index.BG.Groupname');
    IconImage.move_to((650, 150), Center=True);
    indexscreen.add_images(IconImage, imageSetID='bg');
    indexscreen.showImageID += ['bg'];                                          #Tag the background visible
    
    BGPItem = tit.PlanetItem(name = 'Empty');
    BGPItem.scale_to(size = (300, 300));
    BGPItem.move_to((400, 300), Center = True);
    indexscreen.add_items(BGPItem, itemSetID = 'bg.icon');
    indexscreen.bgItemID_icon = 'bg.icon';
    
    indexscreen.showItemID += ['bg', 'bg.indicator', 'bg.icon', 'bg.door'];
    indexscreen.updateItemID += ['bg', 'bg.indicator', 'bg.icon', 'bg.door'];
    
    indexscreen.set_indicator(indicator_name='Index.Indicator2');                #Initialize the option arrow
    
    indexscreen.change_bgp(name = bgpName);                                      #Set the background
    
    #<-------------------------------------------------------------------------
    #增加指令
    indexscreen.add_command((pygame.KEYUP, pygame.K_ESCAPE), "self.return_newcID('IndexScreen')"); #Add a command, press esc to switch to the indexscreen

def return_screen(win_screen, Reset = False):                                   #Surface ouput function
    if Reset:                                                                   #Automatic initialization indexscreen
        init_indexscreen();                                                     #Parameter Reset controls whether to force initialization
    else:
        try:
            indexscreen
        except NameError:
            init_indexscreen();
        
    try:
        win_screen.add_screens(indexscreen, screen_id = screenID);              #Put indexscreen into win_screen(Screen_Basic.WinScreen)
    except AttributeError:
        pass;