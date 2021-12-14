# Modified drawing function & Data structure (IndexScreen), 针对菜单界面专门适配的MoveImage, ID_Set, InteractImage与SubScreen
# 除python第三方包外仅调用Tools, Item, Camera层以及Config_Resource
# Except for the third-party packages of Python, this file only uses Tools, Item and Camera folders and Config_Resource.
import pygame
import numpy as np
from Config_Resource import default_select, name_indicator, SESet
from py.Screen import Basic as sb
from py.Tools import Pre as tp

class Icon_Image(sb.InteractImage):
    #  与InteractImage相同, 但不再向下传递指令  |  This class is the same as class 'InteractImage', but it doesn't pass down instructions.
    #  内置基本操作指令 |  This class contains basic operating instructions.
    #  增加了将自身Command_ID借助pygame.USEREVENT传出的功能 | This class adds the method to pass out its own 'Command_ID' with the help of pygame.USEREVENT.
    """
    Data:
        (Camera_Basic.InteractImage)
        name - str
        orimage
        Command_ID
        AddInfo

    Methods:
        (Camera_Basic.InteractImage)
        __init__
        get_command
        return_select
    """
    def __init__(self, name = "Item", orimage = None, Command_ID = None, AdditionInfo = None):
        sb.InteractImage.__init__(self, name = name, orimage = orimage, Command_ID = Command_ID);
        self.AddInfo = AdditionInfo;
        self.add_command(pygame.K_SPACE, 'self.return_select()');
        self.add_command(pygame.K_RETURN, 'self.return_select()');
    
    def get_command(self, command_key):
        try:
            sb.Indicator.get_command(self, command_key);
        except KeyError:
            pass;
    def return_select(self):
        # 将自身Command_ID借助pygame.USEREVENT传出  | Passes out its own 'Command_ID' with the help of pygame.USEREVENT
        if self.Command_ID == None:
            return;
            
        SESet['Confirm'].play_music();
        temp_event = pygame.event.Event(pygame.USEREVENT, name = 'win_screen_command', creater = 'Icon_Image', value = self.Command_ID);
        pygame.event.post(temp_event);

class Icon_Set(sb.ID_Set):
    # 针对Screen_Basic.InteractImage数据类型专门编写的ID_Set子类
    # This is a class inherited from class 'sb.ID_Set' which is specifically designed for the 'Screen_Basic.InteractImage'.
    # 唯一地绑定一个SubScreen类型  |  It binds a SubScreen type uniquely.
    """
    Data:
        (Camera_Basic.ID_Set)
        ShowMode_str - list[str]
        loce_screen - Camera_Basic.SubScreen
        ShowMode - str
    Methods:
        (Camera_Basic.ID_Set)
        __init__
        __str__
        list_ShowMode
        is_locked
        lock
        set_icon_location
    """
    ShowMode_str = ['|', '||', 'O'];
    def __init__(self, show_id = None):
        sb.ID_Set.__init__(self, Elemtype = sb.InteractImage, show_id = None);
        self.lock_screen = None;             # 绑定记录自己的SubScreen | Binds and records SubScreen of itself. 
        self.ShowMode = '|';
    
    def __str__(self):
        return sb.ID_Set.__str__(self) + f"lock_screen = {self.lock_screen}\nShowMode = {self.ShowMode}\n";
    
    def list_ShowMode(self):
        print(f"ShowModeList:\n{self.ShowMode_str}\n")
    
    def is_locked(self):
        return isinstance(self.lock_screen, sb.SubScreen);
    
    def lock(self, subscreen):
        #  输入并绑定一个SubScreen | Input and bind a SubScreen
        if isinstance(subscreen, sb.SubScreen) and not self.is_locked():
            self.lock_screen = subscreen;
    
    def set_icon_location(self, ShowMode = None, anglerange = None, radius = None):
        #  根据绑定的SubScreen 尺寸与输入的icon排列模式重新排列当前的显示icon集  | Rearrange the current set of display icons according to the bound SubScreen size and the pattern of input icon.
        if not self.is_locked():
            return;
        
        if ShowMode in self.ShowMode_str:
            self.ShowMode = ShowMode;
        else:
            ShowMode = self.ShowMode;
        
        temp_icons = self.get_show_index();
        temp_rect = self.lock_screen.draw_rect;
        
        if ShowMode == '|':
            dh = temp_rect.h//(len(temp_icons) + 3);
            height = 2 * dh;
            for icon in temp_icons:
                temp_icons[icon].move_to(location = (temp_rect.center[0], height), Center = True);
                height += dh;
        
        if ShowMode == '||':
            dh = temp_rect.h//(len(temp_icons)//2 + 3);
            dw = temp_rect.w//3;
            height = 2 * dh;
            width = dw;
            
            for icon in temp_icons:
                temp_icons[icon].move_to(location = (width, height), Center = True);
                if width > temp_rect.center[0]:
                    width = dw;
                    height += dh;
                else:   width = 2 * dw;
        
        if ShowMode == 'O':
            center = pygame.display.get_surface().get_rect().center;
            if not tp.is_number(radius): radius = min((min(pygame.display.get_surface().get_rect().size)-150)//2, 250);
            if not tp.is_location_tuple(anglerange): anglerange = (0, 2 * np.pi);
            angle, max_angle = anglerange;
            for icon in temp_icons:
                temp_icons[icon].move_to(location = tp.add_location_tuple(center,(np.sin(angle) * radius, -np.cos(angle) * radius)), Center = True);
                angle += (max_angle) / len(temp_icons)

class Indicator_Image(sb.InteractImage, sb.Indicator):
    # 显示选项的箭头, 继承自Screen_Basic.InteractImage类型, 充当IndexScreen类型的indicator
    # This class displays options of indicator. It is inherited from Screen_Basic.InteractImage, as an indicator for IndexScreen.
    """
    Data:
        (Screen_Basic.InteractImage)
        select_icon_set - dict{Screen_Basic.InteractImage}
        select_icon - Screen_Basic.InteractImage
        select_index - int
        select_length - int
        
        add_command( pygame.K_LEFT: ..., pygame.K_RIGHT: ..., pygame.K_UP: ..., pygame.K_DOWN: ... )
    Methods:
        (Screen_Basic.InteractImage)
        __init__
        __bool__
        change_select_set
        switch_select
        get_command
        draw
    """
    def __init__(self, name = default_select, orimage = None):
        sb.InteractImage.__init__(self, name = name, orimage = orimage, Command_ID = name_indicator);
        
        self.select_icon_set = None;    # 记录显示选项icon的集合与当前选项在集合中的下标(list化), 初始为空  | Record the set of icon and the index number of the current option in the set. Initial value is None.
        self.select_icon = None;        # 
        self.select_index = None;       # 仅能被内置操作修改  | It can only be modified by built-in operations.
        self.select_length = None;      # 记录所有icon选项的个数, 仅在select_icon_set变更时变更 | Records the number of all icon options. It changes only if 'select_icon_set' is changed.
    
    def __bool__(self):
        # 当self.select_index非int时返回False  | Returns False when 'self.select_index' is not int.
        return type(self.select_index) == int;
    
    def change_select_set(self, icons):
        # 更改选项icons的集合  |  Change the set of option icons
        if isinstance(icons, Icon_Set):
            self.select_icon_set = icons.get_show_index();
            self.select_index = None;
            self.select_icon = None;
            self.select_length = len(self.select_icon_set);
    
    def switch_select(self, switch_dire = None):
        # 当select_icon_set记录了一组icons时(即成功执行了一次change_select_set), 根据switch_dire的值计算箭头指向的新选项, 并同步箭头位置
        # When 'select_icon_set' has recorded a set of icons (i.e. a change_select_set has been successfully executed), calculates the new option pointed by the arrow based on the value of 'switch_dire', then synchronize the arrow's position.
        if type(self.select_icon_set) != dict:
            return;
        if type(switch_dire) != int:
            return;
            
        if self.select_index == None:
            self.select_index = -1 if switch_dire > 0 else 0; 
        self.select_index = (self.select_index + switch_dire) % self.select_length;
        
        self.select_icon = self.select_icon_set[list(self.select_icon_set)[self.select_index]];
        
        self.move_to(location = self.select_icon.get_center(), Center=True);
        SESet['se.selection'].play_music();
    
    def get_command(self, command_key):
        # 在原始函数的基础上增加忽略无效输入的功能  | Add an function to ignore invalid input on the base of original method.
        # 此函数仅作为指令链的尾部而被使用 | This method is only used as the end of the instruction chain.
        try:
            sb.InteractImage.get_command(self, command_key);
        except KeyError:
            if isinstance(self.select_icon, sb.Indicator):
                self.select_icon.get_command(command_key);
        """def hidden(self):
        # 隐藏indicator
        # 暂时无用
        self.select_icon, self.select_index = None, None;"""
    
    def draw(self, SCREEN):
        # 当self.select_index非int时不显示图像 | It doesn't show image when 'self.select_index' is not int.
        if self.__bool__():
            sb.InteractImage.draw(self, SCREEN);

class IndexScreen(sb.SubScreen):
    # 针对菜单界面专门编写的SubScreen子类  | This class is inherited from class sb.SubScreen, which is used specifically for the menu screen.
    """
    Data:
        (Camera_Basic.SubScreen)
        images - Icon_Set
        indicator - InteractImage (with command set)
    Methods:
        (Camera_Basic.SubScreen)
        __init__
        set_icon_location
        update
    """
    showItemID = []                                                             # 需要显示的items集合  | The set of items to be displayed
    showImageID = []                                                            # 需要显示的images集合 | The set of images to be displayed
    updateItemID = []                                                           # 需要更新的items集合  | The set of items to be updated
    updateImageID = []                                                          # 需要更新的images集合 | The set of images to be updated
    
    def __init__(self, size = None, center = None, rect = None, scale_rate = None, scale_center = None):
        # 生成类似SubScreen, 但self.images更改为存储Icon_Set数据类型 
        # This class is similar to class 'sb.SubScreen', but 'self.images' is changed to store the data type of 'Icon_Set'. 
        sb.SubScreen.__init__(self, size = size, center = center, rect = rect, scale_rate = scale_rate, scale_center = scale_center);
        self.images = Icon_Set();
        self.images.lock(self);
        # <---------------------------------------------------------------------
        # Indicator类:增加重设指令 | class Indicator: Add a reset command
        self.add_command('Reset', 'self.restart()');
    
    def change_bgp(self, name = None, bgp_image = None, win_screen = None, bgpScreenID = None):
        # 更改背景图片并记录此次更改  |  Changes the background image and record this change.
        # 优先检测win_screen与bgpScreenID参数, 若win_screen是WinScreen且含有SetID为bgpScreenID的界面, 则将此集合内的界面作为背景使用
        # Priority is given to detecting the 'win_screen' and 'bgpScreenID' parameters. If 'win_screen' is WinScreen and contains a screen with a SetID of 'bgpScreenID', the screens in this set are used as the background.
        # 若上述检测失败但self记录了可用的win_screen以及bgpScreenID, 则将记录的界面作为背景使用
        # If the above detection fails but 'self' records an available 'win_screen' and 'bgpScreenID', the recorded screen will be used as the background.
        # 若上述检测失败, 则使用bgpName, bgpImage参数进行默认的sb.SubScreen.change_bgp()更改, 并记录bgpName, bgpImage
        # If the above detection fails, uses the parameters 'bgpName' and 'bgpImage' to change the default 'sb.SubScreen.change_bgp()', then record 'bgpName' and 'bgpImage'.
        try:
            temp_set = win_screen.sub_screens.indexes[bgpScreenID];
            temp_image = pygame.Surface(size = win_screen.screen.get_rect().size);
            [temp_set[screen].draw(temp_image) for screen in temp_set];
            sb.SubScreen.change_bgp(self, bgp_image = temp_image);
            self.store_WinScreen = win_screen;
            self.store_bgpScreenID = bgpScreenID;
            return;
        except AttributeError:  pass;
        except: pass;
        
        try:
            self.change_bgp(win_screen = self.store_WinScreen, bgpScreenID = self.store_bgpScreenID);
            return;
        except AttributeError:  pass;
        
        try:
            sb.SubScreen.change_bgp(self, name, bgp_image);
            self.store_bgpName = name;
            self.store_bgpImage = bgp_image;
            return;
        except AttributeError:  pass;
        except: pass;
        
        try:
            self.change_bgp(name = self.store_bgpName, bgp_image = self.store_bgpImage);
            return;
        except AttributeError:  pass;
    
    def restart(self):
        # 将界面重设至初始状态 | Reset the screen to its initial state.
        try: 
            self.indicator.change_select_set(self.images);
        except AttributeError:  pass;
        self.change_bgp();
    
    def set_indicator(self, indicator_name = default_select, orimage = None):
        # 创建箭头, 仅在选项icons集合不为空时才能被成功创建
        # Create indicator only if the set of 'icons' is not empty.
        if self.images:
            self.indicator = Indicator_Image(name = indicator_name, orimage = orimage);
            self.indicator.change_select_set(self.images);
        
        self.indicator.add_command(pygame.K_LEFT, 'self.switch_select(-1)');    # |内置indicator操作指令集 | Built-in command set of indicator operation 
        self.indicator.add_command(pygame.K_RIGHT, 'self.switch_select(1)');    # |
        self.indicator.add_command(pygame.K_UP, 'self.switch_select(-1)');      # |
        self.indicator.add_command(pygame.K_DOWN, 'self.switch_select(1)');     # |
    
    def set_icon_location(self, ShowMode = None, anglerange = None, radius = None):
        # 根据界面的大小、显示icons的数量以及输入的显示模式规则排列icons
        # Arrange the icons according to the size of the screen, the number of icons to be displayed and the rules of input showMode.
        self.images.set_icon_location(ShowMode = ShowMode, anglerange = anglerange, radius = radius);
    
    def show(self):
        sb.SubScreen.show(self, show_item_id = self.showItemID, show_image_id = self.showImageID);
        try:
            self.indicator.draw(self.screen);
        except AttributeError:  pass;