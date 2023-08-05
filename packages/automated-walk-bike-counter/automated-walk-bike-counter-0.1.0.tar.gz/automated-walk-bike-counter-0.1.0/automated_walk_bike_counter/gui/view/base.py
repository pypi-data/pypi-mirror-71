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


class BaseFrame(object):
    # Empty base class used to share most basic functions between frames and views
    FONT_FAMILY = "Verdana"


class BaseView(BaseFrame):
    # Base View implementing most of the view functionality

    def __init__(self, parent, controller):

        self.parent = parent
        self.controller = controller
        self.controller.view = self
