# Modified IndexScreen for Control.ShortIndexScreen
# Automatically play the given graphs.
import pygame
from Config_Resource import FPS, default_empty
import py.Screen as ps
import py.Tools.Items as ti

class ShortScreen(ps.SubScreen):
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
    
    graphlist = [];                                                             # Iterable, store the graph name for PPT playing
    StepCounter = -1;
    FPSCounter = -1;
    tempcounter = 0;
    
    def __init__(self, nextScreenID, intervaltime, initgraph = default_empty, size = None, center = None, rect = None, scale_rate = None, scale_center = None):
        ps.SubScreen.__init__(self, size = size, center = center, rect = rect, scale_rate = scale_rate, scale_center = scale_center);
        self.nextScreen = nextScreenID;
        self.initgraph =initgraph;
        self.intervaltime = intervaltime;                                       # The pause time in each playing graph
        self.restart();
        
        # <---------------------------------------------------------------------
        # Indicator类:增加重设指令 | class Indicator: Add a reset command
        self.add_command('Reset', 'self.restart()');
        
    def restart(self):
        # Reset animations' parameters
        self.StepCounter = -1;
        self.FPSCounter = -1;
        self.MaxFPSCounter = int(FPS * self.intervaltime);
        self.tempcounter = 0;
        
        try:
            size = self.graphitem.moveimage.rect.size;
        except AttributeError:      size = None;
        self.graphitem = ti.GeneralItem(name=self.initgraph);
        self.graphitem.scale_to(size = size);
    
    def update(self, UpSize = False, size = None, center = None, rect = None, UpItems = False, item_ids = None):
        # 引入过渡动画, 播放完毕后自动进入下一界面
        # Using transition animations, which automatically move to the next screen after playback.
        ps.SubScreen.update(self, UpSize = UpSize, size = size, center = center, rect = rect, UpItems = UpItems, item_ids = item_ids);
        if self.StepCounter >= len(self.graphlist):                             # 播放完成后解锁空格与回车操作 |  Unlock the space and enter operations when playback is complete
            self.remove_command(pygame.K_SPACE);
            self.remove_command(pygame.K_RETURN);
            self.return_newcID(self.nextScreen);
            return;
        
        # Record the frams that the program has experienced before the last reset of FPSCounter
        # Let StepCounter plus 1 when MaxFPSCounter number of frams have occured, and reset the FPSCounter
        self.tempcounter = 0;
        self.FPSCounter += 1;
        if self.FPSCounter == self.MaxFPSCounter:
            self.FPSCounter = -1;
            self.tempcounter = 1;
        else: return;
        
        if self.tempcounter == 1:
            self.StepCounter += 1;
            self.tempcounter = 0;
        #<--------------------------------------------------------------------
        
        if self.StepCounter == -1:
            # Initialize the PPT playing, lock the opsrations
            self.add_command(pygame.K_SPACE, '');
            self.add_command(pygame.K_RETURN, '');
            self.StepCounter += 1;
        
        try:
            if self.graphitem.moveimage.name != self.graphlist[self.StepCounter]:
                self.graphitem.update_image(self.graphlist[self.StepCounter]);
        except IndexError:  self.StepCounter = len(self.graphlist);
    
    def show(self, show_item_id = None, show_image_id = ()):
        self.graphitem.draw(self.screen);
        ps.SubScreen.show(self, show_item_id = show_item_id, show_image_id = show_image_id);