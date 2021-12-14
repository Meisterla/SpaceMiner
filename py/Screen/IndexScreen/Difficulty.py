# Modified IndexScreen for Control.DifficultyIndexScreen( and additional AboutIndexScreen and GuideIndexScreen)
import numpy as np
import py.Tools.Pre as tp
from py.Screen.IndexScreen import Basic as sib
from Config_Resource import BGMSet

bgmname = 'start';

class DiffIndexScreen(sib.IndexScreen):
    """
    Data:
        (sib.IndexScreen)
        images - Icon_Set
        indicator - InteractImage (with command set)

    Methods:
        (sib.IndexScreen)
        __init__
        reset_bgm
        restart
        update
    """
    bgItemID_PI = None;                                                         # The ID of the decorated item, pointing to the indicator, not automatically updated, but will change the rotation angle to point to the indicator.
    bgItemID_icon = None;                                                       # The ID of the information icon, its image will change as the indicator moves and the selection switchs
    bgItemID_door = None;                                                       # The ID of the movable door, will chang position as the indicator moves
    
    def __init__(self, size = None, center = None, rect = None, scale_rate = None, scale_center = None):
        sib.IndexScreen.__init__(self, size = size, center = center, rect = rect, scale_rate = scale_rate, scale_center = scale_center);
    
    def reset_bgm(self):
        # 重设BGM  |  Reset BGM
        for bgm in BGMSet:
            BGMSet[bgm].stop_music();
        BGMSet[bgmname].play_music();
    
    def restart(self):
        sib.IndexScreen.restart(self);
        
        # Reset the decorated item, information icon and movable door
        try:
            for item in self.items.indexes[self.bgItemID_PI]:
                self.items.indexes[self.bgItemID_PI][item].update_rotate(angle = 0);
                self.items.indexes[self.bgItemID_PI][item].update();
        except KeyError:    pass;
        
        try:
            for item in self.items.indexes[self.bgItemID_door]:
                self.items.indexes[self.bgItemID_door][item].move_to((400, 300), Center = True);
                self.items.indexes[self.bgItemID_PI][item].update();
        except KeyError:    pass;
        
        try:
            for item in self.items.indexes[self.bgItemID_icon]:
                self.items.indexes[self.bgItemID_icon][item].update_image('Empty');
                self.items.indexes[self.bgItemID_icon][item].update();
        except KeyError:    pass;
    
    def update(self, UpSize = False, size = None, center = None, rect = None, UpItems = False, item_ids = None):
        sib.IndexScreen.update(self, UpSize = UpSize, size = size, center = center, rect = rect, UpItems = UpItems, item_ids = item_ids);
        
        # Update the decorated item, information icon and movable door
        try:
            if self.indicator.select_index == None:     {}[1];
            for item in self.items.indexes[self.bgItemID_PI]:
                x, y = tp.minus_location_tuple(self.indicator.center, self.items.indexes[self.bgItemID_PI][item].moveimage.center);
                angle = (np.arcsin(-x/np.sqrt(x**2 + y**2)), np.arccos(-y/np.sqrt(x**2 + y**2)));
                angle = angle[0] if abs(angle[0]) >= abs(angle[1]) else angle[1];
                self.items.indexes[self.bgItemID_PI][item].update_rotate(angle = angle * 180/np.pi);
                self.items.indexes[self.bgItemID_PI][item].update();
        except KeyError:    pass;
        
        try:
            self.indicator.select_icon.AddInfo;
            for item in self.items.indexes[self.bgItemID_door]:
                try:
                    self.items.indexes[self.bgItemID_door][item].move_to(self.indicator.select_icon.AddInfo[1], Center = True);
                    self.items.indexes[self.bgItemID_door][item].update();
                except AttributeError: self.items.indexes[self.bgItemID_door][item].move_to((400, 300), Center = True);
        except AttributeError:  pass;
        except KeyError:    pass;
        
        try:
            self.indicator.select_icon.AddInfo;
            for item in self.items.indexes[self.bgItemID_icon]:
                try:
                    self.items.indexes[self.bgItemID_icon][item].update_image(self.indicator.select_icon.AddInfo[0]);
                    self.items.indexes[self.bgItemID_icon][item].update();
                except AttributeError:  self.items.indexes[self.bgItemID_icon][item].update_image('Empty');
        except AttributeError:  pass;
        except KeyError:    pass;