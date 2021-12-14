#Item Class
import pygame
import Config_Resource as cr
from py.Tools import Pre as tp
from py.Tools.Items import Pre as tip
#除python第三方包外仅调用Tools层以及Config_Resource

#<---------------------------------------------------------------------------->
#III. GeneralItem类
class GeneralItem(pygame.sprite.Sprite):
    #一般类型的Item对象，继承自sprite
    itemType = 'GeneralItem';                                                   #Item属于的类型#the type of item is generalitem
        
    def __init__(self, name = "Item", location = None, rotatespeed = 0, rotatecenter = None, Movetypes = "S"):
        """
        location is a tuple which has the form: (x, y)
        Movetype is a subset ["S"(Static), "TD"(TrainslationDynamic), "RD"(RotationDynamic)]
        
        Data:
            (inherit from pygame.sprite.Sprite)
            moveimage - Tools_Simple.MoveImage
            display - Tools_Simple.MoveImage
            rotate - Tools_Item.MoveAngle
            move - Tools_Item.MoveSpeed
        
        Methods:
            (inherit from pygame.sprite.Sprite)
            get_RD(self, rotatespeed = 0, rotatecenter = None) - 生成/重设旋转参数
            get_TD(self, speed = (0, 0), addspeed = (0, 0)) - 生成/重设移动参数
            update_speed(self, speed = None, addspeed = None, AngleMode = False, PiMode = False) - 重设移动位移、速度、加速度参数
            update_speed_limit(self, MaxSpeed = None, MaxAddSpeed = None) - 重设移动速度、加速度上限
            update_rotate(self, angle = None, speed = None, addspeed = None) - 重设旋转角度、速度、加速度
            add_speed(self, location = None, speed = None, addspeed = None) - 增加/减少移动位移、速度、加速度参数
            move_to(self, location = None, Vector = False, Center = False) - 强制移动到指定位置/指定位移
            print_location(self) - 打印当前位置(测试用)
            scale_to(self, rate = None, size = None) - 放缩围绕图片几何中心进行, rate为放缩比例, size为放缩后的尺寸, 当rate为数字时size无效
            update(self) - 根据内部信息更新运动数据
            draw(self, SCREEN) - 在窗口Screen上显示物体图像
        """
        pygame.sprite.Sprite.__init__(self);
        
        
        """
        self.mass 为暂定参数，只使用在引力模拟功能上
        """
        # create a surface and move to the positon
        self.moveimage = tip.MoveImage(name);                                   #生成图像并移动至指定位置（默认为屏幕中心）
        self.image = self.moveimage.image;                                      #更新sprite自带image参数，以兼容部分sprite原版操作
        self.itemID = None;                                                     #Item实例在ID_Set中的索引ID, 仅在被存入ID_Set中时被赋值
        
        if tp.is_location_tuple(location): #若输入的location符合格式,则将图像中心移至该处, 否则将图像置于窗口中央
            self.moveimage.move_to(location, Center = True);#if the location is a tuple, then move the image to the location
        else:
            self.moveimage.move_to((cr.W//2, cr.H//2), Center = True);#otherwise,move the image to the middle of the window
        
        try:                                #排除不可迭代对象
            iter(Movetypes);
        except TypeError:
            Movetypes = [Movetypes];
        if type(Movetypes) == str:          #处理单字符串输入
            Movetypes = [Movetypes];
            
        for mode in Movetypes:              #运动模式检测#test the move mode
            if mode in ["RD", "rd", "Rd"]:  #若开启旋转模式，则设置旋转画布与参数  #if open the rotation mode, then set the rotation argument
                self.get_RD(rotatespeed = rotatespeed, rotatecenter = rotatecenter);
                continue;
            if mode in ["TD", "td", "Td"]:  #若开启移动模式，则设置移动参数#if open the move mode, then set the move argument
                self.get_TD();
                continue;
    
    def get_RD(self, rotatespeed = 0, rotatecenter = None):
        #生成/重设旋转参数#set/reset the rotatespeed and rotatecenter
        self.display = self.moveimage;
        self.rotate = tip.MoveAngle(speed = rotatespeed);
        if tp.is_location_tuple(rotatecenter) and rotatecenter != self.moveimage.center:   #若旋转中心不在几何中心，则追加设置 #test if the rotation center is the geometric center
            radius = tp.distance_location_tuple(self.moveimage.center, rotatecenter);#calculate the distance between the geometric center and rotation center
            self.rotate.update_center(rotatecenter, radius);#update the rotation center and radius
    
    def get_TD(self, speed = (0, 0), addspeed = (0, 0)):
        self.move = tip.MoveSpeed(location = self.moveimage.get_vertex(), speed = speed, addspeed = addspeed);#create an object of movespeed
        
    def print_location(self):
        self.moveimage.print_location();#print the location of the image
    
    def scale_to(self, rate = None, size = None):
        #放缩围绕图片几何中心进行, rate为放缩比例, size为放缩后的尺寸, 当rate为数字时size无效
        #Scaling is performed around the geometric center of the image, 
        # rate is the scaling ratio, size is the size after scaling, 
        # and size is invalid when rate is a number
        self.moveimage.scale_to(rate = rate, size = size);
        self.image = self.moveimage.image;
        try:
            self.move.update_speed(location = self.moveimage.get_vertex());#try to update the location
        except AttributeError:
            None;        
        
    def update(self):
        try:                                    #若必要参数有定义，则移动位置
            self.move.update_speed(MI = self.moveimage); #将move的运动信息同步到moveimage（原始图像）上 #update the information of move to the original moveimage
        except AttributeError:
            None;
            
        try:                                    #若必要参数有定义，则旋转显示图像 #update the arguments of the rotation
            self.rotate.update_angle();         #更新旋转参数
            self.display = self.moveimage.copy();     #创建新显示图像     #create a new image
            self.display.move_to(self.rotate.rotate_vector(), Vector=True);   #旋转分解1/2: 移动几何中心#the first step is moving the geometric center
            self.display.rotate(self.rotate.angle);   #旋转分解2/2: 中心旋转   #the second step is rotate the image

        except AttributeError:
            None;
    
    def update_speed(self, speed = None, addspeed = None, AngleMode = False, PiMode = False):
        """
        AngleMode: False - speed & addspeed represent the flat coordinate (x, y)
        AngleMode: True - speed & addspeed represect the angle coordinate (angle, length)
        """
        self.move.update_speed(location = self.move.location.location, speed = speed, addspeed = addspeed, AngleMode = AngleMode, PiMode = PiMode);
    
    def update_speed_limit(self, MaxSpeed = None, MaxAddSpeed = None):
        self.move.update_speed_limit(MaxSpeed = MaxSpeed, MaxAddSpeed = MaxAddSpeed);#update the maxspeed and maxaddspeed
    
    def update_rotate(self, angle = None, speed = None, addspeed = None):
        self.rotate.update_angle(angle = angle, speed = speed, addspeed = addspeed);#update the rotation argument
    
    def update_image(self, name = None, orimage = None):#update the image
        if name == None:    name = self.moveimage.name;
        center = self.moveimage.center;
        size = self.moveimage.rect.size;
        self.moveimage = tip.MoveImage(name, orimage);
        self.moveimage.move_to(location = center, Center=True);
        self.scale_to(size=size);
    
    def add_speed(self, location = None, speed = None, addspeed = None, SkipZero = False):#change the arguments about moving,like location,speed and addspeed
        #SkipZero为True时当self.move中某值为0则使该值发生变化
        #when the skipzero is true,if one of the argument is 0, then assign none to this argument.
        if SkipZero:
            if tp.distance_location_tuple(self.move.location) == 0:  location = None;
            if tp.distance_location_tuple(self.move.speed) == 0: speed = None;
            if tp.distance_location_tuple(self.move.addspeed) == 0: addspeed = None;
        self.move.add_speed(location = location, speed = speed, addspeed = addspeed, MI = self.moveimage);
    
    def add_rotate(self, angle = None, speed = None, addspeed = None, SkipZero = False):
        #SkipZero为True时当self.rotate中某值为0则使该值发生变化
        # when the skipzero is true,if one of the argument is 0, then assign none to this argument.
        if SkipZero:
            if self.rotate.angle == 0:  angle = None;
            if self.rotate.speed == 0: speed = None;
            if self.rotate.addspeed == 0: addspeed = None;
        self.rotate.add_angle(angle = angle, speed = speed, addspeed = addspeed);
    
    def move_to(self, location = None, Vector = False, Center = False):
        #强制移动到指定位置/指定位移
        # move the image to location or move by the offset
        if tp.is_location_tuple(location):
            if Center:  #location表示几何中心时  #where the location is the geometric center of image
                location = (location[0] - self.moveimage.rect.w//2, location[1] - self.moveimage.rect.h//2);
            #this is the location of the topleft
            self.moveimage.move_to(location = location, Vector = Vector);
            try:
                self.move.location.set_from_coordinate(location);
            except AttributeError or NameError:
                None;
            #同步self.move.location与self.moveimage的坐标.
            # Synchronize the coordinates of self.move.location and self.moveimage
    """
    def copy(self):
        #深度复制
    
    def interact_[function name](self, newItem):
        #isinstance(newItem, GeneralItem) == True;
        #提供Item间的交互功能，内部代码自由发挥，但输入应遵循 function(Item)的格式
        #此处仅提供书写格式，具体实现应在各个子类中分别进行
    """
        
    def draw(self, SCREEN, center = None, scale_rate = None, correct = None):
        #center, correct, scale_rate的含义见MoveImage.draw()
        try:#where the display exist, then use the scaling argument
            self.display.draw(SCREEN, center = center, scale_rate = scale_rate, correct = correct); #当存在专门用于显示的display数据(MoveImage)时, 启用放缩参数
        except AttributeError:
            self.moveimage.draw(SCREEN, correct = correct);                                         #不然, 只启用矫正参数#otherwise, only use the modify argument

class SurroundedItem(GeneralItem):
    """
    Data:
        (GeneralItem)
        clouds - pygame.sprite.Group
    Methods:
        __init__
        get_clouds
        update
        draw
    """
    
    itemType = 'SurroundedItem';
    
    def __init__(self, name = cr.default_Planet, location = None, rotatespeed = 0):
        GeneralItem.__init__(self, Movetypes=["RD", "TD"], name = name, location = location, rotatespeed = rotatespeed);
        self.clouds = pygame.sprite.Group();
    
    def get_clouds(self, name = None, HeightRate = 0, RotateSpeed = 0, BeginAngle = 0):
        #HeightRate 为Cloud距离Planet表面的相对高度 (最少\多取 -10 ~ 10)
        #heighrate is the distance between the planet surface and cloud,the range is(-10,10)

        HeightRate = HeightRate % 10 if HeightRate>0 else HeightRate % -10;
        
        try:
            cr.IMAGES[name];#try to get the image from source
        except KeyError:    name = self.moveimage.name+'.Clouds';
        try:
            new_clouds = GeneralItem(name = name, Movetypes=["RD"]);
        except KeyError:
            new_clouds = GeneralItem(name = cr.default_empty, Movetypes=["RD"]);#set the could move type to "RD"
        
        radius = self.moveimage.rect.h//2 + HeightRate * self.moveimage.rect.h//20;
        new_clouds.rotate.update_angle(angle = BeginAngle, speed = RotateSpeed);
        # set the rotation radius,rotation angle,ratation center and speed
        new_clouds.rotate.update_center(center = self.moveimage.center, radius = radius);
        new_clouds.move_to(location = tp.add_location_tuple(self.moveimage.center, (0, -radius)), Center = True);
        #move the cloud to a new location while it is rotating
        self.clouds.add(new_clouds);
    
    def update(self):
        GeneralItem.update(self);
        for item in self.clouds:
            try:
                item.rotate.update_center(center = self.moveimage.center);#update the rotate center
                item.move_to(location = tp.add_location_tuple(self.moveimage.center, (0, -item.rotate.radius)), Center = True);#update the geometric center
            except AttributeError:
                item.move_to(location = self.moveimage.center, Center = True);
            item.update();
    def update_image(self, name = None, orimage = None):#update the cloud image
        GeneralItem.update_image(self, name = name, orimage = orimage);

        for item in self.clouds:
            try:
                item.update_image(name = name+'.Clouds');
            except KeyError: item.update_image(name = item.moveimage.name);

    
    def draw(self,SCREEN, center = None, scale_rate = None, correct = None):#scaling the cloud
        GeneralItem.draw(self, SCREEN, center = center, scale_rate = scale_rate, correct = correct);#use the function in generalitem
        for item in self.clouds:
            item.draw(SCREEN, center = center, scale_rate = scale_rate, correct = correct);