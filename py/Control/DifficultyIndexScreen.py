#Difficulty selection screen
import pygame
import numpy as np
import py.Tools.Images as ti
import py.Tools.Items as tit
from py.Screen import IndexScreen as si
from py.Screen.IndexScreen import Difficulty as sid

screenID = 'DifficultyScreen';
bgpName = 'Space1';

def init_indexscreen():                                                         #Implement difficulty selection surface initialization
    winrect = pygame.display.get_surface().get_rect();
    
    global indexscreen;
    
    indexscreen = sid.DiffIndexScreen(size= winrect.size, scale_rate=1);
    
    icon_image = si.Icon_Image(name = 'Index.Select.Easy', Command_ID = 'PlayScreen.Easy.Reset', AdditionInfo = ('YellowRock', (340,266)));     #Create option image, parameter
    indexscreen.add_images(icon_image, imageSetID='icon');                                                                                      #AdditionInfo include the information of pictures on display and the location of the door
    icon_image = si.Icon_Image(name = 'Index.Select.Normal', Command_ID = 'PlayScreen.Normal.Reset', AdditionInfo = ('Rock', (280,232)));       #Create option (item)image
    indexscreen.add_images(icon_image, imageSetID='icon');
    icon_image = si.Icon_Image(name = 'Index.Select.Hard', Command_ID = 'PlayScreen.Hard.Reset', AdditionInfo = ('Rock.Ruins', (220,198)));     #Create option (item)image
    indexscreen.add_images(icon_image, imageSetID='icon');
    icon_image = si.Icon_Image(name = 'Index.Select.Endless', Command_ID = 'PlayScreen.Endless.Reset',  AdditionInfo = ('HotRock',(160,166)));  #Create option (item)image
    indexscreen.add_images(icon_image, imageSetID='icon');
    indexscreen.set_icon_location(ShowMode='O', anglerange = (-np.pi * 36/180, -np.pi * 144/180), radius = 260);                                #Set the arrangement mode of option images
    
    icon_image = si.Icon_Image(name = 'Index.Select.Back', Command_ID = 'IndexScreen',  AdditionInfo = ('Index.BG.SpaceShip',(400,300)));       #Create option (item)image
    icon_image.move_to((638,438),Center = True);
    indexscreen.add_images(icon_image, imageSetID='icon');
    
    indexscreen.showImageID += ['icon'];                                        #Tag the icons visible
    
    IconImage = ti.InteractImage('PlayScreen.BG.Room');                         #Initialize an image
    indexscreen.add_images(IconImage, imageSetID='bg');                         #Add the image to indexscreen
    indexscreen.showImageID += ['bg'];                                          #Tag the background visible
    
    BGPItem = tit.PlanetItem(name = 'Index.BG.Arrow');                          #Initialize an image(planet item)
    indexscreen.add_items(BGPItem, itemSetID = 'bg.indicator');                 #Add the image to indexscreen
    indexscreen.bgItemID_PI = 'bg.indicator';
    
    BGPItem = tit.PlanetItem(name = 'Index.BG.Door.Left');                      #Initialize an image as door(planet item)
    indexscreen.add_items(BGPItem, itemSetID = 'bg.door');
    indexscreen.bgItemID_door = 'bg.door'
    
    BGPItem = tit.PlanetItem(name = 'Index.BG.Door.Right');                     #Initialize an image as door(planet item)
    indexscreen.add_items(BGPItem, itemSetID = 'bg');
    
    BGPItem = tit.PlanetItem('Thor');                                           #Create the images of Thor and Isaac as the background in the same way as above
    BGPItem.scale_to(size=(100,100));
    BGPItem.move_to((300,250),Center=True)
    BGPItem.update_rotate(angle=20)                                             #Set the angle of rotation
    indexscreen.add_items(BGPItem, itemSetID = 'bg');
    BGPItem = tit.PlanetItem('Isaac');
    BGPItem.scale_to(size=(100,100));
    BGPItem.move_to((250,300),Center=True)
    BGPItem.update_rotate(angle=-10)                                            #Set the angle of rotation
    indexscreen.add_items(BGPItem, itemSetID = 'bg');
    
    BGPItem = tit.PlanetItem(name = 'Empty');                                   #Initialize an enpty image
    BGPItem.scale_to(size = (100, 100));
    BGPItem.move_to((540, 300), Center = True);
    indexscreen.add_items(BGPItem, itemSetID = 'bg.icon');
    indexscreen.bgItemID_icon = 'bg.icon';
    
    indexscreen.showItemID += ['bg', 'bg.indicator', 'bg.icon', 'bg.door'];     #Set the items need to show
    indexscreen.updateItemID += ['bg', 'bg.indicator', 'bg.icon', 'bg.door'];   #Set of items to be update
    
    indexscreen.set_indicator(indicator_name='Index.Indicator2');               #Initialize the option arrow
    
    indexscreen.change_bgp(name = bgpName);                                     #Set the background

    indexscreen.add_command((pygame.KEYUP, pygame.K_ESCAPE), "self.return_newcID('IndexScreen')"); #Add a command, press esc to switch to the indexscreen
    indexscreen.add_command('BGM', "self.reset_bgm()")

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