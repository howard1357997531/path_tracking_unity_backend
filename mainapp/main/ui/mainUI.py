import time
from PIL import ImageTk, Image, ImageDraw, ImageOps
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import cv2
import json
import os


class Main(tk.Tk):
    def __init__(self):
        self.windows = tk.Tk()

        width = self.windows.winfo_screenwidth()
        height = self.windows.winfo_screenheight()
        # setting tkinter window size

        width = 260
        height = 180

        self.windows.grid_rowconfigure(0, weight=1)
        self.windows.grid_columnconfigure(0, weight=1)

        self.windows.geometry("%dx%d" % (width, height))

        # self.widget_width, self.widget_height = int(width/2) - 10, int(height/1.25)

        self.windows.title("Plant Pick")

        frame_container = tk.Frame(
            self.windows, width=int(width / 2), height=int(height / 2), bg=""
        )

        frame_container.grid(
            column=0, columnspan=1, row=0, rowspan=3, padx=10, pady=10, sticky=""
        )

        self.titleLabel = tk.Label(
            frame_container, text="Robot Application", font=(None, 20), bg="cyan"
        )
        self.titleLabel.grid(
            column=0, columnspan=2, row=0, stick="nswe", padx=5, pady=5
        )

        self.btnOpenCam_1 = tk.Button(
            frame_container,
            text="Camera",
            command=self.openCam_1,
            font=(None, 15),
            activebackground="Cyan",
        )
        self.btnOpenCam_1.grid(
            column=0, columnspan=2, row=1, stick="nswe", padx=5, pady=5
        )

        self.btnMoveRobot_1 = tk.Button(
            frame_container,
            text="Robot",
            command=self.moveButtonClick,
            font=(None, 15),
            activebackground="Cyan",
        )
        self.btnMoveRobot_1.grid(
            column=0, columnspan=2, row=5, stick="nswe", padx=5, pady=5
        )

        # Parameters
        self.cameraStatus_1 = False
        self.moveStatus = False

        # self.windows.resizable(False, False)

    def openCam_1(self):
        if self.cameraStatus_1:
            self.cameraStatus_1 = False
            self.btnOpenCam_1.configure(bg="Cyan")
        else:
            self.cameraStatus_1 = True
            self.btnOpenCam_1.configure(bg="red")

    def moveButtonClick(self):
        if self.moveStatus:
            self.moveStatus = False
            self.btnMoveRobot_1.configure(bg="Cyan")

        else:
            self.moveStatus = True
            self.btnMoveRobot_1.configure(bg="red")

    def modifyInfoText(self, text):
        self.info.set(text)

    def show(self):
        self.windows.mainloop()


if __name__ == "__main__":
    ui = Main()
    ui.show()
