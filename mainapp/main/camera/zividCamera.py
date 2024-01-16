import time
import yaml
import zivid
import datetime
import os
import cv2

# update in 2022/05/09
class zividCamera:
    def __init__(self):
        # init setting
        app = zivid.Application()
        camera = app.connect_camera()

        print("Configuring 2D settings")
        # 2D camera setting
        settings_2d = zivid.Settings2D()
        settings_2d.acquisitions.append(zivid.Settings2D.Acquisition())

        # settings_2d.exposure_time = 0.2
        self.settings_2d = settings_2d

        # 3D camera setting
        settings_file = "auto3d.yml"
        self.settings = zivid.Settings.load(settings_file)

        # Saving Path
        save_path = "data"
        self.save = False

        self.ply_save_path = os.path.join(save_path, "ply")
        self.image_save_path = os.path.join(save_path, 'image')
        

        os.makedirs(save_path, exist_ok=True)
        os.makedirs(self.ply_save_path, exist_ok=True)
        os.makedirs(self.image_save_path, exist_ok= True)
        print(self.ply_save_path)

        self.device = camera

    def openCamera(self):
        try:
            self.get_capture()
            self.cameraStatus = True
        except Exception as e:
            print(f"open camera error with {e}")
            self.cameraStatus = False

    def closeCamera(self):
        try:
            self.device.disconnect()
            self.cameraStatus = False
        except:
            print("close camera error")
            raise

    def get_capture(self):
        frame_2d = self.device.capture(self.settings_2d)
        frame = self.device.capture(self.settings) 
        print("Capture Finish")
        return frame_2d, frame



    def loadSetting(self):
        pass

    def getData(self):
        # while True:
            if self.cameraStatus:
                startTime = time.time()
                frame_2d, frame = self.get_capture()
                image = frame_2d.image_bgra()
                colors = image.copy_data()[:,:, :3]

                endTime = time.time() - startTime
                # yield [colors, pointCloudData, endTime]
                yield [colors, frame, endTime]

            else:
                yield []
