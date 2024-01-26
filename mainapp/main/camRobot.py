import numpy as np
import os
import requests
import json
import re
import open3d as o3d
from scipy import spatial
# from camera2robot import cam2world
from .KRLTest import connectObj
from .camClass import cameraApplications
from scipy.spatial.transform import Rotation
from django.conf import settings

class cameraRobot(cameraApplications):
    def __init__(self, camera_name = 'ZIVID'):
        super().__init__(camera_name)

        self.camera_name = camera_name
        self.ip = "192.168.2.100"  # robobt ip

        self.downsample = not  True 
        self.port = 54600  # port

        self.robot_pose_scan = np.array(
            [573.95,186.87 ,513.46 , -180.00 ,0.00,180.00], dtype = np.float32
        )  # Robot Home Position

        # self.robot_pose_scan = np.array(
        #     [573.95,186.87 ,598.54 , -180.00 ,0.00,180.00], dtype = np.float32
        # )  # Robot Home Position

        self.max_points = 500  # Maxium points send to robot

        # )  # Calibration Matrix tool -> camera
        txt = os.path.join(settings.MEDIA_ROOT, 'transform_matrix.txt')
        self.tool2Cam = np.loadtxt(txt, dtype = np.float32)
        # self.obj = cam2world(
        #     self.tool2Cam, self.robot_pose_scan
        # )  # Object for camera 2 world.
        self.camDataUpdate_1 = True

        # self.camera_name = camera_name    
        
        self.wifi_command = 'nmcli dev disconnect enp4s0'    # Open wifi connectation
       
        self.ethnet_command = 'nmcli dev connect enp4s0'     # Open ethnet connectation  

    def cam2world(self, point):
        tool2Cam = self.tool2Cam
        x = point[0]
        y =  point[1]
        z = point[2]

        if self.downsample:
            x = x*10 - 7.0 if x  >0 else x*10 + 7.0
            y = y*10  - 7
            z = (point[2] - 4.0)*10  

        else:
            # x = x*10 - 4.5 if x  >0 else x*10 + 4.5
            # y = y*10  - 2.35 if y > 0 else y*10 + 2.35
            # z = (point[2] - 3)*10  

            if y < 0 :
                modify = -1.5
            elif y >=0:
                modify = 1.5
            
            if x<0 :
                x_modify = - 2.75
            elif x>=0:
                x_modify = + 2.75
                
            # modify = 0

            # x_modify = 0

            x *= 10
            y *= 10
            z*= 10


        # x = x*10 - 4.5 if x  >0 else x*10 + 4.5
        # y = y*10  - 2.65 if y > 0 else y*10 + 2.65
        # # z = (point[2] - 3.8)*10  
        # z = (point[2] - 3.8)*10  

        # point cloud send to calibration process
        point = (-x,y,z)
        cam2Tool = np.linalg.inv(tool2Cam)
        Tf_robot_pose_scan = np.eye(4)
        Tf_robot_pose_scan[0,3] = self.robot_pose_scan[0]
        Tf_robot_pose_scan[1,3] = self.robot_pose_scan[1]
        Tf_robot_pose_scan[2,3] = self.robot_pose_scan[2]
        Tf_robot_pose_scan[:3,:3] = Rotation.from_euler('xyz', [np.deg2rad(self.robot_pose_scan[5]), np.deg2rad(self.robot_pose_scan[4]), np.deg2rad(self.robot_pose_scan[3])]).as_matrix()
        Tf_robot_pose_scan_inv = np.linalg.inv(Tf_robot_pose_scan)

        cam2Base = np.dot(cam2Tool,Tf_robot_pose_scan_inv)
        cam2Base_inv = np.linalg.inv(cam2Base)

        X, Y, Z = point
        pos_xyz = [X,Y,Z] # point cloud position of any selected point
        trans_init = np.eye(4)
        trans_init[:3,:3] = tool2Cam[:3,:3]
        trans_init[0,3] = pos_xyz[0]
        trans_init[1,3] = pos_xyz[1]
        trans_init[2,3] = pos_xyz[2]

        homo = np.dot(cam2Base_inv,trans_init)

        homo_2_RotMatrix = homo[:3,:3]
        homo_2_transVector = homo[:3,3]
        rotMatrix_2_euler = Rotation.from_matrix(homo_2_RotMatrix).as_euler('xyz', degrees=True)

        # b, c = 34.67, -158.85
        b, c =  self.robot_pose_scan[-2], self.robot_pose_scan[-1]

        final_pose = [homo_2_transVector[0] + x_modify, homo_2_transVector[1] + modify, homo_2_transVector[2] - 2.5,
                      self.robot_pose_scan[-3],
                    #   self.robot_pose_scan[-2],
                    #   self.robot_pose_scan[-1]
                    b,c
                      
                      ] # keep A,B,C the same with robot pose scan.

        return final_pose


    def get_data(self, url):
        """Get Unity points and convert thoose to robot system.

        Args:
            url(str) : The input to get the unity points
        Returns:
            pts(list):  The return list, including all the robot points. 
                        For Example : 
                        [
                            {
                                "points": "(-15.7801, -10.6459, 82.2589)"
                            },
                            {
                                "points": "(-13.6308, -13.6941, 82.1895)"
                            }
                        ]
        """

        # pts = json.loads(requests.get(url).text)[0]["route"]
        

        if not self.downsample:
            # pts = [{ "points": "(-10.20, 2.09, 86.99)"},]

            # pts = [{ "points": "(17.10, -13.73, 85.96)"},]
                

            pts = [
                

                    # { "points": "(-14.69, 5.83, 92.55)"},

                    # { "points": "(2.06, 5.57, 91.81)"},
                
                    # { "points": "(-9.31, -5.74, 84.66)"},
                    # { "points": "(-8.17, -4.15, 84.39)"},
                    # { "points": "(-6.46, -4.38, 84.3)"},
                    # { "points": "(-6.67, -6.68, 84.51)"},
                
                    # { "points": "(-13.37, 2.9, 84.87)"},
                    # { "points": "(-12.19, 2.75, 84.7)"},
                    # { "points": "(-11.24, 2.22, 84.52)"},
                    # { "points": "(-10.62, 0.93, 84.41)"},
                    # { "points": "(-11.59, -0.02, 84.55)"},
                

                    { "points": "(9.8, -2.95, 81.26)"},
                    { "points": "(9.71, -3.63, 81.26)"},
                    { "points": "(9.61, -4.37, 81.26)"},



                   ]            


        else:
            # pts = [{ "points": "(-9.96, 2.32, 87.25)"},]

            # pts = [{ "points": "(-10.05, 2.8, 87.18)"},]
            pts = [{ "points": "(-21.63, 12.49, 87.72)"},]


            pts = [{ "points": "(-4.93, -9.87, 84.62)"}, 
                   { "points": "(-5.2, -8.51, 84.42)"},
                   { "points": "(-4.85, 7.35, 84.26)"},
                   { "points": "(-3.57, 7.64, 84.30)"},
                   { "points": "(-2.77, 8.45, 84.35)"},
                   { "points": "(-2.19, 9.37, 84.46)"},

                   ]            


        return pts
    
    def parse_data(self, pts, id):
        data_path = os.path.join(settings.MEDIA_ROOT, f'camera_data/{id}', '0.ply')
        """ Parse data from database.
        Args:
            pts(list): The points from database. 
                For example:                        
                    [
                        {
                            "points": "(-15.7801, -10.6459, 82.2589)"
                        },
                        {
                            "points": "(-13.6308, -13.6941, 82.1895)"
                        }
                    ]
        Return:
            points(list): Parsed points by adding default robot angle(a, b and c) by robot_pose_scan . 
                For example:
                    [[-15.7801, -10.6459, 82.2589, -180.0, 0.0, 180.0], 
                    [-13.6308, -13.6941, 82.1895, -180.0, 0.0, 180.0]]
        """
        if self.pc:
            align_pc = self.pc.point_cloud().copy_data('xyz').reshape((-1,3))
        else:
            # align_pc = np.asarray(o3d.io.read_point_cloud('data/align/0.ply').points)
            align_pc = np.asarray(o3d.io.read_point_cloud(data_path).points)
        
        points = []

        for idx, point in enumerate(pts):
            point = point["points"]
            
            point = re.sub("[()]", "", point)
            point = [float(p) for p in point.split(",")]

            # point = (pts_[idx]/[-10,10,10]).tolist()

            point = self.find_closest_point(np.asarray([point]), align_pc, k = 5, method = 'all').tolist()

            if self.downsample:
                # point = self.find_closest_point(np.asarray([point]), align_pc/10, k = 1)
                # point[:, 2] -= 3.5
                # point = np.mean(point, axis = 0).tolist()
                point = point


            point += self.robot_pose_scan[3:].tolist()      # Add default a, b and c angle to point.
            points.append(point)

        return points

    def convert2real(self, points):
        """ Convert Point cloud to robot coordiante system.
        Args:
            points(list) : input points. 
                For example:
                        [[-15.7801, -10.6459, 82.2589, -180.0, 0.0, 180.0], 
                        [-13.6308, -13.6941, 82.1895, -180.0, 0.0, 180.0]]
        Return:
            final_poses(list): output points for robot coordinate system.
                For example:
                    [[740.21704, 423.8744, -3.974609375, -180.0, 0.0, 180.0], 
                    [744.7912, 433.95306, -4.3492431640625, -180.0, 0.0, 180.0]]
        """

        final_poses = []
        for p in points:
            
            p = self.cam2world(p)            
            final_poses.append(p)


        print(final_poses)
        while len(final_poses) < self.max_points:
            final_poses.append(final_poses[-1])

        #os.system(self.ethnet_command) # Open ethnet
        return final_poses


    def connect(self):
        """ Connect Robot"""

        while True:
            # Connect Robot
            self.connectObject = connectObj()

            connect = self.connectObject.connect(self.ip, self.port)

            if not connect:
                text = 'Connect Fail'                    
            else:
                text = 'Connected OK' 
                print(text)
                break

    def send_robot_data(self, real_position, interval = 50):
        """ Send real position to robot.
        Args:
            real_position(list or array) : robot coordiaition system.
            interval(int): how many data send to robot in one time.
        Return 
            None
        """
        send_count = 0
        while True:
            # Parse Point and send to Robot system, the maxmun 
            # points all process are 500 points, we will send 
            # 50 points every step.  If given points less than
            # interval(50 points). We will fill to 50 points by 
            # last point.

            sendPos = real_position[send_count*interval :send_count*interval + interval]
            connect = self.connectObject.sendData(1,sendPos, interval)
            if not connect:
                text = 'Send Points Error'    
                self.connect()
               
                continue            
            stauts = connect[0].text
            send_count += 1
            text = f'Sent {(send_count + 1)*50} points'
            print(text)  
            if stauts == 'Done':
                print('Finish sending process')
                break  

    def find_closest_point(self, target_point, points_array, k = 5, method = 'xy'):
        # target_point[0][2] -= 3.8
        factor = [-10, 10, 10]
        target_point = target_point.squeeze()
        if method == 'xy':
            distances = np.linalg.norm(points_array[:,:-1] - target_point[:-1]*factor[:-1], axis=1)
        else:
            x = target_point[0]
            y = target_point[1]

            x = 0
            y = 0
            z = 3.0
            
            x = -0.3 if x>0 else 0.3
            y = +0.3 if y>0 else -0.3
            
            target_point -= [x, y, z]

            distances = np.linalg.norm(points_array - target_point*factor, axis=1)
        index = np.argsort(distances)[:k]
        
        closest_point = points_array[index]/factor
        if k >= 2:
            closest_point = np.mean(closest_point, axis = 0)
        return closest_point        

# if __name__ == '__main__':
#     from sklearn.neighbors import KDTree
#     camRobot = cameraRobot()
#     points = camRobot.get_data('https://threed-object.onrender.com/get_object_3d/')
#     ply = o3d.io.read_point_cloud('data/ply/1.ply')
#     points = camRobot.parse_data(points)
#     ply = np.asarray(ply.points)

#     def find_closest_point(target_point, points_array):
#         distances = np.linalg.norm(points_array - target_point, axis=1)
#         # closest_index = np.argmin(distances)
#         index = np.argsort(distances)[:5]
#         closest_point = points_array[index]
#         return closest_point    
#     # distance, idx = KDTree(ply).query(np.asarray([points[0][:3]])*10)
#     point = find_closest_point(np.asarray(points[0][:3])*10, ply)
#     final_poses = camRobot.convert2real(points)
#     print(final_poses[0])