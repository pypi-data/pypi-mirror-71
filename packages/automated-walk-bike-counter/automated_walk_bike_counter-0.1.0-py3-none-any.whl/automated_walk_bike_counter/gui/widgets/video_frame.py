# Copyright (c) Data Science Research Lab at California State University Los
# Angeles (CSULA), and City of Los Angeles ITA
# Distributed under the terms of the Apache 2.0 License
# www.calstatela.edu/research/data-science
# Designed and developed by:
# Data Science Research Lab
# California State University Los Angeles
# Dr. Mohammad Pourhomayoun
# Mohammad Vahedi
# Haiyan Wang

import os
import threading
from tkinter import ALL, CENTER, HORIZONTAL, Canvas, E, Event, Frame, IntVar, N, S, W
from tkinter.ttk import Progressbar

import cv2
from PIL import Image, ImageTk


class VideoFrame(Frame):
    def __init__(self, parent, controller):
        super(VideoFrame, self).__init__(parent, height=600)

        self.controller = controller
        self.object_detection_thread = None
        self.detection_thread_event = None
        self.loading_thread = None
        self.loading_thread_event = None
        self.loading_thread_started = False
        self.loading_frames = []
        self.loading_image = Image.open(
            os.path.join(os.path.dirname(__file__), "../static/images/loading.gif")
        )
        self.video_frame_width = 800
        self.video_frame_height = 600
        self.cur_fr_number = IntVar()
        self.video_player_canvas = Canvas(
            master=self, width=800, height=600, bg="black"
        )
        self.progressbar = Progressbar(
            master=self,
            orient=HORIZONTAL,
            mode="determinate",
            variable=self.cur_fr_number,
        )
        self.video_player_canvas.grid(row=0, column=0, padx=(0, 0), sticky=(W, E, S, N))
        self.progressbar.grid(
            row=1, column=0, padx=(0, 0), pady=(0, 0), sticky=(E, W, S)
        )
        self.grid_columnconfigure(0, weight=1)

        self.controller.video_frame = self

    def initialize_canvas(self):
        self.making_loading_frames()

        self.detection_thread_event = Event()
        sample_video_path = os.path.join(
            os.path.dirname(__file__), "../static/videos/sample.mp4"
        )
        self.object_detection_thread = threading.Thread(
            target=self.controller.update_video_canvas,
            args=(sample_video_path, self),
            daemon=True,
        )
        self.object_detection_thread.start()

        self.loading_thread_event = Event()
        self.loading_thread = threading.Thread(
            target=self.video_player_canvas_loading_animation, args=(), daemon=True
        )
        self.loading_thread.start()

    def video_player_canvas_loading_animation(self):

        self.loading_thread_started = True
        cnt = 0

        while self.loading_thread_started and cnt < len(self.loading_frames):

            self.video_player_canvas.after(
                75, self.change_video_player_canvas_image(self.loading_frames[cnt])
            )

            if cnt == len(self.loading_frames) - 1:
                cnt = 0
            else:
                cnt += 1

    def change_video_player_canvas_image(self, image):

        self.video_player_canvas.create_image(
            self.video_frame_width / 2,
            self.video_frame_height / 2,
            anchor=CENTER,
            image=image,
        )
        self.video_player_canvas.image = image

    def making_loading_frames(self):
        try:
            i = 0
            while True:
                photo_frame = ImageTk.PhotoImage(self.loading_image)

                self.loading_frames.append(photo_frame)

                i += 1
                self.loading_image.seek(i)
        except EOFError:
            pass

    def handle_post_processed_frame(self, frame, frame_number):

        if self.loading_thread_started:
            self.loading_thread_started = False

        dim = None
        (h, w) = frame.shape[:2]

        r = 800 / float(w)
        dim = (800, int(h * r))

        self.cur_fr_number.set(frame_number)
        frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

        frame_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_image = Image.fromarray(frame_image)
        frame_image = ImageTk.PhotoImage(frame_image)

        self.video_player_canvas.create_image(
            self.video_frame_width / 2,
            self.video_frame_height / 2,
            anchor=CENTER,
            image=frame_image,
        )
        self.video_player_canvas.image = frame_image

    def stop_threads(self):
        self.video_player_canvas.delete(ALL)
        self.cur_fr_number.set(0)

    def set_progressbar_maximum(self):
        self.progressbar["maximum"] = self.controller.video.frame_count
