import pyrealsense2 as rs
import numpy as np
import time
import yaml
import os
import logging


class L515:
    def __init__(self):
        # init setting
        self.camera = "Intel"
        # camera init
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.pc = rs.pointcloud()
        self.pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        self.pipeline_profile = self.config.resolve(self.pipeline_wrapper)
        self.device = self.pipeline_profile.get_device()
        self.device_product_line = str(
            self.device.get_info(rs.camera_info.product_line)
        )

        camConfig = self.loadSetting()

        self.parser_basic_config(camConfig)
        self.parser_external_config(camConfig)

        self.cameraStatus = False

        # Camera setting
        self.config.enable_stream(
            rs.stream.color, self.resolution[0], self.resolution[1], rs.format.rgb8, 30
        )

        logging.warning(
            f"camera: {self.camera},  Current config are using :{camConfig}"
        )

        # self.cameraSensor.set_option(rs.option.exposure,300)

    def openCamera(self):
        try:
            self.pipeline.start(self.config)
            # Skip 5 first frames to give the Auto-Exposure time to adjust
            for x in range(5):
                self.pipeline.wait_for_frames()
            self.pipeline = self.pipeline
            self.cameraStatus = True
        except:
            print("open camera error")
            raise

    def closeCamera(self):
        if self.cameraStatus:
            try:
                self.pipeline.stop()
                self.cameraStatus = False
            except:
                print("close camera error")
                raise

    def loadSetting(self):
        yaml_file = "./camera/camera_setting.yaml"
        assert (os.path.isfile(yaml_file), "No such file found on folder.")

        if os.path.isfile(yaml_file):
            with open(yaml_file, "r") as f:
                configData = yaml.load(f, yaml.Loader)
                config = {}
                for k, v in configData["baseConfig"].items():
                    config[k] = v[self.camera]
                external = configData["externalConfig"]
                if external and self.camera in external:
                    for k, v in external[self.camera].items():
                        config[k] = v

        return config

    def parser_basic_config(self, camConfig):

        """
        parser basic config: [resolution, depthMode, serialNumber]

        Input :
            config : dict.
        Output:
            None

        """
        if "resolution" not in camConfig:
            print(
                f"Resolution setting cannot found! It will convert to use 1080p resolution."
            )
            self.resolution = [1920, 1080]
        resolution = camConfig["resolution"]
        if resolution == "1080p":
            self.resolution = [1920, 1080]
        elif resolution == "720p":
            self.resolution = [1280, 720]
        elif resolution == "540p":
            self.resolution = [960, 540]
        else:
            print(
                f"Resolution : {resolution} cannot found! It will convert to use 1080p resolution."
            )
        #
        self.serialNumber = camConfig["serialNumber"]
        self.depth = camConfig["depthMode"]

        if self.serialNumber is not None:
            self.config.enable_device(self.serialNumber)

        if self.depth:
            self.config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)
            self.align_to = rs.stream.color
            self.align = rs.align(self.align_to)
            self.depth_sensor = self.device.first_depth_sensor()
            self.cameraSensor = self.device.query_sensors()[1]

            self.depth_sensor.set_option(rs.option.receiver_gain, 18)

    def parser_external_config(self, camConfig):
        """
        parse external setting from camera yaml file.

        Input :
            config : dict.
        Output:
            None

        """
        ##### Any external setting added, need to write the own code.

        if "laser_power" in camConfig:
            self.depth_sensor.set_option(
                rs.option.laser_power, camConfig["laser_power"]
            )

        if "min_distance" in camConfig:
            self.depth_sensor.set_option(
                rs.option.min_distance, camConfig["min_distance"]
            )

        return

    def getData(self):
        while True:
            if self.cameraStatus:
                startTime = time.time()
                frames = self.pipeline.wait_for_frames()
                if self.depth:
                    aligned_frames = self.align.process(frames)
                    colorFrame = aligned_frames.get_color_frame()
                    colorImage = np.asanyarray(colorFrame.get_data())
                    depthFrame = aligned_frames.get_depth_frame()
                    pointCloudData = self.pc.calculate(depthFrame)
                    pointCloudData = pointCloudData.get_vertices()
                    pointCloudData = (
                        np.asanyarray(pointCloudData)
                        .view(np.float32)
                        .reshape(self.resolution[1], self.resolution[0], 3)
                        * 1000
                    )


                


                    endTime = time.time() - startTime
                    yield [colorImage, pointCloudData, endTime]
                else:
                    colorFrame = frames.get_color_frame()
                    colorImage = np.asanyarray(colorFrame.get_data())
                    endTime = time.time() - startTime
                    yield [colorImage, endTime]
            else:
                yield []


class D435I:
    def __init__(self, cameraConfig):
        # init setting
        if "resolution" not in cameraConfig:
            print(
                f"Resolution setting cannot found! It will convert to use 1080p resolution."
            )
            self.supportResolution = [1920, 1080]
        resolution = cameraConfig["resolution"]
        if resolution == "1080p":
            self.supportResolution = [1920, 1080]
        elif resolution == "720p":
            self.supportResolution = [1280, 720]
        elif resolution == "540p":
            self.supportResolution = [960, 540]
        else:
            print(
                f"Resolution : {resolution} cannot found! It will convert to use 1080p resolution."
            )

        self.cameraStatus = False
        self.serialNumber = None
        self.cameraConfig = cameraConfig

        if "SerialNumber" in self.cameraConfig:
            self.serialNumber = self.cameraConfig["SerialNumber"]
        # camera init
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        self.pipeline_profile = self.config.resolve(self.pipeline_wrapper)
        self.device = self.pipeline_profile.get_device()
        self.device_product_line = str(
            self.device.get_info(rs.camera_info.product_line)
        )

        # Camera setting

        self.config.enable_stream(
            rs.stream.color, self.resolution[0], self.resolution[1], rs.format.rgb8, 30
        )
        if self.serialNumber is not None:
            self.config.enable_device(self.serialNumber)

        # self.cameraSensor.set_option(rs.option.exposure,300)

    def openCamera(self):
        try:
            self.pipeline.start(self.config)
            # Skip 5 first frames to give the Auto-Exposure time to adjust
            for x in range(5):
                self.pipeline.wait_for_frames()
            self.cameraStatus = True
        except:
            print("open camera error")
            raise

    def loadSetting(self):

        with open("./camera/camera_setting.yaml", "r") as f:
            configData = yaml.load(f, yaml.Loader)
            config = {}
            for k, v in configData.items():
                config[k] = v["Intel"]
        return config

    def closeCamera(self):
        try:
            self.pipeline.stop()
            self.cameraStatus = False
        except:
            print("close camera error")
            raise

    def getData(self):
        while True:
            if self.cameraStatus:
                startTime = time.time()
                frames = self.pipeline.wait_for_frames()
                colorFrame = frames.get_color_frame()
                colorImage = np.asanyarray(colorFrame.get_data())
                endTime = time.time() - startTime
                yield [colorImage, endTime]
            else:
                yield []
