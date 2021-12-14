#Preparation for item
import numpy as np
import Config_Resource as cr
from py.Tools import Pre as tp
from py.Tools.Images.General import MoveImage
#除python第三方包外仅调用Tools层以及Config_Resource

#<---------------------------------------------------------------------------->
#II. 小型自定义类, 含有可自定义的运算函数
class MovePoint():
    #以tuple形式储存二元数字对（可为平面坐标或向量）, 提供简单向量运算
    # Store binary number pairs in tuple form (could be plane coordinates or vectors), provide simple vector operations
    def __init__(self, center = None, x = None, y = None, angle = None, length = None, PiMode = False):
        if tp.is_location_tuple(center):#use the centre tuple to set the location.
            self.set_from_coordinate(center);
        elif tp.is_location_tuple((x, y)):#use the x,y to set the location
            self.set_from_coordinate((x, y));
        elif tp.is_numberizable(angle) and tp.is_numberizable(length):#set the polar coordinate with the angle and length
            self.set_from_angle(angle = angle, length = length, PiMode = PiMode);
        else:
            self.set_from_coordinate();#set the location (0,0)
    
    def print_contains(self):#print the point location,length,direction
        print(f"location = ({self.location[0]}, {self.location[1]}), length = {self.length}\ndirection = {self.angle} or {self.pi_angle} (pi-scale)")
            
    def set_from_coordinate(self, center = None):     #根据平面坐标生成数据
        if tp.is_location_tuple(center):
            self.location = center;
            self.length = self.distance((0, 0)); #计算作为向量时的二范数#when the tuple is a vector, calculate its 2-Norm
        else:
            self.location = (0, 0);
            self.length = 0;
        
        if self.location[0] == 0:       #计算location作为向量与x轴正方向的夹角（逆时针为正方向）#calculate the angle between vector and the positive direction of x-axis
            self.pi_angle = -np.pi if self.location[1] > 0 else np.pi
        else:
            self.pi_angle = -np.arctan(self.location[1]/self.location[0]);
        
        self.angle = self.pi_angle * 180 / np.pi;
        
    def set_from_angle(self, angle = 0, length = 0, PiMode = False):    #根据角坐标生成数据#Generate data based on polar coordinates
        if tp.is_numberizable(angle):#turn the input into angle or pi_angle
            self.angle = angle * 180 / np.pi if PiMode else angle;
            self.pi_angle = angle if PiMode else angle * np.pi / 180;
        else:
            self.angle = self.pi_angle = 0;
        
        self.length = length if tp.is_numberizable(length) else 0;
        
        self.location = (self.length * np.cos(self.pi_angle), -self.length * np.sin(self.pi_angle));
        # use the length and angle to caculate the location
    def get_coordinate(self):#get the location
        return self.location;        
    
    def get_angle(self):#get the angle
        return (self.length, self.angle, self.pi_angle);
    
    def show(self):#print the location, angle and length data
        print(f"x = {self.location[0]}, y = {self.location[1]}\n angle = {self.angle} or {self.pi_angle} (pi-scale), length = {self.length}");
        
    def add(self, mv):
        #接受MovePoint或者坐标tuple为输入 #accept MovePoint or tuple as a input
        if isinstance(mv, MovePoint):
            self.set_from_coordinate(center = (self.location[0] + mv.location[0], self.location[1] + mv.location[1]));
        if tp.is_location_tuple(mv):
            self.set_from_coordinate(center = (self.location[0] + mv[0], self.location[1] + mv[1]));
    
    def negative(self):
        self.set_from_coordinate((-self.location[0], -self.location[1]));
    
    def limit(self, limit):#limit the length and make sure it would not out of the range
        if tp.is_numberizable(limit) and self.length > 0:
            if self.length >limit:
                self.location = tp.dot_tuple(self.location, limit/self.length);
                self.length = limit;
    
    def distance(self, np):
        #接受MovePoint或者坐标tuple为输入#accept MovePoint or tuple as a input
        if isinstance(np, MovePoint):
            return self.tp.distance_location_tuple(self.location, np.location);
        return tp.distance_location_tuple(self.location, np);#calculate the distance between the location of object and input

class MoveSpeed():
    #移动必需参数之集合: 速度、加速度, 更新函数
    # A collection of necessary parameters for movement: speed, acceleration, update function
    def __init__(self, location = (0, 0), speed = (0, 0), addspeed = (0, 0), MaxSpeed = None, MaxAddSpeed = None, AngleMode = False, PiMode = False):
        """
        AngleMode: False - speed & addspeed represent the flat coordinate (x, y)
        AngleMode: True - speed & addspeed represect the angle coordinate (angle, length)
        PiMode: False - accept angle with normal-scale
        PiMode: True - accept angle with pi-scale
        """
        #注意，长度参数应除以FPS
        if AngleMode:#speed and addspeed represect the angle coordinate (angle, length)
            self.location = MovePoint(angle = location[0], length = speed[1], PiMode = PiMode) if tp.is_location_tuple(location) else MovePoint();
            self.speed = MovePoint(angle = speed[0], length = speed[1] / cr.FPS, PiMode = PiMode) if tp.is_location_tuple(speed) else MovePoint();
            self.addspeed = MovePoint(angle = addspeed[0], length = addspeed[1] / cr.FPS, PiMode = PiMode) if tp.is_location_tuple(addspeed) else MovePoint();
        else:#speed and addspeed represent the flat coordinate (x, y)
            self.location = MovePoint(center = location) if tp.is_location_tuple(location) else MovePoint();
            self.speed = MovePoint(center = tp.dot_tuple(speed,1/cr.FPS)) if tp.is_location_tuple(speed) else MovePoint();
            self.addspeed = MovePoint(center = tp.dot_tuple(addspeed,1/cr.FPS)) if tp.is_location_tuple(addspeed) else MovePoint();
        
        self.maxspeed = MaxSpeed;
        self.maxaddspeed = MaxAddSpeed;
        # set the maxspeed and maxaddspeed
    def print_contains(self):
        print("location:")
        self.location.print_contains();
        print("speed:")
        self.speed.print_contains();
        print("addspeed:")
        self.addspeed.print_contains();
    
    def update_speed_limit(self, MaxSpeed = None, MaxAddSpeed = None):#update the maxspeed and maxaddspeed
        self.maxspeed = MaxSpeed;
        self.maxaddspeed = MaxAddSpeed;
    
    def update_speed(self, location = None, speed = None, addspeed = None, MI = None, AngleMode = False, PiMode = False):
        if tp.is_location_tuple(addspeed):#update the addspeed with the addspeed/cr.FPS
            if AngleMode:
                self.addspeed.set_from_angle(angle = addspeed[0], length = addspeed[1]/cr.FPS, PiMode = PiMode)
            else:
                self.addspeed.set_from_coordinate(tp.dot_tuple(addspeed,1/cr.FPS));
        if type(self.maxaddspeed) in [int, float]:
            self.addspeed.limit(self.maxaddspeed);
            # if the maxaddspeed has been set, then modify the current addspeed.
        if tp.is_location_tuple(speed):#update the speed with speed/cr.FPS
            if AngleMode:
                self.speed.set_from_angle(angle = speed[0], length = speed[1]/cr.FPS, PiMode = PiMode);
            else:
                self.speed.set_from_coordinate(tp.dot_tuple(speed,1/cr.FPS));
        else:#update the speed by adding the addspeed
            self.speed.add(self.addspeed);
        if type(self.maxspeed) in [int, float]:#if the maxspeed has been set,then modify the current speed
            self.speed.limit(self.maxspeed);
        
        if tp.is_location_tuple(location):#update the location with the input
            if AngleMode:
                self.location.set_from_angle(angle = location[0], length = location[1], PiMode = PiMode);
            else:
                self.location.set_from_coordinate(location);
        else:#if the location is none, then update it by the speed
            self.location.add(self.speed);
        
        if isinstance(MI, MoveImage):                       #rect.x, y只能为整数值，因此直接将速度叠加的话会产生显著的舍入误差，使得位移与速度不匹配, 因此只能另添加一对浮点数来储存位置值，并通过同步更新将浮点数与rect绑定
            MI.move_to(location = (round(self.location.location[0]), round(self.location.location[1])))
    
    def add_speed(self, location = None, speed = None, addspeed = None, MI = None):
        self.location.add(location);
        self.speed.add(tp.dot_tuple(speed,1/cr.FPS));
        self.addspeed.add(tp.dot_tuple(addspeed,1/cr.FPS));
        
        if isinstance(MI, MoveImage):                       #rect.x, y只能为整数值，因此直接将速度叠加的话会产生显著的舍入误差，使得位移与速度不匹配, 因此只能另添加一对浮点数来储存位置值，并通过同步更新将浮点数与rect绑定
            MI.move_to(location = (round(self.location.location[0]), round(self.location.location[1])))
        # rect x,y only could be integer, so add the speed directly will result in significant error, then the speed would not match move.
        # so add another pair of float to store the location, and match the rect by updating.
class MoveAngle():
    #旋转必需参数之集合: 角、角速度、角加速度、旋转中心、旋转半径, 更新、换算函数
    def __init__(self, angle = 0, speed = 0, addspeed = 0, center = None, radius = None):
        self.reset(angle = angle, speed = speed, addspeed = addspeed, center = center, radius = radius);
    
    def reset(self, angle = 0, speed = 0, addspeed = 0, center = None, radius = None):
        #重设参数        #reset the arguments of angle, speed and addspeed, center, radius
        self.angle = angle;
        self.pi_angle = self.angle * np.pi / 180;
        self.speed = speed / cr.FPS;
        self.addspeed = addspeed / cr.FPS;
        if tp.is_location_tuple(center):#reset the center and radius
            self.center = center;
            self.radius = abs(radius) if tp.is_numberizable(radius) else 1;
    
    def print_contains(self, ShowCenter = False):#print the angle,speed,addspeed and also the center and radius if needed
        print(f"algle = {self.angle}, speed = {self.speed}, addspeed = {self.addspeed}");
        if ShowCenter:
            print(f"center = ({self.center[0]}, {self.center[1]}), radius = {self.radius}");
    
    def add_angle(self, angle = None, speed = None, addspeed = None):
        if tp.is_number(addspeed):
            self.addspeed += addspeed / cr.FPS;
            
        if tp.is_number(speed):
            self.speed += speed / cr.FPS;
        
        if tp.is_number(angle):
            self.angle += angle;
            self.bound_angle();
    
    def bound_angle(self):
        #限定self.angle取值在(-180, 180)#the value of self.angle must be in the range of (-180,180)
        while self.angle>180:
            self.angle-=360;
        while self.angle<-180:
            self.angle+=360;
        self.pi_angle = self.angle * np.pi / 180;
    
    def update_radius(self, radius = None):
        #更新旋转半径#update the rotation radium
        if tp.is_numberizable(radius):
            self.radius = abs(radius);
    
    def update_center(self, center = None, radius = None):
        #更新旋转中心与旋转半径#update the rotation center and radium
        self.update_radius(radius);
        if tp.is_location_tuple(center):
            self.center = center;
    
    def update_angle(self, angle = None, speed = None, addspeed = None):
        #更新角速度等参数
        if tp.is_number(addspeed):
            self.addspeed = addspeed / cr.FPS;#update the addspeed
            
        if tp.is_number(speed):#update the speed according to input,if input is none,then add speed with addspeed.
            self.speed = speed / cr.FPS;
        else:
            self.speed += self.addspeed;
        
        if tp.is_number(angle):#update the angle according to input,if input is none, then add angle with speed
            self.angle = angle;
        else:
            self.angle += self.speed;
            self.bound_angle();
    
    def rotate_vector(self):
        """
        Calculate the equivalent vector that the geometrical center of the image should move in a rotation.
        The original geom-center is directly above the rotation center (-y direction).
        """
        #计算造成按参数旋转后image几何中心移动结果的等效向量. 原始几何中心规定在旋转中心正上方(-y方向)
        try:
            return (round(-self.radius * np.sin(self.pi_angle)), round(self.radius * (1 - np.cos(self.pi_angle))))
        except AttributeError:
            return (0, 0)

class ItemValue():
    #用于记录Planet中质量与温度值的数据结构#use to record the temperature and mass of the planet
    def __init__(self, value = None, devalue = None, bound = None, cate_break = None):
        #value为存储数值
        #devalue为update时value的变化值
        #bound为value边界, 取None时意味无上/下界, 否则其中的值应按升序排列
        #cate_break为对value作分类时的临界值, 其中的值应按升序排列
        # value is the stored data
        # devalue is the change of value after each update
        # bound is the range of the value, if the bound is none,then there is no upper bound or lower bound.
        # cate_break is the critical value when categorizing value, and the values should be arranged in ascending order
        self.value = value if tp.is_number(value) else 0;
        self.devalue = devalue/cr.FPS if tp.is_number(devalue) else 0;
        self.bound = bound if tp.is_location_tuple(bound) else (None, None);
        self.cate_break = cate_break if tp.is_numberizable(cate_break) else None;
    
    def __repr__(self):
        return f"Value = {self.value}, Devalue = {self.devalue}\nBound = {self.bound}\nBreaks = {self.cate_break}"
        # in order to print the value,devalue,cate-break and bound
    def add(self, value = None, devalue = None):
        if tp.is_number(value):
            self.value += value;
        if tp.is_number(devalue):
            self.devalue += devalue/cr.FPS;
        # set the value and devalue
        self.bound_value();
    
    def bound_value(self):#modify the value if the value out of the range
        if tp.is_location_tuple(self.bound):
            if self.value < self.bound[0]:
                self.value = self.bound[0];
            if self.value > self.bound[1]:
                self.value = self.bound[1];
    
    def categorize(self):#categorize the value according to the given cate_break
        try:
            iter(self.cate_break);
        except TypeError:   return;
        for i in range(len(self.cate_break)):
            if self.value <= self.cate_break[i]:    return i;#if the value is less than the cate_break[i],then return i
        return len(self.cate_break);
    
    
    def draw(self,SCREEN, location = None, col = None):
        #在界面上可视化显示数据
        #self.value的大小决定了显示的样貌
        # Visually display data on the interface
        # The size of self.value determines the appearance of the display
        """
        ......
        """
        pass;
    
    def get_log_value(self, y_min, y_max):
        #建立函数模型y= a * log10(x+1) + c, 取x = self.value, 返回对应的y值
        #注意, 输入的y_min, y_max分别为函数在x = 0 与x = self.bound[1]处的取值
        # build the function y= a * log10(x+1) + c, let x = self.value, and return the y
        # y_min, y_max分别为函数在x = 0 与x = self.bound[1]处的取值
        # the y_min is the value where x=0, and y_max is the value where x=self.bound[1]
        if not tp.is_numberizable((y_min, y_max, self.value)) or self.value < 0:
            return;
        if not tp.is_number(self.bound[1]):
            return (y_min + y_max)/2;
        
        a = (y_max - y_min)/np.log10(self.bound[1] + 1);
        return a * np.log10(self.value + 1) + y_min;
    
    def get_qmodel_value(self, c):
        #建立函数模型y= - a * x^2 + c, 取x = self.value, 返回对应的y值
        #注意, 输入参数c 即为函数参数c, 并规定函数在self.bound上界处取0(若上界存在)
        # the input argument c is the c of the function.if the upper bound exist,then let y=0 where x reach upper bound.
        if not tp.is_location_tuple((c, self.value)):
            return;
        if not tp.is_number(self.bound[1]):
            return c;
        
        a = c / self.bound[1] ** 2;
        return - a * self.value ** 2 + c;
    
    def get_lmodel_value(self, c):
        #建立函数模型y= - a * log10(x+1) + c, 取x = self.value, 返回对应的y值
        #注意, 输入参数c 即为函数参数c, 并规定函数在self.bound上界处取0(若上界存在)
        # the input argument c is the c of the function.if the upper bound exist,then let y=0 where x reach upper bound.
        if not tp.is_location_tuple((c, self.value)) or self.value < 0:
            return;
        if not tp.is_number(self.bound[1]) or self.bound[1] <= 1:
            return c;
        
        a = c/np.log10(self.bound[1] + 1);
        return - a * np.log10(self.value + 1) + c;
    
    def get_qlmodel_value(self,c):
        #建立函数模型y= - a * (log10(x+1))^2 + c, 取x = self.value, 返回对应的y值
        #注意, 输入参数c 即为函数参数c, 并规定函数在self.bound上界处取0(若上界存在)
        #build the function model y= - a * (log10(x+1))^2 + c, x is self.value, and then return the y

        #the input argument c is the c of the function.if the upper bound exist,then let y=0 where x reach upper bound.
        if not tp.is_location_tuple((c, self.value)) or self.value < 0:
            return;
        if not tp.is_number(self.bound[1]) or self.bound[1] <= 1:
            return c;
        
        a = c/np.log10(self.bound[1] + 1) ** 2;
        return - a * np.log10(self.value + 1) ** 2 + c;
        
    """
    def get......
    """
    
    def update(self, value = None, devalue = None):
        if tp.is_number(devalue):
            self.devalue = devalue/cr.FPS;
        #devalue is the change of the value after update
        if tp.is_number(value):
            self.value = value;#if the value change, then update the value
        else:
            self.value += self.devalue;#if the input value is none, then change it with devalue
        
        self.bound_value();
        
        