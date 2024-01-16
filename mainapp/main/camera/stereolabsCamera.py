from PIL import ImageTk, Image, ImageDraw, ImageOps
import multiprocessing as mp
import pyzed.sl as sl
import numpy as np
import cv2
import time
import yaml
import logging
import os


class zed2:
    def __init__(self):
        self.camera = "ZED2"

        # Camera setting
        self.zed = sl.Camera()
        self.init_params = sl.InitParameters()
        self.init_params.enable_right_side_measure = True

        # init setting
        camConfig = self.loadSetting()
        # income setting
        self.resolution = camConfig["resolution"]
        self.fps = camConfig["fps"]
        self.depthMode = camConfig["depthMode"]
        self.serialNumber = camConfig["serialNumber"]

        # Parser basic config setting
        self.parser_basic_config(camConfig)
        self.parser_external_config(camConfig)

        self.init_params.camera_resolution = self.camera_resolution
        self.init_params.depth_mode = self.depth_mode
        self.init_params.camera_fps = int(self.fps)

        self.runtime_parameters = sl.RuntimeParameters(
            confidence_threshold=100, texture_confidence_threshold=100
        )
        self.image = sl.Mat()
        self.depthMap = sl.Mat()
        self.point_cloud = sl.Mat()

        logging.warning(
            f"camera: {self.camera},  Current config are using :{camConfig}"
        )

    def openCamera(self):
        try:
            err = self.zed.open(self.init_params)
            self.cameraStatus = True
        except:
            # print('open camera error')
            # raise
            raise ("Open Camera Error")

    def closeCamera(self):
        if not self.cameraStatus:

            try:
                self.zed.close()
                self.cameraStatus = False
            except:
                # print('close camera error')
                # raise
                raise ("Open Camera Error")

    def loadSetting(self):

        """
        Loading camera setting.

        """
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

        return config

    def parser_basic_config(self, config):
        """
        Loading basic config: [resolution, depthMode, serialNumber]
        Input :
            config : dict.
        Output:
            None

        """

        if self.resolution == "1440p":
            self.camera_resolution = sl.RESOLUTION.HD2K  # Use HD1440 video mode
        elif self.resolution == "1080p":
            self.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
        elif self.resolution == "720p":
            self.camera_resolution = sl.RESOLUTION.HD720  # Use HD720 video mode
        elif self.resolution == "VGA":
            self.camera_resolution = sl.RESOLUTION.VGA  # Use VGA video mode
        else:
            self.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
            print(
                f"Resolution : {self.resolution} cannot found! It will convert to use 1080p resolution."
            )

        if self.depthMode == "ULTRA":
            self.depth_mode = sl.DEPTH_MODE.ULTRA
        elif self.depthMode == "NEURAL":
            self.depth_mode = sl.DEPTH_MODE.NEURAL
        elif self.depthMode == "QUALITY":
            self.depth_mode = sl.DEPTH_MODE.QUALITY
        else:
            self.depth_mode = sl.DEPTH_MODE.PERFORMANCE

        if self.serialNumber is not None:
            self.init_params.set_from_serial_number(self.serialNumber)

    def parser_external_config(self, config):
        """
        parse external setting from camera yaml file.

        Input :
            config : dict.
        Output:
            None

        """

        ##### Any external setting added, need to write the own code.

        if "cameraSide" in config:
            if config["cameraSide"] == "L":
                self.left_right = sl.VIEW.LEFT
        else:
            self.left_right = sl.VIEW.RIGHT

        if "coordinate_units" in config:
            unit = config["coordinate_units"]

            if unit == "CENTIMETER":
                self.init_params.coordinate_units = sl.UNIT.CENTIMETER
            elif unit == "METER":
                self.init_params.coordinate_units = sl.UNIT.METER
            elif unit == "INCH":
                self.init_params.coordinate_units = sl.UNIT.INCH
            elif unit == "FOOT":
                self.init_params.coordinate_units = sl.UNIT.FOOT
            else:
                self.init_params.coordinate_units = sl.UNIT.MILLIMETER

    def getData(self):
        """
        Getting data from camera.
        Input : None
        Output:
            currentImg: array. shape deponds on camera settings.
            pc: array: .shape deponds on camera settings.
            end Time: Time for capture 1 time.

            Noted: The shape of current Img and pc should be same.
        """
        while True:
            if self.cameraStatus:
                if self.zed.grab(self.runtime_parameters) == sl.ERROR_CODE.SUCCESS:
                    startTime = time.time()
                    # A new image is available if grab() returns SUCCESS

                    self.zed.retrieve_image(self.image, self.left_right)
                    self.zed.retrieve_measure(self.depthMap, sl.MEASURE.DEPTH)

                    # Point cloud
                    self.zed.retrieve_measure(self.point_cloud, sl.MEASURE.XYZRGBA)
                    pc = self.point_cloud.get_data()[:, :, :3]

                    currentImg = self.image.get_data()[:, :, :3]
                    currentImg = currentImg[:, :, ::-1]
                    # currentImg = cv2.Canny(currentImg.astype(np.uint8),100,50)
                    endTime = time.time() - startTime
                    # cv2.imshow('img', currentImg)
                    # cv2.waitKey(0)
                    yield [currentImg, pc, endTime]
                else:
                    yield []
            else:
                yield []


"""
sample code
cameriaSet= {
    "resolution":"1440p",
    "fps":"15",
    "depthMode":"NEURAL",
}
self.camera =  stereolabsCamera.zed2(cameriaSet)
self.cameraGen = self.camera.getData()
camData -> [RGBImage,PointCloud,GrabImageTime]
"""
