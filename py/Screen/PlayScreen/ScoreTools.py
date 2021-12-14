# Score Image
import pygame
import py.Tools.Pre as tp
from py.Tools.Images import InteractImage
from py.Screen.Basic import get_score_image

class ScoreImage(InteractImage):
    # A child of py.Tools.Images.General.InteractImage
    # Store a number as self.score and will translated the number in to a image
    # Use self.update_score() method to update the stored value
    def __init__(self, score = None, maxdigit = None, Command_ID = None, location = None, Center = False):
        if not tp.is_location_tuple(location):
            location = pygame.display.get_surface().get_rect().center;
        
        if type(score) == int:
            self.score = score if score > 0 else 0;
        else:   self.score = 0;
        self.maxdigit = maxdigit;
        
        oriscore = get_score_image(self.score, maxdigit = self.maxdigit);
        InteractImage.__init__(self, orimage = oriscore, Command_ID = Command_ID);
        self.move_to(location, Center = Center);
    
    def update_score(self, newscore = None, KeepCenter = True):
        # 更新分数并重新生成图片
        # Update scores and regenerate images.
        # newscore give the new self.score value
        # KeepCenter decides the updated images position:
            # If KeepCenter == True, the updated images will keep the center position
            # If KeepCenter == False, the updated images will keep the topleft position
        # Citation: inspired by: https://github.com/Meisterla/flappy_bird/blob/main/main.py
        if type(newscore) != int:
            return;
        self.score = newscore if newscore > 0 else 0;
        
        location = self.rect.center if KeepCenter else self.rect.topleft;
        
        oriscore = get_score_image(self.score, maxdigit = self.maxdigit);
        InteractImage.__init__(self, orimage = oriscore, Command_ID = self.Command_ID);
        self.move_to(location, Center = KeepCenter);
    