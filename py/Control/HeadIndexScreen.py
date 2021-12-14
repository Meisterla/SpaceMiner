#Create the index(title) surface
#Including create and initialize function
import pygame
from py.Screen import IndexScreen as si
from py.Screen.IndexScreen import Head as sih
from py.Tools import Pre as tp
from py.Tools.Items import Planet as tip

screenID = 'IndexScreen';
bgpName = 'Space1';

def init_indexscreen():                                                         #Implement index surface initialization
    winrect = pygame.display.get_surface().get_rect();                          #Get the size of the surface
    
    global indexscreen;                                                         #Define indexscreen as global variable
    
    indexscreen = sih.HeadIndexScreen(size= winrect.size, scale_rate=1);        #Initialize the indexscreen
    
    icon_image = si.Icon_Image(name = 'Index.BG.Maintext', Command_ID = 'PlayScreen');      #Initialize background image
    icon_image.move_to(tp.add_location_tuple(winrect.midtop, (0,160)), Center = True);      #Move the image to the specified coordinate
    indexscreen.add_images(icon_image, imageSetID='bg');                        #Add the image to indexscreen
    indexscreen.showImageID += ['bg'];                                          #Tag the background visible
    
    indexscreen.images.show_id = 'icon';
    icon_image = si.Icon_Image(name = 'Index.Select.HalfStart', Command_ID = 'StoryShortScreen');     #Initialize other images(icons)
    indexscreen.add_images(icon_image, imageSetID='icon');                      #The specific designd are similar to the above
    icon_image = si.Icon_Image(name = 'Index.Select.QuickStart', Command_ID = 'PlayScreen.Reset');
    indexscreen.add_images(icon_image, imageSetID='icon');
    icon_image = si.Icon_Image(name = 'Index.Select.Config', Command_ID = 'GalleryScreen');
    indexscreen.add_images(icon_image, imageSetID='icon');
    icon_image = si.Icon_Image(name = 'Index.Select.About', Command_ID = 'AboutScreen');
    indexscreen.add_images(icon_image, imageSetID='icon');
    icon_image = si.Icon_Image(name = 'Index.Select.Quit', Command_ID = 'Quit');
    indexscreen.add_images(icon_image, imageSetID='icon');
    indexscreen.set_icon_location(ShowMode='O');                                #Set the arrangement mode of option images
    indexscreen.showImageID += ['icon'];                                        #Tag the icons visible
    
    
    indexscreen.set_indicator(indicator_name='Index.Indicator');                #Initialize the option arrow
    
    BGPItem = tip.PlanetItem(name = 'Hot', rotatespeed = -10);                  #Initialize(create) background item(hot planet)
    BGPItem.scale_to(size=(80, 80))                                             #Define the size of this item
    BGPItem.move_to((220, 300), Center = True);                                 #Move the image to the specified coordinate
    indexscreen.add_items(BGPItem, itemSetID = 'planet');                       #Add the item to the screen
    BGPItem = tip.PlanetItem(name = 'Ice', rotatespeed = -10);                  #Initialize(create) background item(ice planet)
    BGPItem.scale_to(size=(200, 200))                                           #The specific operation is the same as above
    BGPItem.move_to((120, 450), Center = True);
    indexscreen.add_items(BGPItem, itemSetID = 'planet');
    BGPItem = tip.PlanetItem(name = 'Rock', rotatespeed = -10);                 #Initialize(create) background item(rock planet)
    BGPItem.move_to(tp.add_location_tuple(winrect.midbottom, (0,300)), Center = True);      #The specific operation is the same as above
    indexscreen.add_items(BGPItem, itemSetID = 'planet');
    indexscreen.Anima2 = 'planet';                                              #Tag 'planet' as the action object of the second stage animation
    
    BGPItem = tip.PlanetItem(name = 'Index.BG.SpaceShip');                      #Initialize the background item(spaceship)
    BGPItem.scale_to(size = (200, 200));                                        #The specific operation is the same as above
    indexscreen.add_items(BGPItem, itemSetID = 'spaceship');
    indexscreen.Anima1 = 'spaceship';                                           #Tag 'spaceship' as the action object of the first stage animation
    
    indexscreen.updateItemID += ['planet', 'spaceship'];
    
    indexscreen.change_bgp(name = bgpName);                                     #Set the background

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