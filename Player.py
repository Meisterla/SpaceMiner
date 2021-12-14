# Indicator item
import py.Tools.Items.Planet as tip
from py.Tools.Indicator import Indicator
from Config_Resource import SESet

class IndicatorPlanet(tip.PlanetItem, Indicator):
    """
    Data；
        name
        rotatecenter
        rotatespeed
        radius
        itemType
    
    Methods:
        __init__(name = None, rotatespeed = 0, rotatecenter = None, radius = None)
        add_tag(tagkey = None, tagvalue = None)
        remove_tag(tagkey = None, RemoveAll = False)
        interact(Object)
    """
    tag = {};                                                                   # 用于缓存信息的标签集, 注意及时移除不用的tag选项    The tag set used to cache information. Please be aware of removing unused tag options in time.
    screen = None;                                                              # 缓存所属的SubScreen, 仅供临时读取\调用方法     The SubScreen to which cache belongs, only available for temporary reading or invoking methods.
    def __init__(self, name = None, rotatespeed = 0, rotatecenter = None, radius = None):
        # 随机生成一个特征符合设定的主角, 为围绕屏幕中心旋转的爪子
        # Randomly generate a main character Player with the required features, which is a claw that rotates around the centre of the screen.
        Indicator.__init__(self);
        if name == None:    name = 'PlayScreen.Player';
        tip.PlanetItem.__init__(self, name = name);
        self.rotate.update_angle(speed = rotatespeed);
        self.rotate.update_center(center = rotatecenter, radius = radius);
        self.itemType = 'Player';
    
    def add_tag(self, tagkey = None, tagvalue = None):
        if type(tagkey) != str:                                                 # 只接受字符串作为key   Only accepts str as tagkey.
            return;
        try:
            self.tag[tagkey];                                                   # 若tagkey已存在, 进行下述操作  If the tagkey already exists, do the following actions:
            if tagvalue == None:
                if type(self.tag[tagkey]) == int:
                    self.tag[tagkey] += 1;                                      # |若tagvalue为None且self.tag[tagkey]为整数, 则将此key继续作为计数器使用    If tagvalue is None and self.tag[tagkey] is int, then this tagkey will continue to be used as a counter.
                else:   return;                                                 # |若tagvalue为None但self.tag[tagkey]不是整数, 则不操作 If tagvalue is None but self.tag[tagkey] is not int, then do nothing.
            else:   self.tag[tagkey] = tagvalue;                                # |若tagvalue非None, 则将值覆盖     If tagvalue is not None, then self.tag[tagkey] will be overwritten by tagvalue.
                
        except KeyError:                                                        # 若tagkey不存在, 进行下述操作  If tagkey doesn't exist, do the following actions:
            self.tag[tagkey] = 1 if tagvalue == None else tagvalue              # |tagvalue为None时赋予整数, 用作计数器, 不然赋予tagvalue   If tagvalue is None, self.tag[tagkey] will be assigned an int value and used as a counter, otherwise, it will be assigned tagvalue.
    
    def remove_tag(self, tagkey = None, RemoveAll = False):
        if RemoveAll:   [self.tag.pop(key) for key in self.tag.copy()]          # 若RemoveAll为True, 则清空tag  If RemoveAll is True, clear the tag.
        try:                                                                    # 若RemoveAll为False, 则尝试移除tagkey  If RemoveAll is False, attempt to remove the tagkey.
            self.tag.pop(tagkey)
        except KeyError:    return;
    
    def interact(self, Object):
        if not tip.is_touch_round_item(self, Object):
            return;
        
        if Object.itemType == 'RockPlanet':                                     # 遇到陨石, 击碎, 添加rock标记  If encountering a RockPlanet, crash it and add a 'rock' tag to it.
            self.interact_give_crash(Object, rate = 0.9);
            self.add_tag('rock');
            Object.Ruins();
            SESet['se1'].play_music();
            return;
        
        if Object.itemType == 'IceRockPlanet':                                  # 遇到冰冻陨石, 被弹回, 添加icerock标记并停止检测与冰陨石的碰撞 If encountering a IceRockPlanet, player is bounced back, add a 'icerock' tag and stop detecting collisions for this object.
            if 'icerock' in self.tag:
                return;
            self.move.speed.negative();
            self.add_rotate(angle = 180);
            self.add_tag('icerock');
            SESet['reflect'].play_music();
            return;
        
        if Object.itemType == 'HotRockPlanet':                                  # 遇到熔融陨石, 击碎, 添加hotrock标记   If encountering a HotRockPlanet, crash it and add a 'hotrock' tag to it.
            self.interact_give_crash(Object, rate = 0.9);
            self.add_tag('hotrock');
            Object.Ruins();
            SESet['boom'].play_music();
            return;
        
        if Object.itemType == 'HealingBoxItem':
            self.add_tag('healing');
            Object.update_speed(speed=(0,0));
            Object.Ruins();
            SESet['collect.packet'].play_music();
            return;
        
        if Object.itemType == 'TimingBoxItem':
            self.add_tag('timing');
            Object.update_speed(speed=(0,0));
            Object.Ruins();
            SESet['collect.packet'].play_music();
            return;
        
        if Object.itemType in ['YellowRockPlanet']:                             # 捕获, 添加catched标记并停止检测该物体的碰撞   Catch YellowRockPlanet, add a 'catched' tag and stop detecting collisions for this object.
            if 'catched' in self.tag:
                if Object not in self.tag['catched']:
                    Object.update_speed(speed = self.get_speed(), addspeed = (0, 0));
                    self.screen.items.move_elem(Object.itemID, self.screen.mainItemID, self.screen.catchedItemID);
                    self.tag['catched'] += [Object];
                return;
            Object.update_speed(speed = self.get_speed(), addspeed = (0, 0));
            self.screen.items.move_elem(Object.itemID, self.screen.mainItemID, self.screen.catchedItemID);
            self.add_tag('catched', [Object]);
            SESet['touch.gold'].play_music();
            return;