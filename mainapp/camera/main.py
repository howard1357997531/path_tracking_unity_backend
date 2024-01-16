from threading import Thread
from tkinter import W
# from ui import mainUI as mainUI
from camClass import cameraApplications


class MainTH(Thread):
    # def __init__(self, ui):
    #     Thread.__init__(self)
    #     self.ui = ui
    #     self.camRobot = cameraApplications()

    def __init__(self):
        Thread.__init__(self)
        self.camRobot = cameraApplications()

    def run(self):
        while True:
            
            if self.ui.cameraStatus_1:    # Detemine button clicked or not
                self.camRobot.capture()    #Capture Image
                self.ui.openCam_1()


if __name__ == "__main__":
    mainUI = mainUI.Main()
    mainTH = MainTH(mainUI)
    mainTH.start()
    mainUI.show()
