#PlayScreen
import pygame
import py.Tools.Images.General as tig
import py.Tools.Items.General as tige
import py.Screen as scr
import py.Screen.PlayScreen as sp

screenID = 'PlayScreen';
bgpName = 'Space1';

def init_playscreen():                                                          #Implement basic surface initialization
    global playscreen;                                                          #Define playscreen as global variable
    
    playscreen = sp.PlayScreen();                                               ##Initialize the playscreen
    
    IconImage = tig.InteractImage('PlayScreen.BG.Room');                        #Add background image
    playscreen.add_images(IconImage, imageSetID='bg');                          #Add the image to playscreen
    IconImage = tig.InteractImage('PlayScreen.BG.Interface');                   #Add background image
    IconImage.scale_to(size = (100,100));                                       #Set scale of size
    IconImage.move_to((63,290),Center=True);                                    #Move the image to the specified coordinate
    playscreen.add_images(IconImage, imageSetID='bg');
    IconImage = tig.InteractImage('PlayScreen.BG.LongInterface');
    IconImage.scale_to(rate = 0.4);
    IconImage.move_to((740,340),Center=True);
    playscreen.add_images(IconImage, imageSetID='bg');
    IconImage = tig.InteractImage('PlayScreen.BG.Text.Score');
    IconImage.move_to((665,540),Center=True);
    playscreen.add_images(IconImage, imageSetID='bg');
    IconImage = tig.InteractImage('PlayScreen.BG.Text.Time');
    IconImage.scale_to(rate=0.6);
    IconImage.move_to((745,270),Center=True);
    playscreen.add_images(IconImage, imageSetID='bg');
    IconImage = tig.InteractImage('PlayScreen.BG.Text.Health');
    IconImage.scale_to(rate=0.5);
    IconImage.move_to((745,360),Center=True);
    playscreen.add_images(IconImage, imageSetID='bg');
    
    playscreen.showImageID += ['bg'];                                           #Tag the background visible
    
    BGPItem = tige.GeneralItem('PlayScreen.BG.Railway', Movetypes = 'RD');      #Create line of sight
    #BGPItem.move_to(playscreen.camera_rect.center, Center = True);
    playscreen.add_items(BGPItem, itemSetID = playscreen.bgItemID_SAI);         #Create an item list,itema have same angel with Indicator
    
    playscreen.items.show_id = playscreen.mainItemID;
    playscreen.change_bgp(name = bgpName);                                      #Set the background
    
    #<-------------------------------------------------------------------------
    #增加指令
    playscreen.add_command((pygame.KEYUP, pygame.K_ESCAPE), "self.return_newcID('PauseScreen.Reset')");     #Add a command, press esc to switch to the pausescreen



def return_screen(win_screen, Reset = False):                                   #Surface ouput function
    if Reset:                                                                   #Automatic initialization indexscreen
        init_playscreen();                                                      #Parameter Reset controls whether to force initialization
    else:
        try:
            playscreen;
        except NameError:
            init_playscreen();
        
    try:
        win_screen.add_screens(playscreen, screen_id = screenID);               #Put indexscreen into win_screen(Screen_Basic.WinScreen)
    except AttributeError:
        pass;