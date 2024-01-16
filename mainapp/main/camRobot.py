import numpy as np
import os
import requests
import json
import re
import open3d as o3d
from .camera2robot import cam2world
from KRLTest import connectObj
from camClass import cameraApplications

class cameraRobot(cameraApplications):
    def __init__(self, camera_name = 'ZIVID'):
        super().__init__(camera_name)
        self.camera_name = camera_name
        self.ip = "192.168.2.100"  # robobt ip

        self.port = 54600  # port

        self.robot_pose_scan = np.array(
            [573.95,186.87 ,513.46 , -180.00 ,0.00,180.00], dtype = np.float32
        )  # Robot Home Position

        self.max_points = 500  # Maxium points send to robot

        # )  # Calibration Matrix tool -> camera
        self.tool2Cam = np.loadtxt('transform_matrix.txt',dtype = np.float32)
        self.obj = cam2world(
            self.tool2Cam, self.robot_pose_scan
        )  # Object for camera 2 world.
        self.camDataUpdate_1 = True

        # self.camera_name = camera_name    
        
        self.wifi_command = 'nmcli dev disconnect enp4s0'    # Open wifi connectation
       
        self.ethnet_command = 'nmcli dev connect enp4s0'     # Open ethnet connectation  

    def cam2world(self, point):
        return self.obj.process(point)


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

        pts = json.loads(requests.get(url).text)[0]["route"]

        return pts
    
    def parse_data(self, pts):
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
        points = []
        for point in pts:
            point = point["points"]
            
            point = re.sub("[()]", "", point)
            point = [float(p) for p in point.split(",")]

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

        while len(final_poses) < self.max_points:
            final_poses.append(final_poses[-1])

        os.system(self.ethnet_command) # Open ethnet
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
                continue            
            stauts = connect[0].text
            send_count += 1
            text = f'Sent {(send_count + 1)*50} points'
            print(text)  
            if stauts == 'Done':
                print('Finish sending process')
                break        


if __name__ == '__main__':
    camRobot = cameraRobot()
    points = camRobot.get_data('https://threed-object.onrender.com/get_object_3d/')

    points = camRobot.parse_data(points)
    final_poses = camRobot.convert2real(points)
    print(final_poses)