# __init__.py in Screen
# Camera下的文件除python第三方包外仅调用Tools, Item, Camera层以及Config_Resource
# Except for the third-party packages of Python, this file only uses Tools, Item and Camera folders and Config_Resource.
from py.Screen.Basic import ID_Set, SubScreen, WinScreen, get_score_image
__all__ = ['Basic', 'IndexScreen', 'PlanetScreen'];