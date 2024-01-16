from threading import Thread
from tkinter import W
from ui import mainUI as mainUI
import numpy as np
import os
from KRLTest import connectObj
import open3d as o3d
from camRobot import cameraRobot

class MainTH(Thread):
    def __init__(self, ui):
        Thread.__init__(self)
        self.ui = ui
        self.camRobot = cameraRobot()
        self.url = "https://threed-object.onrender.com/get_object_3d/"  # Url for get interface data
        self.ip = "192.168.2.100"    # robobt ip
        self.port = 54600           # port


    def run(self):
        while True:
            # When Camera button Clicked
            if self.ui.cameraStatus_1:
                
                os.system(self.camRobot.ethnet_command)     

                self.camRobot.capture()    # Catpure Data
                self.camRobot.save_img(os.path.join(self.camRobot.image_save_path))    # save image
                self.camRobot.save_pc(os.path.join(self.camRobot.ply_save_path))     # save pc
                os.system(self.camRobot.wifi_command)     
                self.ui.openCam_1()

            # When Robot button Clicked.
            if self.ui.moveStatus:
                points = self.camRobot.get_data(self.url)    # connect database

                points = self.camRobot.parse_data(points)
                real_position = self.camRobot.convert2real(points)

                os.system(self.camRobot.ethnet_command)     
                self.camRobot.connect()

                self.camRobot.send_robot_data(real_position)
                self.ui.moveButtonClick()
                
                os.system(self.camRobot.wifi_command)


if __name__ == "__main__":
    mainUI = mainUI.Main()
    mainTH = MainTH(mainUI)
    mainTH.start()
    mainUI.show()
