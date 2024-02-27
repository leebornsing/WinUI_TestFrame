import os

from config_lib.App_UI_Base import App_UI_Base
from config_lib import operation_base
ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
class Draw_Relationship_Base_Tree(App_UI_Base):
    def __init__(self, confidence=0.8, duration=0.2, interval=0.3):
        super().__init__(confidence=confidence, duration=duration, interval=interval)

    def Draw_relationship_tree(self):
        self.Windows_relationship_tree()
        self.MenuTools_relationship_tree()
        self.MainMenu_relationship_tree()
        self.Canvas_relationship_tree()

    def Windows_relationship_tree(self):
        Windows_InputButtons = os.path.join(ROOT_PATH, "config_png/mspaint_App/Windows/Windows_InputButtons.png")
        self.Windows_InputButtons = self.create_relationship_tree(Windows_InputButtons)

        Windows_FileNameN = os.path.join(ROOT_PATH, "config_png/mspaint_App/Windows/Windows_FileNameN.png")
        self.Windows_FileNameN = self.create_relationship_tree(Windows_FileNameN, operation=operation_base.click)

        Windows_OpenO = os.path.join(ROOT_PATH, "config_png/mspaint_App/Windows/Windows_OpenO.png")
        self.Windows_OpenO = self.create_relationship_tree(Windows_OpenO, operation=operation_base.click)

        Windows_SaveS = os.path.join(ROOT_PATH, "config_png/mspaint_App/Windows/Windows_SaveS.png")
        self.Windows_SaveS = self.create_relationship_tree(Windows_SaveS, operation=operation_base.click)

    def MainMenu_relationship_tree(self):
        MainMenu_SaveWindows = os.path.join(ROOT_PATH, "config_png/mspaint_App/MainMenu/MainMenu_SaveWindows.png")
        self.MainMenu_SaveWindows = self.create_relationship_tree(MainMenu_SaveWindows)

    def MenuTools_relationship_tree(self):
        self.Shape_relationship_tree()
        self.Graphics_relationship_tree()

    def Shape_relationship_tree(self):
        Shape_Hexagram = os.path.join(ROOT_PATH, "config_png/mspaint_App/MenuTools/Shape/Shape_Hexagram.png")
        self.Shape_Hexagram = self.create_relationship_tree(Shape_Hexagram, operation=operation_base.click)

        Shape_Rectangle = os.path.join(ROOT_PATH, "config_png/mspaint_App/MenuTools/Shape/Shape_Rectangle.png")
        self.Shape_Rectangle = self.create_relationship_tree(Shape_Rectangle, operation=operation_base.click)

        Shape_StraightLine = os.path.join(ROOT_PATH, "config_png/mspaint_App/MenuTools/Shape/Shape_StraightLine.png")
        self.Shape_StraightLine = self.create_relationship_tree(Shape_StraightLine, operation=operation_base.click)

        Shape_Shape = os.path.join(ROOT_PATH, "config_png/mspaint_App/MenuTools/Shape/Shape_Shape.png")
        self.Shape_Shape = self.create_relationship_tree(Shape_Shape)

        Shape_StraightLined = os.path.join(ROOT_PATH, "config_png/mspaint_App/MenuTools/Shape/Shape_StraightLined.png")
        self.Shape_StraightLined = self.create_relationship_tree(Shape_StraightLined)

    def Graphics_relationship_tree(self):
        Graphics_Rotate = os.path.join(ROOT_PATH, "config_png/mspaint_App/MenuTools/Graphics/Graphics_Rotate.png")
        self.Graphics_Rotate = self.create_relationship_tree(Graphics_Rotate)

        Graphics_Graphics = os.path.join(ROOT_PATH, "config_png/mspaint_App/MenuTools/Graphics/Graphics_Graphics.png")
        self.Graphics_Graphics = self.create_relationship_tree(Graphics_Graphics)

        Graphics_SelectOperation = os.path.join(ROOT_PATH, "config_png/mspaint_App/MenuTools/Graphics/Graphics_SelectOperation.png")
        self.Graphics_SelectOperation = self.create_relationship_tree(Graphics_SelectOperation)

        Graphics_SelectAll = os.path.join(ROOT_PATH, "config_png/mspaint_App/MenuTools/Graphics/Graphics_SelectAll.png")
        self.Graphics_SelectAll = self.create_relationship_tree(Graphics_SelectAll, operation=operation_base.click)

    def Canvas_relationship_tree(self):
        Canvas_SelectAll = os.path.join(ROOT_PATH, "config_png/mspaint_App/Canvas/Canvas_SelectAll.png")
        self.Canvas_SelectAll = self.create_relationship_tree(Canvas_SelectAll, operation=operation_base.click)

        Canvas_Copy = os.path.join(ROOT_PATH, "config_png/mspaint_App/Canvas/Canvas_Copy.png")
        self.Canvas_Copy = self.create_relationship_tree(Canvas_Copy, operation=operation_base.click)
