#Preporation (Simple tools)
import numpy as np
#仅调用python第三方包
#only import python third-party package
#<---------------------------------------------------------------------------->
#I. 小型功能函数，不依赖下方的类
#I. this is a small function and didn't depend on the class below
def is_number(nu):#test if the nu is a number.
    return type(nu) in [int, float, np.float64];

def is_numberizable(tu = None):
    """
    Test if all the inputted parameter contains are number value.
    """
    if tu == None:                  #排除None输入#Exclude None input
        return False
    
    try:
        if type(tu) in [int, float, np.float64]:
            return True             #确认数值型输入#Confirm numeric input
        
        for item in tu:
            if not is_number(item):
                return False        #排除非数值型输入# Exclude non-numeric input
        return True                 #确认全部数值型输入#if all the arguments in tu is numeric,then return true
    except IndexError or ValueError or TypeError:
        return False                #排除无法被处理的输入#excllude the non-numeric number

def is_location_tuple(tu = None):#test if the tu is a tuple with two numeric arguments
    if type(tu) == tuple and len(tu) == 2 and is_numberizable(tu):
        return True;
    return False;

def add_location_tuple(tu = None, at = None):#add the location tu with the vector at
    if is_location_tuple(tu) and is_location_tuple(at):
        return (tu[0]+at[0], tu[1]+at[1]);

def minus_location_tuple(tu = None, mt = None):#minus the location tu with the vector mt
    if is_location_tuple(tu) and is_location_tuple(mt):
        return (tu[0]-mt[0], tu[1]-mt[1]);

def distance_location_tuple(tu = None, at = None):#calculate the distance between two points
    if is_location_tuple(tu):
        if is_location_tuple(at):
            return np.sqrt((tu[0]-at[0])**2+(tu[1]-at[1])**2)
        else:
            return np.sqrt((tu[0])**2+(tu[1])**2)
    return 0;

def dot_tuple(tu = None, c = 1):#plus the vector with the variable c
    if is_location_tuple(tu) and is_numberizable(c):
        if c == 1:
            return tu;
        return (c * tu[0], c * tu[1])

def get_angle(tu):
    #根据向量大小取与y轴负方向的夹角, 以逆时针为正方向
    # According to the magnitude of the vector, take the angle with the negative direction of the y-axis, and take counterclockwise as the positive direction
    #返回值为度数(取值(-180~180)不含pi)
    if not is_location_tuple(tu):
        return;
    
    #处理0值情况
    #consider the situation when y==0
    x, y = tu;
    if x == 0 and y == 0:
        return;
    
    if y == 0:
        return 90 if x < 0 else -90;
    
    if y < 0:
        #不需要修正反三角函数
        return np.arctan(x/y) * 180 / np.pi;
    else:
        #需要修正反三角函数
        return 180 + np.arctan(x/y) * 180 / np.pi;
        
    
    