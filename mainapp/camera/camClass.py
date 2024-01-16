import numpy as np
import cv2
from .camera import intelCamera
import os
import open3d as o3d
from django.conf import settings
from mainapp.models import InitialObject


class cameraApplications:
    def __init__(self):
        # save_path = "./data"
        # os.makedirs(save_path, exist_ok=True)
        # self.count = len(
        #     [
        #         i
        #         for i in os.listdir(save_path)
        #         if i.lower().endswith(("jpg", "png", "jpeg"))
        #     ]
        # )
        self.count = 1
        self.camDataUpdate_1 = True

    def capture(self, state):
        """
        Capture from camera, save image and ply  file to ./data folder
        Args:
            None
        Returns:
            result(bool) : The return value, True for success, False for otherwise.
        """

        self.camera = intelCamera.L515()  # Connect camera
        self.camera.openCamera() # 沒連接camera會直接跳except
        cameraData_1 = self.camDataUpdate_pick(self.camera)  # Capture camera
        result = False

        # ------------------------
        if state == "open":
            check_folder = InitialObject.objects.filter(is_finished=False)
            if check_folder:
                init_obj = check_folder.first()
            else:
                init_obj = InitialObject.objects.create()
        else:
            init_obj = InitialObject.objects.filter(is_finished=False).first()
        camera_data_id = init_obj.id
        save_path = os.path.join(settings.MEDIA_ROOT, f'camera_data/{camera_data_id}')
        os.makedirs(save_path, exist_ok=True)
        self.count = 1 + len([i for i in os.listdir(save_path) if i.lower().endswith(('jpg', 'jpeg', 'png'))])
        img_path = os.path.join(save_path, f'{self.count}.jpg')
        ply_path = os.path.join(save_path, 'output.ply')
        img_res_path = ""
        # ------------------------

        # cameraData_1 = True 相機有偵測到物體
        if cameraData_1:
            image, pc, _ = cameraData_1
            # cv2.imwrite(f"./data/{self.count}.jpg", image[:,:,::-1])
            cv2.imwrite(img_path, image[:,:,::-1])
            
            if state == "save_ply":
                ply = pc.reshape(-1, 3)
                pcd = o3d.geometry.PointCloud()
                pcd.points = o3d.utility.Vector3dVector(ply)
                o3d.io.write_point_cloud(ply_path, pcd)
                
            # ------------------------
                init_obj.ply_path = f'media/camera_data/{camera_data_id}/output.ply'
                init_obj.is_finished = True
            img_res_path = f'media/camera_data/{camera_data_id}/{self.count}.jpg' 
            init_obj.image_path = img_res_path 
            init_obj.save()   
            # ------------------------

            self.camera.closeCamera()
            result = True

        return result, img_res_path

    def camDataUpdate_pick(self, camera):
        if self.camDataUpdate_1:
            self.camerGen_1 = camera.getData()
            cameraData_1 = next(self.camerGen_1)
        return cameraData_1
