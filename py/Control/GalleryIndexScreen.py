#The screen fo 'About us'
import pygame
import py.Tools.Items as tit
from py.Screen import IndexScreen as si
from py.Screen.IndexScreen import Difficulty as sid

screenID = 'GalleryScreen';
bgpName = 'Space2';

def init_indexscreen():                                                         #Implement pause surface initialization
    winrect = pygame.display.get_surface().get_rect();                          #Get the size of the surface
    
    global indexscreen;                                                         #Define indexscreen as global variable
    
    indexscreen = sid.DiffIndexScreen(size= winrect.size, scale_rate=1);        #Initialize the indexscreen
    
    icon_image = si.Icon_Image(name = 'Index.Select.Others', AdditionInfo = ('Index.Info.Story1',));     #Create option image, AdditionInfo is the show image
    icon_image.move_to((120,570),Center = True);                                                         #Move the image to location
    indexscreen.add_images(icon_image, imageSetID='icon');                                               #Add image
    icon_image = si.Icon_Image(name = 'Index.Select.Others', AdditionInfo = ('Index.Info.Story2',));     #Create option image, AdditionInfo is the show image
    icon_image.move_to((212,480),Center = True);                                                         #Move the image to location
    indexscreen.add_images(icon_image, imageSetID='icon');                                               #Add image
    icon_image = si.Icon_Image(name = 'Index.Select.Others', AdditionInfo = ('Index.Info.Operation',));  #Create option image, AdditionInfo is the show image
    icon_image.move_to((344,450),Center = True);                                                         #Move the image to location
    indexscreen.add_images(icon_image, imageSetID='icon');                                               #Add image
    icon_image = si.Icon_Image(name = 'Index.Select.Others',  AdditionInfo = ('Index.Info.Iteminfo1',)); #Create option image, AdditionInfo is the show image
    icon_image.move_to((456,450),Center = True);                                                         #Move the image to location
    indexscreen.add_images(icon_image, imageSetID='icon');                                               #Add image
    icon_image = si.Icon_Image(name = 'Index.Select.Others',  AdditionInfo = ('Index.Info.Iteminfo2',)); #Create option image, AdditionInfo is the show image
    icon_image.move_to((588,480),Center = True);                                                         #Move the image to location
    indexscreen.add_images(icon_image, imageSetID='icon');                                               #Add image
    
    icon_image = si.Icon_Image(name = 'Index.Select.Back', Command_ID = 'IndexScreen',  AdditionInfo = ('CargoSS.Details',));       #Create option image, AdditionInfo is the show image
    icon_image.move_to((680,570),Center = True);                                                                                    #Move the image to location
    indexscreen.add_images(icon_image, imageSetID='icon');                                                                          #Add image
    
    indexscreen.showImageID += ['icon'];                                        #Set the list('icon') visible
    
    BGPItem = tit.PlanetItem(name = 'Empty');
    BGPItem.scale_to(size = (400, 400));
    BGPItem.move_to((400, 200), Center = True);
    indexscreen.add_items(BGPItem, itemSetID = 'bg.icon');
    indexscreen.bgItemID_icon = 'bg.icon';
    
    indexscreen.showItemID += ['bg', 'bg.indicator', 'bg.icon', 'bg.door'];                             #Set the items need to show
    indexscreen.updateItemID += ['bg', 'bg.indicator', 'bg.icon', 'bg.door'];                           #Set of items to be update
    
    indexscreen.set_indicator(indicator_name='Index.Indicator');                                        #Initialize the option arrow
    
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