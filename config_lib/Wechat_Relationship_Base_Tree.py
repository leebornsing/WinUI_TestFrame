import os

from config_lib.App_UI_Base import App_UI_Base
from config_lib import operation_base
ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
class Wechat_Relationship_Base_Tree(App_UI_Base):
    def __init__(self, confidence=0.8, duration=0.2, interval=0.3):
        super().__init__(confidence=confidence, duration=duration, interval=interval)

    def Wechat_relationship_tree(self):
        self.Windows_relationship_tree()
        self.MainMenu_relationship_tree()

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
        Chat_SearchUserBox = os.path.join(ROOT_PATH, "config_png/Wechat/Chat/Chat_SearchUserBox.png")
        self.Chat_SearchUserBox = self.create_relationship_tree(Chat_SearchUserBox)

        Chat_SendButton = os.path.join(ROOT_PATH, "config_png/Wechat/Chat/Chat_SendButton.png")
        self.Chat_SendButton = self.create_relationship_tree(Chat_SendButton)