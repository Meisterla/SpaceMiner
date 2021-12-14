# Modified IndexScreen for Control.HeadIndexScreen
import pygame
from Config_Resource import FPS, BGMSet
from py.Screen.IndexScreen import Basic as sib
import py.Tools.Pre as tp

subFPS = 30;
animaFPS = 20;
MaxFPSCounter = FPS // subFPS;
bgmname = 'start';

class HeadIndexScreen(sib.IndexScreen):
    """
    Data:
        (sib.IndexScreen)
        images - Icon_Set
        indicator - InteractImage (with command set)
        StepCounter
        FPSCounter
        tempcounter
        Anima1_originaldata
        Anima2_originaldata
        Anima1_tempdata
        Anima2_tempdata
    Methods:
        (sib.IndexScreen)
        __init__
        restart
        update
    """
    Anima1 = None;
    Anima2 = None;
    def __init__(self, size = None, center = None, rect = None, scale_rate = None, scale_center = None):
        sib.IndexScreen.__init__(self, size = size, center = center, rect = rect, scale_rate = scale_rate, scale_center = scale_center);
        self.restart();
        self.StepCounter = -1;
        self.FPSCounter = -1;
        self.tempcounter = 0;
        self.Anima1_originaldata = {};
        self.Anima2_originaldata = {};
        self.Anima1_tempdata = {};
        self.Anima2_tempdata = {};
        
    def restart(self):
        sib.IndexScreen.restart(self);
        try:
            self.showItemID.remove(self.Anima1);
        except ValueError:  pass;
        try:
            self.showItemID.remove(self.Anima2);
        except ValueError:  pass;
        
        # Reset BGM
        for bgm in BGMSet:
            BGMSet[bgm].stop_music();
        BGMSet[bgmname].play_music();
        
        # Reset animations' parameters
        self.StepCounter = -1;
        self.FPSCounter = -1;
        self.tempcounter = 0;
        self.Anima1_originaldata = {};
        self.Anima2_originaldata = {};
        self.Anima1_tempdata = {};
        self.Anima2_tempdata = {};
    
    def update(self, UpSize = False, size = None, center = None, rect = None, UpItems = False, item_ids = None):
        # 新增两段item的开场动画, 动画逻辑采用硬编码, 两段动画的作用item集合ID分别为Anima1, Anima2
        # Add two new opening animations of 'item'. The animations' logic is hard coded. The IDs of two animations item Sets are 'Anima1' and 'Anima2'.
        sib.IndexScreen.update(self, UpSize = UpSize, size = size, center = center, rect = rect, UpItems = UpItems, item_ids = item_ids);
        if self.StepCounter >= 5:                                               #播放完成后解锁空格与回车操作 |  After playing unlock the space and enter operations.
            self.remove_command(pygame.K_SPACE);
            self.remove_command(pygame.K_RETURN);
            return;
        
        if self.StepCounter == -1:
            self.StepCounter = 0;
            try: 
                for item in self.items.indexes[self.Anima1]:
                    self.Anima1_originaldata[item] = self.items.indexes[self.Anima1][item].moveimage.rect.size;
            except KeyError:    self.StepCounter = 3;
            try:
                for item in self.items.indexes[self.Anima2]:
                    self.Anima2_originaldata[item] = self.items.indexes[self.Anima2][item].moveimage.rect.center;
            except KeyError:    self.StepCounter = 5;
        
        if self.StepCounter == 0:
            self.StepCounter = 1;
            for item in self.items.indexes[self.Anima1]:
                self.items.indexes[self.Anima1][item].scale_to(rate = 1/animaFPS);
                self.Anima1_tempdata[item] = self.items.indexes[self.Anima1][item].moveimage.rect.size;
            for item in self.items.indexes[self.Anima2]:
                self.Anima2_tempdata[item] = (self.draw_rect.h - self.items.indexes[self.Anima2][item].moveimage.rect.y);
                self.items.indexes[self.Anima2][item].add_speed(location = (0, self.draw_rect.h - self.items.indexes[self.Anima2][item].moveimage.rect.y));
            self.showItemID += [self.Anima1, self.Anima2];
        self.add_command(pygame.K_SPACE,'None');                                # 开始播放动画时锁住空格与回车操作 | While starting playing lock the space and enter operations.
        self.add_command(pygame.K_RETURN,'None');
        
        if self.StepCounter == 1:
            self.FPSCounter += 1;
            if self.FPSCounter == MaxFPSCounter:
                self.FPSCounter = 0;
                self.tempcounter += 1;
                
                for item in self.items.indexes[self.Anima1]:
                    self.items.indexes[self.Anima1][item].scale_to(size = tp.dot_tuple(self.Anima1_tempdata[item], self.tempcounter));
                    self.items.indexes[self.Anima1][item].update_image();
                    if self.items.indexes[self.Anima1][item].moveimage.rect.size[0] > self.Anima1_originaldata[item][0]:
                        self.StepCounter = 2;
        
        if self.StepCounter == 2:
            self.FPSCounter = -1;
            self.tempcounter = 0;
            for item in self.items.indexes[self.Anima1]:
                self.items.indexes[self.Anima1][item].scale_to(size = self.Anima1_originaldata[item]);
                self.items.indexes[self.Anima1][item].update_image();
            self.StepCounter = 3;
        
        if self.StepCounter == 3:
            self.FPSCounter += 1;
            if self.FPSCounter == MaxFPSCounter:
                self.FPSCounter = 0;
                self.tempcounter += 1;
                
                for item in self.items.indexes[self.Anima2]:
                    self.items.indexes[self.Anima2][item].move_to(location = (tp.add_location_tuple(self.Anima2_originaldata[item], (0, self.Anima2_tempdata[item] * (1-self.tempcounter/animaFPS)))), Center = True);
                    if tp.distance_location_tuple(self.items.indexes[self.Anima2][item].moveimage.rect.center, self.Anima2_originaldata[item]) < 1:
                        self.StepCounter = 4;
        
        if self.StepCounter == 4:
            self.FPSCounter = -1;
            self.tempcounter = 0;
            for item in self.items.indexes[self.Anima2]:
                self.items.indexes[self.Anima2][item].move_to(location = self.Anima2_tempdata[item], Center = True);
            self.StepCounter = 5;
                