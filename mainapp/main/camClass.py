import numpy as np
import cv2
from .camera import intelCamera, zividCamera
import os
import open3d as o3d
from django.conf import settings
from mainapp.models import InitialObject

class cameraApplications:
    """ Camera Applications.
    """
    def __init__(self,  camera_name = 'ZIVID'):
        self.camDataUpdate_1 = True
        self.camera_name = camera_name
        self.count = 0

        self.image_save_path = ''
        self.ply_save_path = ''
        self.init_camera = True
        self.pc = None

    def get_folder_length(self, path):
        """ Get length for folder by include only  jpg, png or jpeg file."""        
        self.count = len(
            [
                i
                for i in os.listdir(path)
                if i.lower().endswith(("jpg", "png", "jpeg"))
            ]
        )
        
    def capture(self, state):
        """
        Capture from zivid camera and save image and ply  file to ./data folder
        Args:
            None
        Returns:
            result(bool) : The return value, True for success, False for otherwise.
        """

        if self.init_camera:
            if  self.camera_name == 'ZIVID':
                self.camera = zividCamera.zividCamera()    #Connect Zivid camera
            else:
                self.camera = intelCamera.L515()  # Connect Intel camera
            self.init_camera = False

        # self.get_folder_length(self.camera.image_save_path)   # Get Folder length

        # self.ply_save_path = os.path.join(self.camera.ply_save_path, f'{self.count}.ply')
        # self.image_save_path = os.path.join(self.camera.image_save_path, f'{self.count }.jpg')

        self.camera.openCamera()
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
        self.image_save_path = os.path.join(save_path, f'{self.count}.jpg')
        self.ply_save_path = os.path.join(save_path, 'output.ply')
        self.ply_data_path = os.path.join(save_path, '0.ply')
        img_res_path = ""
        # ------------------------

        if cameraData_1:
            self.image, self.pc, _ = cameraData_1
            # ----------------
            self.save_img(self.image_save_path)
            if state == 'save_ply':
                self.save_pc(self.ply_save_path, self.ply_data_path)
                init_obj.ply_path = f'media/camera_data/{camera_data_id}/output.ply'
                init_obj.is_finished = True
            img_res_path = f'media/camera_data/{camera_data_id}/{self.count}.jpg' 
            init_obj.image_path = img_res_path 
            init_obj.save()   
            # ----------------

            result = True
        return result, img_res_path 

    def camDataUpdate_pick(self, camera):
        if self.camDataUpdate_1:
            self.camerGen_1 = camera.getData()
            cameraData_1 = next(self.camerGen_1)

        return cameraData_1
    def check_folder(self):
        os.makedirs('./data/image', exist_ok = True)
        os.makedirs('./data/ply', exist_ok = True)
        

    def save_img(self, save_path = ''):
        """ Save image to path.
        Args:
            save_path(str): File Path to save point cloud, it should be includ file name. 
                            example: data/0.jpg
        """        
        # self.check_folder()
        # if '.jpg' not in save_path:
        #     save_path = os.path.join(self.camera.image_save_path , '0.jpg')     
        # print(save_path)
        cv2.imwrite(save_path, self.image)

    def save_pc(self, save_path = '', data_path = ''):
        """ Save ply point cloud to path.
        Args:
            save_path(str): File Path to save point cloud, it should be includ file name. 
                            example: data/0.ply
        """
        # self.check_folder()
        # if '.ply' not in save_path:
        #     save_path = os.path.join(self.camera.ply_save_path, '0.ply')
        
        ###Zivid
        if self.camera_name == 'ZIVID':
            # frame.point_cloud = frame.point_cloud().downsampled(zivid.PointCloud.Downsampling.by2x2)
            if not self.downsample:
                self.pc.save(
                    f"{save_path}"
                )
                self.pc.save(
                    # 'data/align/0.ply'
                    f"{data_path}"
                )
            else:
                self.pc.save(
                    # './data/align/0.ply'
                    f"{data_path}"
                )
                pc_ = self.camera.downsample(self.pc)
                # pc_ = self.pc.point_cloud()
                ply = pc_.copy_data('xyz')
                image = pc_.copy_data('rgba')

                # shape = ply.shape
                # resize = (int(ply.shape[0]/2), int(ply.shape[1]/2))
                # ply = cv2.resize(ply, (resize))
                # image = cv2.resize(image, (resize))

                # ply =  self.pc.point_cloud().copy_data('xyz')
                ply = ply.reshape(-1, 3)
                ply = np.nan_to_num(ply, 0)
                pcd = o3d.geometry.PointCloud()
                pcd.points = o3d.utility.Vector3dVector(ply)
                colors = image[:,:,:-1][:,:, ::-1]/255.0
                # colors = self.image[:,:,::-1]/255.0
                pcd.colors = o3d.utility.Vector3dVector(colors.reshape(-1, 3))
                o3d.io.write_point_cloud(f"{save_path}", pcd)            

        else:
            ### Intel
            ply = self.pc.reshape(-1, 3)
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(ply)
            colors = self.image/255.0
            pcd.colors = o3d.utility.Vector3dVector(colors.reshape(-1,3))
            o3d.io.write_point_cloud(f"{save_path}", pcd)
        