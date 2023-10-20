# -*- coding: utf-8 -*-
"""
@Time ： 2023-09-13 9:58
@Auth ： XinpengLu
@File ：UAV.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
class UAV:
    """This class represents each UAV, including all of its attributes

    Attributes:
        ID               The value of the UAV
        efficiency       The efficiency of the UAV
        task_selection   The task selection of the UAV
    """

    def __init__(self, Id, efficiency, task_selection):
        self.Id = Id
        self.efficiency = efficiency
        self.task_selection = task_selection
