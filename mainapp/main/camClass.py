import numpy as np
import cv2
from camera import intelCamera, zividCamera
import os
import open3d as o3d

class cameraApplications:
    """ Camera Applications.
    """
    def __init__(self,  camera_name = 'ZIVID'):
        self.camDataUpdate_1 = True
        self.camera_name = camera_name
        self.count = 0

        self.image_save_path = ''
        self.ply_save_path = ''

    def get_folder_length(self, path):
        """ Get length for folder by include only  jpg, png or jpeg file."""        
        self.count = len(
            [
                i
                for i in os.listdir(path)
                if i.lower().endswith(("jpg", "png", "jpeg"))
            ]
        )
        
    def capture(self):
        """
        Capture from zivid camera and save image and ply  file to ./data folder
        Args:
            None
        Returns:
            result(bool) : The return value, True for success, False for otherwise.
        """
        if  self.camera_name == 'ZIVID':
            self.camera = zividCamera.zividCamera()    #Connect Zivid camera
        else:
            self.camera = intelCamera.L515()  # Connect Intel camera

        self.get_folder_length(self.camera.image_save_path)   # Get Folder length

        self.ply_save_path = os.path.join(self.camera.ply_save_path, f'{self.count}.ply')
        self.image_save_path = os.path.join(self.camera.image_save_path, f'{self.count }.jpg')


        self.camera.openCamera()
        cameraData_1 = self.camDataUpdate_pick(self.camera)  # Capture camera
        result = False
        if cameraData_1:
            self.image, self.pc, _ = cameraData_1

            result = True

        return result

    def camDataUpdate_pick(self, camera):
        if self.camDataUpdate_1:
            self.camerGen_1 = camera.getData()
            cameraData_1 = next(self.camerGen_1)

        return cameraData_1

    def save_img(self, save_path = ''):
        """ Save image to path.
        Args:
            save_path(str): File Path to save point cloud, it should be includ file name. 
                            example: data/0.jpg
        """        
        if '.jpg' not in save_path:
            save_path = os.path.join(self.camera.image_save_path , '0.jpg')     
        print(save_path)
        cv2.imwrite(save_path, self.image)

    def save_pc(self, save_path = ''):
        """ Save ply point cloud to path.
        Args:
            save_path(str): File Path to save point cloud, it should be includ file name. 
                            example: data/0.ply
        """
        if '.ply' not in save_path:
            save_path = os.path.join(self.camera.ply_save_path, '0.ply')
        ###Zivid
        if self.camera_name == 'ZIVID':
            self.pc.save(
                f"{save_path}"
            )
        else:
            ### Intel
            ply = self.pc.reshape(-1, 3)
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(ply)
            o3d.io.write_point_cloud(f"{save_path}", pcd)
        self.camera.closeCamera()