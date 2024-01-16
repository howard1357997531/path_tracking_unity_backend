import socket
import sys
import time
import xml.etree.ElementTree as ET


class connectObj:
    def __init__(self):
        self.position_pre_define = ["X ", "Y ", "Z ", "A ", "B ", "C "]
        self.driver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.driver.settimeout(5)
        self.connect_status = not True
        self.count = 0

    def connect(self, host: str, port: int):
        try:
            self.driver.connect((host, int(port)))
            self.connect_status = True
        except Exception as e:
            print(e)
            self.connect_status = False

        return self.connect_status

    def sendData(self, controlCode: int, position: list, point_threshold: int = 50):
        """Fetch position points from input and send to robot.

        The function is getting points from inputs,

        Args:
            controlCode(int) : control case to the robot, in current function only apply digit 1 which means move robot to certain points.
            position(list): container to include all the points from the input. it should already  converted to robot system.
            point_threshold(int) : Threshold to

        Return:
            bool: The return value. True for success connect robot, False otherwise.

        """

        if not self.connect_status:
            return False
        string = ""
        while len(position) < point_threshold:
            position.append(position[-1])

        for idx, pos in enumerate(position):
            assert Warning(len(pos) == len(self.position_pre_define))
            new_pos = ",".join(
                [f"{x}{str(y)}" for x, y in zip(self.position_pre_define, pos)]
            )
            idx += 1
            if idx < 10:
                idx = "0" + str(idx)

            new_pos = "{" + new_pos + "}"
            pt = f"<GetData{idx}>{new_pos}</GetData{idx}>"
            string += pt

        sendData = f"<xml><RobotCommand><PGNO>{controlCode}</PGNO><Pos><Start>{self.count*50 + 1}</Start>{string}</Pos></RobotCommand></xml>"
        sendData = sendData.encode("utf8")

        self.driver.send(sendData)
        time.sleep(0.1)

        received = self.driver.recv(1024).decode()
        root = ET.fromstring(received)
        self.count += 1
        return root
