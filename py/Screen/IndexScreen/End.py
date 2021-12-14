# Modified IndexScreen for Control.EndIndexScreen
# Only rewrite the restart method
from py.Screen.IndexScreen import Basic as sib

class EndIndexScreen(sib.IndexScreen):
    def restart(self):
        self.change_bgp();