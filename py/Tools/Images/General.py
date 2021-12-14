#Tools for image
#除python第三方包外仅调用Tools层以及Config_Resource
import pygame
import numpy as np
import Config_Resource as cr
from py.Tools import Pre as tp
from py.Tools.Indicator import Indicator

class MoveImage():
    #包含一个pygame.Surface类型变量及其常用位置参数
    # this contains a pygame.Surface type variable and its position arguments.
    #并含有移动、原地旋转、复制等简单操作函数
    # and it also contains some simple functions like move,rotate and copy etc.
    """
    Data:
        image - pygame.Surface
        rect - pygame.rect.Rect
        center - tuple (location)
        name
    Function:
        __init__
        __str__
        move_to
        rotate
        scale_to
        get_vetex
        copy
        draw
    """
    def __init__(self, name = "Item", orimage = None):
        if isinstance(orimage, pygame.Surface):#if the input orimage is a surface, then assign it to self.image
            self.image = orimage.copy();
        else:
            self.image = cr.IMAGES[name].copy();#copy the orimage and assign it to self.image
        self.name = name;                           #使用的图片名use the name of picture
        #self.ID 可能可以用于区分各个图片的标签
        self.rect = self.image.get_rect();    # use the rect
        self.center = self.rect.center;       #rect的几何中心（类型为tuple, 不会随rect变化而自动更新）
        # assign the centre location to the self.center(the type is tuple and it could not change with rect)
    
    def __str__(self):
        return f"name: {self.name}\nlocation = ({self.rect.x}, {self.rect.y})\ncenter = ({self.center})\n"
        # return the information about the name, the location and the centre
    def move_to(self, location = (0, 0), Vector = False, Center = False):
        """
        Vector: False - move to the given location
        Vector: True - move by the given vector
        """
        if not tp.is_location_tuple(location):
            return;#test if the location is a tuple
            
        if Vector:
            self.rect.move_ip(location);#move by the given offset
        elif Center:
            self.rect = self.image.get_rect(center = location);#create a new at the location
        else:
            self.rect.update(location, self.rect.size);    #move to the given location 
        self.center = self.rect.center;                 #更新几何中心#update the centre of the image
    
    def rotate(self, angle = 0, PiMode = False):
        """
        PiMode: False - angle is expressed without pi
        PiMode: True - angle is expressed by pi
        """
        if PiMode:
            angle = angle * 180 / np.pi;
        
        self.image = pygame.transform.rotate(self.image, angle);#rotate the image with angle
        self.rect = self.image.get_rect(center = self.center);#get the new rect of the image
    
    def scale_to(self, rate = None, size = None):
        #放缩围绕图片几何中心进行, rate为放缩比例, size为放缩后的尺寸, 当rate为数字时size无效
        if tp.is_number(rate):#change the size according to the scaling rate
            size = tp.dot_tuple(self.image.get_size(), rate);
            
        if tp.is_location_tuple(size):
            self.image = pygame.transform.scale(self.image, size);#scale the image according to the size
            self.rect = self.image.get_rect(center = self.center);#create a new rectangle at the some position
    
    def get_vertex(self):
        #返回左上角顶点的坐标#return the topleft point location of the rectangle.
        return self.rect.topleft;
    
    def get_center(self):#return the center location of the position
        return self.rect.center;
    
    def copy(self):#copy a new surface and put it into original place, then return it
        new_Mimage = MoveImage(orimage=self.image.copy());
        new_Mimage.move_to((self.rect.x, self.rect.y));
        return new_Mimage;
    
    def draw(self, SCREEN, center = None, scale_rate = None, correct = None):
        """图像带移动的缩放"""
        #center, correct是元素为数字的二元组, scale_rate是数字
        #只有当缩放中心center与缩放率scale_rate同时有意义, 才会进行缩放
        """scaling to image"""
        # center, correct are tuples with two arguments, scale_rate is a number
        # only if both center and scale_rate make sense, then the function works
        if tp.is_location_tuple(center) and tp.is_number(scale_rate):
            vect = tp.minus_location_tuple(center, self.center);
            vect = tp.dot_tuple(vect, 1 - scale_rate);
            self.move_to(vect, Vector=True);            #将中心移动到缩放后的中心#move the image to the scaling centre
            self.scale_to(rate = scale_rate);           #原地缩放#scale the image and remain the same position
            
        """图像位置矫正"""
        """modify the location of the image"""
        if tp.is_location_tuple(correct):               #根据矫正向量correct将图像位置坐标变换为显示的相对坐标
                                                        # #according to the correct vector change the image location
            self.rect.move_ip(correct);
        
        SCREEN.blit(self.image, self.rect);


class InteractImage(MoveImage, Indicator):
    #在MoveImage的基础上拓展交互接口, 新增辨识ID以及指令映射表
    # Expand the interactive interface on the basis of MoveImage, add identification ID and instruction mapping table
    """
    Data:
        (Tools_Image.MoveImage)
        (Indicator)
    Function:
        (Tools_Image.MoveImage)
        (Indicator)
        __init__
        __str__
    """
    def __init__(self, name = "Item", orimage = None, Command_ID = None):
        MoveImage.__init__(self, name = name, orimage = orimage);
        Indicator.__init__(self, Command_ID = Command_ID);
    
    def __str__(self):
        return MoveImage.__str__(self) + Indicator.__str__(self);