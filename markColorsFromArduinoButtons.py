"""
    assign mark colors from arduino buttons
    
    This assumes (colored) buttons on the Arduino, whose presses it listens to and assigns mark colors to selected glyphs accordingly.
    It requires the ControlBoard extension to run:
    https://github.com/andyclymer/ControlBoard
    Set up your buttons in ControlBoard, and assign names. This script assumes a naming convention "<color>Button", so "redButton", "blueButton" and so forth, where the color name corresponds to the key in self.markColors below. Specify your exact mark colors there.
    Nina Stössinger 10.3.15
"""

import vanilla
from mojo.events import addObserver, removeObserver
from mojo.roboFont import OpenWindow

class markButtons:    
    def __init__(self):
        addObserver(self, "controlBoardCallback", "ControlBoardInput")
        self.w = vanilla.Window((200, 20), "Arduino Listener")
        self.w.bind("close", self.windowClosed)
        self.w.open()
        
        # assign exact mark colors to the individual color buttons here.
        # these should probably correspond to the color values you use in RoboFont.
        # The key needs to correspond to the button name that belongs to it (= "<key>Button")
        self.markColors = {
            "green": (0.7311, 1.0, 0.1645, 1.0),
            "red": (0.8936, 0.0, 0.2533, 1.0),
            "yellow": (1.0, 0.8579, 0.0535, 1.0),
            "blue": (0.287, 0.5264, 1.0, 1.0),
            "white": None,
            }
         
    def windowClosed(self, sender):
        removeObserver(self, "ControlBoardInput")
        
    def controlBoardCallback(self, info):
        if info["state"] == "down":
            colorName = info["name"][:-6]
            self.updateMarkColor(colorName)
                
    def updateMarkColor(self, cname):
        f = CurrentFont()
        if f:
            if len(f.selection) > 0:
                for gn in f.selection:
                    try:
                        f[gn].mark = self.markColors[cname]
                    except IndexError:
                        pass
    
OpenWindow(markButtons)
