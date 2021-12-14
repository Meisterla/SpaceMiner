#Special Planet Item
import numpy as np
import Config_Resource as cr
import py.Tools.Pre as tp
from py.Tools.Items import Planet as tip

class RockPlanet(tip.PlanetItem):
    itemType = 'RockPlanet';
    def __init__(self, location = None, rotatespeed = 0):
        #随机生成一个特征符合设定的陨石
        mass = np.random.randint(cr.item_mass_breaks[0], cr.item_mass_breaks[1]);
        tempr = np.random.randint(cr.item_tempr_breaks[0], cr.item_tempr_breaks[1]);
        tip.PlanetItem.__init__(self, name = 'Rock', location = location, rotatespeed = rotatespeed, mass = mass, tempr = tempr);
        
        self.update_size();
    
    def interact(self, Object):
        if not tip.is_touch_round_item(self, Object):
            return;
        
        if 'Rock' in Object.itemType:                                           #只与Rock类型发生both碰撞
            self.interact_both_crash(Object = Object);

class IceRockPlanet(tip.PlanetItem):
    itemType = 'IceRockPlanet';
    def __init__(self, location = None, rotatespeed = 0):
        #随机生成一个特征符合设定的陨石
        mass = np.random.randint(cr.item_mass_breaks[0], cr.item_mass_breaks[1]);
        tempr = np.random.randint(cr.item_tempr_range[0], cr.item_tempr_breaks[0]);
        tip.PlanetItem.__init__(self, name = 'IceRock', location = location, rotatespeed = rotatespeed, mass = mass, tempr = tempr);
        
        self.update_size();
    
    def interact(self, Object):
        if not tip.is_touch_round_item(self, Object):
            return;
        
        if 'Rock' in Object.itemType:                                           #只与Rock类型发生both碰撞
            self.interact_both_crash(Object = Object);

class HotRockPlanet(tip.PlanetItem):
    itemType = 'HotRockPlanet';
    def __init__(self, location = None, rotatespeed = 0):
        #随机生成一个特征符合设定的陨石
        mass = np.random.randint(cr.item_mass_breaks[0], cr.item_mass_breaks[1]);
        tempr = np.random.randint(cr.item_tempr_breaks[1], cr.item_tempr_range[1]);
        tip.PlanetItem.__init__(self, name = 'HotRock', location = location, rotatespeed = rotatespeed, mass = mass, tempr = tempr);
        
        self.update_size();
    
    def interact(self, Object):
        if not tip.is_touch_round_item(self, Object):
            return;
        
        if 'Rock' in Object.itemType:                                           #只与Rock类型发生both碰撞
            self.interact_both_crash(Object = Object);

class YellowRockPlanet(tip.PlanetItem):
    itemType = 'YellowRockPlanet';
    def __init__(self, location = None, rotatespeed = 0):
        #随机生成一个特征符合设定的陨石
        mass = np.random.randint(cr.item_mass_breaks[0], cr.item_mass_breaks[1]);
        tempr = np.random.randint(cr.item_tempr_breaks[0], cr.item_tempr_breaks[1]);
        tip.PlanetItem.__init__(self, name = 'YellowRock', location = location, rotatespeed = rotatespeed, mass = mass, tempr = tempr);
        
        self.update_size();
    
    def interact(self, Object):
        if not tip.is_touch_round_item(self, Object):
            return;
        
        if 'Rock' in Object.itemType:                                           #只与Rock类型发生both碰撞
            self.interact_both_crash(Object = Object);

class HealingBoxItem(tip.PlanetItem):
    itemType = 'HealingBoxItem';
    def __init__(self, location = None, rotatespeed = 0):
        #随机生成一个特征符合设定的盒子
        mass = np.random.randint(cr.item_mass_range[0], cr.item_mass_breaks[0]);
        tempr = np.random.randint(cr.item_tempr_breaks[0], cr.item_tempr_breaks[1]);
        tip.PlanetItem.__init__(self, name = 'HealingBox', location = location, rotatespeed = rotatespeed, mass = mass, tempr = tempr);
        
        self.update_size();
    
    def interact(self, Object):
        pass;

class TimingBoxItem(tip.PlanetItem):
    itemType = 'TimingBoxItem';
    def __init__(self, location = None, rotatespeed = 0):
        #随机生成一个特征符合设定的盒子
        mass = np.random.randint(cr.item_mass_range[0], cr.item_mass_breaks[0]);
        tempr = np.random.randint(cr.item_tempr_breaks[0], cr.item_tempr_breaks[1]);
        tip.PlanetItem.__init__(self, name = 'TimingBox', location = location, rotatespeed = rotatespeed, mass = mass, tempr = tempr);
        
        self.update_size();
    
    def interact(self, Object):
        pass;

class CargoShip(tip.PlanetItem):
    itemType = 'CargoShip';
    havecargo = True;                                                           #标记是否还未生成过货物, True为未生成
    def __init__(self, location = None, rotatespeed = None):
        #随机生成一个特征符合设定的盒子
        mass = np.random.randint(cr.item_mass_breaks[0], cr.item_mass_breaks[1]);
        tempr = np.random.randint(cr.item_tempr_breaks[0], cr.item_tempr_breaks[1]);
        tip.PlanetItem.__init__(self, name = 'CargoSS', location = location, mass = mass, tempr = tempr);
        
        self.update_size();
    
    def interact(self, Object):
        pass;
    
    def get_item(self, itemtype):
        itemClass = PlanetCategories[itemtype];
        cr.SESet['spawn.packet'].play_mucis();
        return itemClass(location = self.moveimage.center, rotatespeed=np.random.randint(-40, 40));
    
    def update(self):
        self.update_rotate(angle = tp.get_angle(self.get_speed()));
        tip.PlanetItem.update(self);

#<-----------------------------------------------------------------------------
#class索引
PlanetCategories = {'Rock': RockPlanet, 'IceRock': IceRockPlanet, 'HotRock': HotRockPlanet, 'YellowRock': YellowRockPlanet,
                    'HealingBox': HealingBoxItem, 'TimingBox': TimingBoxItem, 'CargoSS': CargoShip};

def get_PlanetClass(name):
    try:
        return PlanetCategories[name];
    except KeyError:    return;
