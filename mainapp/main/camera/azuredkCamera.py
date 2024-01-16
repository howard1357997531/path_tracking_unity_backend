import pyk4a
from pyk4a import Config, PyK4A
import time
import yaml
import logging
import os

# update in 2022/05/09
class azureDK:
    def __init__(self):
        # init setting
        self.camera = "Kinect"

        camConfig = self.loadSetting()
        self.parser_basic_config(camConfig)
        self.parser_external_config(camConfig)

        self.config = Config(
            color_resolution=self.resoulution,
            camera_fps=self.fps,
            depth_mode=self.depthMode,
            synchronized_images_only=True,
            color_format=self.colorFormat,
            wired_sync_mode=self.WiredSync,
        )

        self.device = PyK4A(self.config)

        # 0-<color 1->pc
        if camConfig["algin"] == "pointcloud":
            self.algin = 1
        else:
            self.algin = 0

        self.cameraStatus = False

        logging.warning(
            f"camera: {self.camera},  Current config are using :{camConfig}"
        )

    def openCamera(self):
        try:
            self.device.start()
            # Skip 5 first frames to give the Auto-Exposure time to adjust
            for x in range(5):
                capture = self.device.get_capture()
            self.cameraStatus = True
        except:
            # print('open camera error')
            logging.error(f"open camera error")
            # raise
            # raise ('Open Camera Error')

    def closeCamera(self):
        if not self.cameraStatus:

            try:
                self.device.stop()
                self.cameraStatus = False
            except:
                # print('close camera error')
                logging.error(f"open camera error")
                # raise ('Open Camera Error')

                # raise

    # def loadSetting(self):
    #     yaml_file = './camera/camera_setting.yaml'
    #     assert  (os.path.isfile(yaml_file), 'No such file found on folder.')
    #     if os.path.isfile(yaml_file):
    #         with open(yaml_file,'r') as f:
    #             configData = yaml.load(f, yaml.Loader)
    #             config = {}
    #             for k,v  in configData.items():
    #                 config[k] = v['Kinect']

    #         if config['resolution']=='3072p' and config['fps']> 15:
    #             config['fps'] = 15
    #         if config['depthMode']=='WFOV' and config['fps'] >15:
    #             config['fps'] = 15
    #     return config

    def loadSetting(self):
        yaml_file = "./camera/camera_setting.yaml"
        assert (os.path.isfile(yaml_file), "No such file found on folder.")

        if os.path.isfile(yaml_file):
            with open(yaml_file, "r") as f:
                configData = yaml.load(f, yaml.Loader)
                config = {}
                for k, v in configData["baseConfig"].items():
                    config[k] = v[self.camera]
                if configData["externalConfig"]:
                    for k, v in configData["externalConfig"][self.camera].items():
                        config[k] = v

        if config["resolution"] == "3072p" and config["fps"] > 15:
            config["fps"] = 15
        if config["depthMode"] == "WFOV" and config["fps"] > 15:
            config["fps"] = 15

        return config

    def parser_basic_config(self, camConfig):

        """
        parser basic config: [resolution, depthMode, serialNumber]

        Input :
            config : dict.
        Output:
            None

        """
        resolutionSet = {
            "720p": pyk4a.ColorResolution.RES_720P,
            "1080p": pyk4a.ColorResolution.RES_1080P,
            "3072p": pyk4a.ColorResolution.RES_3072P,
        }
        fpsSet = {"15": pyk4a.FPS.FPS_15, "30": pyk4a.FPS.FPS_30}
        depthModeSet = {
            "WFOV_2x2": pyk4a.DepthMode.WFOV_2X2BINNED,
            "WFOV": pyk4a.DepthMode.WFOV_UNBINNED,
            "NFOV_2x2": pyk4a.DepthMode.NFOV_2X2BINNED,
        }
        depthModeRes = {
            "WFOV_2x2": (512, 512, 3),
            "WFOV": (1024, 1024, 3),
            "NFOV_2x2": (320, 288, 3),
        }

        self.resoulution = resolutionSet[camConfig["resolution"]]
        self.fps = fpsSet[str(camConfig["fps"])]
        self.depthMode = depthModeSet[camConfig["depthMode"]]
        self.depthRes = depthModeRes[camConfig["depthMode"]]

    def parser_external_config(self, camConfig):
        """
        parse external setting from camera yaml file.

        Input :
            config : dict.
        Output:
            None

        """

        ##### Any external setting added, need to write the own code.

        if "align" in camConfig:
            # 0-<color 1->pc
            if camConfig["algin"] == "pointcloud":
                self.algin = 1
            else:
                self.algin = 0
        else:
            self.algin = 0

        # colorControlSet = {
        #     'EXPOSURE_TIME_ABSOLUTE':pyk4a.ColorControlCommand.EXPOSURE_TIME_ABSOLUTE,
        #     'AUTO_EXPOSURE_PRIORITY':pyk4a.ColorControlCommand.AUTO_EXPOSURE_PRIORITY,
        #     'BRIGHTNESS':pyk4a.ColorControlCommand.BRIGHTNESS,
        #     'CONTRAST':pyk4a.ColorControlCommand.CONTRAST,
        #     'SATURATION':pyk4a.ColorControlCommand.SATURATION,
        #     'SHARPNESS':pyk4a.ColorControlCommand.SHARPNESS,
        #     'WHITEBALANCE':pyk4a.ColorControlCommand.WHITEBALANCE,

        #     'BACKLIGHT_COMPENSATION':pyk4a.ColorControlCommand.BACKLIGHT_COMPENSATION,
        #     'GAIN':pyk4a.ColorControlCommand.GAIN,
        #     'POWERLINE_FREQUENCY':pyk4a.ColorControlCommand.POWERLINE_FREQUENCY,
        # }
        # self.colorControl = colorControlSet[camConfig['ColorControl']]

        WiredSyncSet = {
            "STANDALONE": pyk4a.WiredSyncMode.STANDALONE,
            "MASTER": pyk4a.WiredSyncMode.MASTER,
            "SUBORDINATE": pyk4a.WiredSyncMode.SUBORDINATE,
        }

        colorSet = {
            "MJPG": pyk4a.ImageFormat.COLOR_MJPG,
            "BGR": pyk4a.ImageFormat.COLOR_BGRA32,
        }

        self.colorFormat = colorSet[camConfig["ColorFormat"]]
        if "WiredSync" in camConfig:
            self.WiredSync = WiredSyncSet[camConfig["WiredSync"]]
        else:
            # Base on default setting
            self.WiredSync = WiredSyncSet["STANDALONE"]

    def getData(self):
        while True:
            if self.cameraStatus:
                startTime = time.time()
                capture = self.device.get_capture()
                if self.algin == 0:
                    colors = capture.color[:, :, 2::-1]
                    pointCloudData = capture.transformed_depth_point_cloud
                    # pointCloudData = capture.transformed_smooth_depth_point_cloud
                else:
                    colors = capture.transformed_color[..., (2, 1, 0)].reshape(
                        self.depthRes
                    )
                    pointCloudData = capture.depth_point_cloud

                endTime = time.time() - startTime
                yield [colors, pointCloudData, endTime]
            else:
                yield []


"""
sample code
cameriaSet= {
    "resolution":"3072p",
    "fps":"15",
    "depthMode":"NFOV_2x2",
    "algin":"color"
}
self.camera =  azuredkCamera.azureDK(cameriaSet)
self.cameraGen = self.camera.getData()
camData -> [RGBImage,PointCloud,GrabImageTime]
"""
