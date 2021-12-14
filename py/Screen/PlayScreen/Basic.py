# PlayScreen
from numpy.random import randint, rand
from pygame.rect import Rect
from py.Tools.Items.Planet import is_touch_round_item
from Player import IndicatorPlanet
from py.Screen.PlayScreen.ScoreTools import ScoreImage
from Config_Resource import FPS, BGMSet, SESet

import pygame
import py.Screen.Basic as sb
import py.Tools.Pre as tp
import py.Tools.Items.Special as tis

PlayerRadius = 275;
bgmname = '8-bit-game-music';

class PlayScreen(sb.SubScreen):
    """
    Data:
    (Camera_Basic.SubScreen)
    indicatorSet
    scoreimage
    timeimage
    healthimage
    showImageID

    Methods:
        (Camera_Basic.SubScreen)
        __init__
        restart - Reset the interface to its initial state
        reset_difficulty - Set the game generation data according to the parameters, which affect the difficulty of the game.
        get_dynamic_indicator
        remove_dynamic_indicator - Remove the 'Dynamic' indicator and switch back to the 'Static' indicator.
        update
        check_itempopulation - Count the number of items in a specific set of items that are in all ranges of self.RectSet['spawn', 'spawndetect'].
        check_dead - Death detection
        check_range - Range detection
        check_speed - Speed detection
        get_planet - Generate planet types based on the name entered
        get_random_planet
        get_planets - Generate planets in batches
        random_select_name - Randomly pick a member from self.itemNameList
        end_game
        show
    """
    # 预设\可调参数
    # Pre-set or adjustable parameters
    indicatorNameList = ['Thor.Up&Down', 'Isaac.Up&Down']
    indicatorName = indicatorNameList[randint(0, 2)];
    indicatorSize = (75, 75)
    itemNameList = ['Rock', 'HotRock', 'CargoSS', 'YellowRock', 'IceRock'];     # 预设item生成概率, 调试用(提交前记得改!!!)
                                                                                # Preset probabilities of generating item, for debugging use.
    
    bgImageID_Info = 'bg.info'
    
    bgItemID_SAI = 'bg.sai';                                                    # (Same Angle with Indicator)与indicator相同旋转角度的装饰item集合id, 不自动更新, 但旋转角会与indicator强制同步
    deadItemID = 'deadplanet';                                                  # (Same Angle with Indicator) The id of the decorated item Set which have the same rotation angle as the 'indicator'.It does not automatically update, but the rotation angle is forced to be synchronized with the 'indicator'.
    mainItemID = 'planet'
    catchedItemID = 'catchedplanet';
    PlayerRotateSpeed = 40;
    PlayerMoveSpeed = 400;
    MaxItemSpeed = 60;
    MinItemSpeed = 20;
    MaxItem = 5;
    
    #显示\更新集合
    #Show \Update Set
    showItemID = [mainItemID, deadItemID, catchedItemID, bgItemID_SAI]          # 需要显示的items集合   | Set of items to be displayed.
    showImageID = [bgImageID_Info]                                              # 需要显示的images集合  | Set of images to be displayed.
    updateItemID = [deadItemID, mainItemID, catchedItemID]                      # 需要更新的items集合   | Set of items to be updated.
    updateImageID = []                                                          # 需要更新的images集合  | Set of images to be updated.
    
    #生成\消失检测范围
    #Generate \ disappearance detection range
    RectSet = {};
    RectSet['spawn'] = [Rect(216,116,368,368)];
    #RectSet['spawn'] = [Rect(350,250,100,100)];
    RectSet['spawndetect'] = [Rect(125,25,550,550)];
    RectSet['range'] = [Rect(100,0,600,600)];
    
    #游戏数据
    #Data of game
    fpscounter = 0;                                                             # 记录当前经过多少帧   |  Record how many frames have currently passed.
    timecounter = 0;                                                            # 记录当前经过多少秒   |  Record how many seconds have currently passed.
    timequater = False;                                                         # 记录当前帧timecounter是否发生了改变  |  Record whether the 'timecounter' of current frame changed or not.
    
    score_max_digit = 8;
    score = 0;
    scoreimage = None;
    time_limit = 120;
    timer = 0;
    timeimage = None;
    maxhealth = 10;
    inithealth = 5;
    health = 5;
    healthimage = None;
    
    def __init__(self, scale_rate = None):
        sb.SubScreen.__init__(self, scale_rate = scale_rate);
        #<---------------------------------------------------------------------
        self.indicatorSet = {};                                                 #创建多indicator结构  |  Create a multi-indicator structure
        
        indicator = IndicatorPlanet(name = self.indicatorName, rotatecenter = self.draw_rect.center, radius = PlayerRadius); #indicator 由self.restart()定义  |  indicator is defined by self.restart()
        indicator.move_to(location = tp.add_location_tuple(self.camera_rect.center, (0, -PlayerRadius)), Center = True);
        indicator.scale_to(size = self.indicatorSize);
        indicator.skip = True;
        self.indicatorSet['Static'] = indicator;                                #创建key为'Static'的indicator, 此indicator为主要控制对象  |  Create an indicator with key equaling to 'Static'. This indicator is the main control object.
        self.indicator = self.indicatorSet['Static'];                           #记录'Static'indicator为self.indicator   |   Record 'Static'indicator as self.indicator.
        #self.restart();
        
        #<---------------------------------------------------------------------
        #添加游戏信息显示图层  | Add a game information display layer
        self.scoreimage = ScoreImage(self.score, self.score_max_digit,location = (700,500), Center = True);
        self.timeimage = ScoreImage(self.timer, 3, location = (645, 200));
        self.healthimage = ScoreImage(self.health, 2, location = (645, 290));
        
        self.add_images(self.scoreimage, self.timeimage, self.healthimage, imageSetID = 'bg.info');
        self.showImageID += ['bg.info'];
        #<---------------------------------------------------------------------
        #Indicator类:增加重设指令 |  Class Indicator: Add reset command
        self.add_command('Reset', 'self.restart()');
        self.add_command('Easy', 'self.reset_difficulty(0)');
        self.add_command('Normal', 'self.reset_difficulty(1)');
        self.add_command('Hard', 'self.reset_difficulty(2)');
        self.add_command('Endless', 'self.reset_difficulty(3)');
        
        self.add_command((pygame.KEYDOWN, pygame.K_SPACE), 'self.get_dynamic_indicator()');
        
        self.indicator.add_command((pygame.KEYDOWN, pygame.K_RIGHT), f'self.add_rotate(speed = {self.PlayerRotateSpeed})');
        self.indicator.add_command((pygame.KEYDOWN, pygame.K_LEFT), f'self.add_rotate(speed = {-self.PlayerRotateSpeed})');
        self.indicator.add_command((pygame.KEYUP, pygame.K_RIGHT), f'self.add_rotate(speed = {-self.PlayerRotateSpeed}, SkipZero = True)');
        self.indicator.add_command((pygame.KEYUP, pygame.K_LEFT), f'self.add_rotate(speed = {self.PlayerRotateSpeed}, SkipZero = True)');
        
        #self.indicator.add_command((pygame.KEYDOWN, pygame.K_SPACE), 'self.add_rotate(angle = 180)');
    
    def restart(self):
        #将界面重设至初始状态 |  Reset the interface to its initial state
        #移除地图item |  Remove mapitem
        self.items.remove_set(self.mainItemID, self.deadItemID, self.catchedItemID);
        
        #重置indicator | Reset indicator
        self.remove_dynamic_indicator();
        self.indicatorSet['Static'].update_rotate(angle = 0, speed = 0, addspeed = 0);
        self.indicatorName = self.indicatorNameList[randint(0, 2)];
        self.indicator.update_image(self.indicatorName);
        
        #重置数据  | Reset data
        self.fpscounter = 0;
        self.timecounter = 0;
        self.timequater = False;
        self.score = 0;
        self.scoreimage.update_score(self.score);
        self.timer = 0;
        self.timeimage.update_score(self.time_limit);
        self.health = self.inithealth;
        self.healthimage.update_score(self.health);
        
        #重置BGM  |  Reset BGM
        for bgm in BGMSet:
            BGMSet[bgm].stop_music();
        BGMSet[bgmname].play_music();
    
    def reset_difficulty(self, diff = None):
        # 根据参数设置游戏生成数据, 这些数据会影响游戏的难度
        # Set the game initial data according to parameters, which could affect the difficulty of the game.
        if type(diff) != int:   return;
        
        if diff == 0:
            self.time_limit = 180;
            self.maxhealth = 10;
            self.inithealth = 10;
            self.PlayerRotateSpeed = 120;
            self.PlayerMoveSpeed = 600;
            self.MaxItemSpeed = 60;
            self.MaxItem = 10;
            self.itemNameList = ['Rock', 'YellowRock', 'HealingBox', 'IceRock', 'HotRock', 'TimingBox'];
        
        if diff == 1:
            self.time_limit = 120;
            self.maxhealth = 8;
            self.inithealth = 5;
            self.PlayerRotateSpeed = 80;
            self.PlayerMoveSpeed = 400;
            self.MaxItemSpeed = 60;
            self.MaxItem = 8;
            self.itemNameList = ['Rock', 'HotRock', 'CargoSS', 'YellowRock', 'IceRock'];
        
        if diff == 2:
            self.time_limit = 60;
            self.maxhealth = 5;
            self.inithealth = 3;
            self.PlayerRotateSpeed = 40;
            self.PlayerMoveSpeed = 350;
            self.MaxItemSpeed = 180;
            self.MaxItem = 8;
            self.itemNameList = ['Rock', 'IceRock', 'HotRock', 'CargoSS', 'YellowRock'];
        
        if diff == 3:
            self.time_limit = 999999;
            self.maxhealth = 10;
            self.inithealth = 1;
            self.PlayerRotateSpeed = 40;
            self.PlayerMoveSpeed = 350;
            self.MaxItemSpeed = 120;
            self.MaxItem = 6;
            self.itemNameList = ['Rock', 'IceRock', 'CargoSS', 'HotRock', 'YellowRock'];
    
    def get_dynamic_indicator(self):
        # 若'Dynamic'indicator已存在则不执行 | This method does not execute if the 'Dynamic' indicator already exists.
        # 生成临时的'Dynamic'indicator, 其初始位置为'Static'indicator当前的显示位置 | This method generates a temporary 'Dynamic' indicator, the initial location of which is the current display location of the 'Static' indicator.
        # 将self.indicator切换至'Dynamic'indicator, 并沿直径方向移动至圆环另一端  |  Switch the self.indicator to 'Dynamic' indicator and move it along the diameter direction to the other end of the circle.
        # 移动过程中发生碰撞检测   |  Collision detection during movement.
        # 此处仅用于初始化'Dynamic'indicator   |  This method is only used to initialise the 'Dynamic' indicator
        if 'Dynamic' in self.indicatorSet:
            return;
        
        try:
            new_indicator = IndicatorPlanet(name = self.indicatorName+'.dynamic');
        except KeyError:    new_indicator = IndicatorPlanet(name = self.indicatorName);
        new_indicator.scale_to(size = self.indicator.moveimage.rect.size);
        new_indicator.update_rotate(angle = self.indicator.rotate.angle);
        new_indicator.move_to(self.indicator.display.center, Center = True);
        
        temp_tuple = tp.minus_location_tuple(self.draw_rect.center, new_indicator.moveimage.center);
        temp_tuple = tp.dot_tuple(temp_tuple, self.PlayerMoveSpeed/tp.distance_location_tuple(temp_tuple));
        new_indicator.update_speed(speed = temp_tuple);
        new_indicator.screen = self;
        
        self.indicatorSet['Dynamic'] = new_indicator;
        self.indicator.update_rotate(speed = 0);
        
        self.indicator = self.indicatorSet['Dynamic'];
        SESet['launch'].play_music();
    
    def remove_dynamic_indicator(self, Opposite = False):
        # 移除'Dynamic'indicator并切换回'Static'indicator    |  Remove the 'Dynamic' indicator and switch back to the 'Static' indicator
        # 根据参数决定是否将'Static'indicator移动至圆环另一侧  |  The parameters determine whether the 'Static' indicator should be moved to the other side of the circle or not.
        try:
            self.indicatorSet.pop('Dynamic');
        except KeyError:    pass;
        self.indicator = self.indicatorSet['Static'];
        
        if Opposite:
            self.indicator.add_rotate(angle = 180);
        self.indicator.update();                                                # 更新indicator显示信息, 防止闪帧  |  Update indicator display information in case of frames flashing.
    
    def update(self, UpSize = False, size = None, center = None, rect = None, UpItems = False, item_ids = None):
        sb.SubScreen.update(self, UpSize = UpSize, size = size, center = center, rect = rect, UpItems = UpItems, item_ids = item_ids);
        self.indicator.update();
        
        self.fpscounter += 1;                                                   # 更新时间与帧记录, 其中帧记录了距离timecounter上一次更新运行了多少帧  |  Update time and frame records. The frame records how many frames have elapsed since the 'timecounter' was last updated.
        if self.timequater:     self.timequater = False;                        # 检测timecounter前先重置timequater  | Reset timequater before determing timecounter.
        if self.fpscounter == FPS:                                              # 时间记录了当前总共运行了多少秒   |  The timecounter records the total number of seconds currently running.
            self.timecounter +=1;
            self.timequater = True;
            self.fpscounter = 0;
        #
        #<---------------------------------------------------------------------
        # 同步游戏信息:timer, health
        # Synchronised game information: timer, health
        if self.timequater:     self.timer += 1;
        if self.timer > self.time_limit:    self.timer = self.time_limit;
        elif self.timer < 0:    self.timer = 0;
        
        if self.health > self.maxhealth:    self.health = self.maxhealth;
        elif self.health < 0:   self.health = 0;
        #
        #<---------------------------------------------------------------------
        # 判断游戏是否结束
        # Determine if the game is over
        if self.timer == self.time_limit:
            self.end_game();
            return;
        if self.health == 0:
            self.end_game();
            return;
        #
        #<---------------------------------------------------------------------
        # 同步游戏信息:贴图
        # Synchronised game information: Images
        self.scoreimage.update_score(self.score);
        self.timeimage.update_score(self.time_limit - self.timer);
        self.healthimage.update_score(self.health);
        #
        #<---------------------------------------------------------------------
        # showitem交互检测\与indicator检测部分:
        # showitem interaction detection\ with indicator detection section:
        temp_dict = self.items.get_set().copy();
        for item in temp_dict:
            self.indicator.interact(temp_dict[item]);
        
        for item1 in temp_dict:
            for item2 in temp_dict:
                if item1 == item2:  continue;
                temp_dict[item1].interact(temp_dict[item2]);
        #
        #<---------------------------------------------------------------------
        # 'Dynamic'indicator状态检测
        # 'Dynamic' indicator status detection
        if 'Dynamic' in self.indicatorSet:
            # 'Dynamic'indicator 运动中, 维护tag信息  |  'Dynamic' indicator in motion, maintains tag information
            if 'catched' in self.indicator.tag:                                 # 更新'catched'tag信息, 同步被捕获的item的速度 |  Update 'catched' tag information, synchronize the speed of captured items.
                for item in self.indicator.tag['catched']:
                    item.update_speed(speed = self.indicator.get_speed());
            
            if tp.distance_location_tuple(self.indicator.moveimage.center, self.camera_rect.center) > PlayerRadius:
                # 'Dynamic'indicator 结束一次运动, 提取其tag信息并销毁'Dynamic'indicator  |  When the 'Dynamic' indicator ends movement, extract its tag information and destroy the 'Dynamic' indicator.
                if 'rock' in self.indicator.tag:
                    self.score += self.indicator.tag['rock'] * 10;              # 每碰撞一次陨石增加10分, 暂未写入可定义参数中 |  10 points for each meteorite collision
                    self.indicator.remove_tag('rock');
                
                if 'icerock' in self.indicator.tag:                             # 提取'icerock'tag信息 |  Extract information of 'icerock' tag 
                    self.indicator.remove_tag('icerock');
                    oppoflag = False;
                else:
                    oppoflag = True;
                
                if 'hotrock' in self.indicator.tag:
                    self.health -= self.indicator.tag['hotrock'];
                    self.indicator.remove_tag('hotrock');
                
                if 'healing' in self.indicator.tag:
                    self.health += self.indicator.tag['healing'];
                    self.indicator.remove_tag('healing');
                
                if 'timing' in self.indicator.tag:
                    self.timer -= self.indicator.tag['timing'] * 20;            # 每碰撞一次TimingBox增加20秒可用时间, 暂未写入可定义参数中   |   With Each collision, the 'TimingBox' increases available time by 20 seconds.
                    self.indicator.remove_tag('timing');
                
                if 'catched' in self.indicator.tag:
                    for item in self.indicator.tag['catched']:
                        if item.itemType == 'YellowRockPlanet':
                            self.score += int(item.Mass.value) * 100;   # 按照被捕获物体的质量加分 |  Add score according to Mass of object captured.
                        if 'YellowRockPlanet' in item.itemType:
                            SESet['collect.gold'].play_music();
                        self.items.remove_elem(elemSetID = self.catchedItemID, elemID = item.itemID);
                    self.indicator.remove_tag('catched');
                
                self.remove_dynamic_indicator(Opposite = oppoflag);             # 在tag全部处理完毕后销毁'Dynamic'indicator  |   Destroy the 'Dynamic' indicator after tag being fully processed.
        #
        #<---------------------------------------------------------------------
        # 同步bgItemID_SAI集合item的角度  |   Synchronise the angle of the bgItemID_SAI set item.
        try:
            for item in self.items.indexes[self.bgItemID_SAI]:
                self.items.indexes[self.bgItemID_SAI][item].update_rotate(angle = self.indicator.rotate.angle);
                self.items.indexes[self.bgItemID_SAI][item].update();
        except KeyError:    pass;
        #
        #<---------------------------------------------------------------------
        # item显示更新、生成与移除部分:
        # The section of updating, generating and removing item:
            #| 更新show index的item集合 | Update 'show index's item set
        self.check_dead();
        self.check_range();
        self.check_speed(timelimit = 10 * FPS);                                 # 允许低速item存活10秒 |  Allow item with low speed to live for 10 seconds
            #| 更新deaditem的item集合  |  Update 'deaditem's item set
        self.check_range(self.deadItemID);
        self.check_speed(self.deadItemID, timelimit = 3 * FPS);
        
            #| 在固定区域生成item  |  Generate an item in a fixed area
        if self.check_itempopulation(self.mainItemID) < self.MaxItem:
            for rect in self.RectSet['spawn']:
                if self.get_random_planet(spawn_rect=rect, itemSetID=self.mainItemID): break;
            
            #| 判断Ship是否生成货物, 每秒进行一次判断(借助timequater来决定距离上次判断是否到达1秒)
            # Determine if Ship has generated a cargo per second (With the help of a 'timequater' to determine if time has reached 1 second since the last determination)
        if self.timequater:
            temp_dict = self.items.get_set().copy();
            for item in temp_dict:
                if temp_dict[item].itemType == 'CargoShip':
                    if temp_dict[item].havecargo:                               # 遍历mainitemset的'CargoShip', 若发现havecargo为True的实例, 则概率判断生成 | Read through the 'CargoShip' of the mainitemset. If finding an instance with 'havecargo' True, generate it with probability.
                        if rand() < 0.25:                                       # 每次判断都有25%的概率生成'HealingBox'   |   There is a 25% chance of generating a 'HealingBox' for each determing.
                            self.get_planet(name = 'HealingBox', location = temp_dict[item].moveimage.center, speed = (0, 0));
                            temp_dict[item].havecargo = False;
                            temp_dict[item].speed_up(200);
                            SESet['spawn.packet'].play_music();
                            continue;
                        if rand() < 0.10:                                       # 每次判断都有10%的概率生成'TimingBox' |  There is a 10% chance of generating a 'TimingBox' for each determing.
                            self.get_planet(name = 'TimingBox', location = temp_dict[item].moveimage.center, speed = (0, 0));
                            temp_dict[item].havecargo = False;
                            temp_dict[item].speed_up(200);
                            SESet['spawn.packet'].play_music();
                            continue;
                    
    
    def check_itempopulation(self, itemSetID = None):
        # 统计处于self.RectSet['spawn', 'spawndetect']所有范围下的特定item集合的item个数
        # Count the number of item in a specific set of item that are in all ranges of self.RectSet['spawn', 'spawndetect'].
        count = 0;
        temp_dict = self.items.get_set(itemSetID);
        for item in temp_dict:
            for rect in self.RectSet['spawn'] + self.RectSet['spawndetect']:
                if rect.colliderect(temp_dict[item].moveimage.rect):
                    count +=1;
                    break;
        return count;
    
    def check_dead(self, itemSetID = None):
        #死亡检测  | Death detection
        if itemSetID == self.deadItemID:
            return;
        temp_dict = self.items.get_set(itemSetID);
        for item in temp_dict.copy():
            try:
                if temp_dict[item].skip:                                            #转移死亡物体  | Move dead objects
                    self.items.add_elem(temp_dict[item], elemSetID = self.deadItemID);
                    self.items.remove_elem(item, elemSetID = itemSetID);
            except AttributeError:  pass;
        
    
    def check_range(self, itemSetID = None):
        # 范围检测 |  Range detection
        temp_dict = self.items.get_set(itemSetID);
        for item in temp_dict.copy():
            for rect in self.RectSet['range']:
                if not isinstance(rect, pygame.rect.Rect):
                    continue;
                if not rect.colliderect(temp_dict[item].moveimage.rect):        # 移除rect范围外物体 | Remove objects out of rect range.
                    self.items.remove_elem(item, elemSetID = itemSetID);
                    continue;
    
    def check_speed(self, itemSetID = None, timelimit = None):
        # 速度检测  | Speed detection
        if not tp.is_number(timelimit):    timelimit = FPS;
        temp_dict = self.items.get_set(itemSetID);
        for item in temp_dict.copy():
            try:
                if temp_dict[item].move.speed.distance((0, 0)) <= self.MinItemSpeed/FPS:           # 移除低速物体  |  Remove objects with low speed.
                    try:
                        temp_dict[item].timer += 1;
                        if temp_dict[item].timer > timelimit:
                            temp_dict[item].timer = 0;
                            self.items.remove_elem(item, elemSetID = itemSetID);
                    except AttributeError:  self.items.remove_elem(item, elemSetID = itemSetID);
            except AttributeError:  pass;
    
    def get_planet(self, name = None, location = None, spawn_rect = None, itemSetID = None, speed = None, RandomSpeed = True):
        # 目前可以根据输入的名字生成星球类型  | It is currently possible to generate planet types based on the input name.
        # 应当由spawn_range来指定生成的范围 |  The range of generation should be specified by 'spawn_range'.
        # 若不输入则默认在全屏生成  | If nothing enters, generates planet in full screen by default.
        if itemSetID == None: itemSetID = self.items.show_id;
        
        PlanetClass = tis.get_PlanetClass(name);
        if PlanetClass == None:     PlanetClass = tis.RockPlanet;
        
        # Location detection section
        #|location检测部分, start
        # 若location为坐标则在location处生成, 否则在spawn_rect范围内寻找未占用的位置生成
        # If location type is coordinate, generate planet at location, otherwise, find an unoccupied location within spawn_rect
        if tp.is_location_tuple(location):
            PItem = PlanetClass(location = location, rotatespeed = randint(-40, 40));
        else:
            if not isinstance(spawn_rect, pygame.rect.Rect):
                spawn_rect = self.camera_rect;
            else:
                correct = tp.dot_tuple(self.camera_rect.topleft,-1);
                spawn_rect.topleft = tp.add_location_tuple(spawn_rect.topleft, correct);
            
            count = 0;
            while True:
                # 判断新生成的item是否与现有item重叠;
                # Determine if the newly generated item overlaps with an existing item;
                count += 1
                if count >5:  return False;
                location = randint(spawn_rect.x, spawn_rect.right), randint(spawn_rect.y, spawn_rect.bottom);
                PItem = PlanetClass(location = location, rotatespeed = randint(-40, 40));
                temp_dict = self.items.get_set(itemSetID);
                flag = True;
                for item in temp_dict:
                    #if PItem.moveimage.rect.colliderect(temp_dict[item].moveimage.rect):
                    if is_touch_round_item(PItem, temp_dict[item]):
                        flag = False;
                        break;
                if flag: break;
        #| location检测部分, end
        # Location detection section
        
        # Speed detection section
        #|speed检测部分, start
        if not tp.is_location_tuple(speed):
            # 仅在未给定speed的时候自动生成速度 | Generate speeed automatically only if 'speed' is not given.
            if RandomSpeed:
                # 随机生成速度 |  Generate speed randomly
                if tp.distance_location_tuple(PItem.moveimage.center, self.camera_rect.center) > PlayerRadius * 0.9:
                    # 当item生成在物体边缘, 保证item向中心移动  |  When an item is generated at the edge of the object, it is guaranteed to move towards the centre.
                    speed = tp.minus_location_tuple(self.camera_rect.center, PItem.moveimage.center);
                    speed = tp.dot_tuple(speed, PItem.Mass.get_qlmodel_value(randint(self.MinItemSpeed*1.5, self.MaxItemSpeed+1))/tp.distance_location_tuple(speed));
                    speed = tp.add_location_tuple(speed, (randint(-self.MinItemSpeed//5, self.MinItemSpeed//5), randint(-self.MinItemSpeed//5, self.MinItemSpeed//5)))
                else:
                    speed = (PItem.Mass.get_qlmodel_value(randint(self.MinItemSpeed, self.MaxItemSpeed+1)), PItem.Mass.get_qlmodel_value(randint(self.MinItemSpeed, self.MaxItemSpeed+1)));
                    flag1 = 1 if rand() < 0.5 else -1;
                    flag2 = 1 if rand() < 0.5 else -1;
                    speed = flag1*speed[0], flag2*speed[1];
            else:
                speed = (0, 0);
        #|speed检测部分, end
        # Speed detection section
                
        PItem.update_speed(speed = speed);
        self.add_items(PItem, itemSetID = itemSetID);
        return True;
    
    def get_random_planet(self, spawn_rect = None, itemSetID = None, speed = None, RandomSpeed = True):
        name = self.random_select_name();
        return self.get_planet(name = name, spawn_rect = spawn_rect, itemSetID=itemSetID, speed=speed, RandomSpeed=RandomSpeed);
        
    
    def get_planets(self, num, spawn_rect = None):
        #批量生成星球  | Generate planets in batches
        if type(num) != int:
            return;
        for i in range(num):
            name = self.random_select_name();
            self.get_planet(name = name, spawn_rect = spawn_rect);
    
    def random_select_name(self):
        # 随机从self.itemNameList中挑选一个成员, 只识别self.itemNameList前10位, 不足则补足至10位检测
        # 各位置被选中的概率为: 50, 25, 10, 5, 3, 2, 2, 1, 1, 1 (%)
        # Randomly pick a member from self.itemNameList and identify the first 10 bits of it. Add to 10 bits if it is less than 10 bits.
        # The probability of each position being selected is: 50, 25, 10, 5, 3, 2, 2, 1, 1, 1 (%)
        try:
            temp_list = self.itemNameList.copy();
            while len(temp_list) < 10:
                temp_list += [''];
        except:     return;
        
        if rand()<0.5:  return temp_list[0];                                    #选择位置1 | Choose Postion 1
        else:   temp_list = temp_list[1:];
        
        if rand()<0.5:  return temp_list[0];                                    #选择位置2 | Choose Position 2
        else:   temp_list = temp_list[1:];
        
        if rand()<0.4:  return temp_list[0];                                    #选择位置3 | Choose Position 3
        else:   temp_list = temp_list[1:];
        
        if rand()<1/3:  return temp_list[0];                                    #选择位置4 | Choose Position 4
        else:   temp_list = temp_list[1:];
        
        if rand()<0.3:  return temp_list[0];                                    #选择位置5 | Choose Position 5
        else:   temp_list = temp_list[1:];
        
        if rand()<2/7:  return temp_list[0];                                    #选择位置6、7  | Choose Position 6 & 7
        elif rand()<4/7:  return temp_list[1]
        else:   temp_list = temp_list[2:];
        
        if rand()<1/3:  return temp_list[0];                                    #选择位置8、9、10  | Choose Position 8, 9 and 10
        elif rand()<2/3:  return temp_list[1];
        else:   return temp_list[2];
    
    def end_game(self):
        self.return_newcID('EndScreen.Reset');
        #self.restart();
    
    def show(self):
        sb.SubScreen.show(self, show_item_id = self.showItemID, show_image_id = self.showImageID);
        try:
            correct = tp.dot_tuple(self.camera_rect.topleft,-1);
            self.indicator.draw(self.screen, correct = correct);
        except AttributeError:  pass;