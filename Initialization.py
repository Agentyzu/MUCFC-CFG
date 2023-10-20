# -*- coding: utf-8 -*-
"""
@Time ： 2023-09-13 22:10
@Auth ： XinpengLu
@File ：Initialization.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
from Task import Task
from UAV import UAV
import random


class Initialization():
    'This class represents the initialization of the task and UAV properties'
    def __init__(self):
        from Mytoolhelper import Toolhelper
        self.N_UAV, self.N_Task, self.alpha, self.iteration, self.iter_avg = Toolhelper().load_configuration()

    # Initialize the attributes of the UAV
    def Init_UAV(self):
        UAVs = []
        for i in range(self.N_UAV):
            Id = i
            efficiency = random.uniform(0.5, 1)
            task_selection = random.randint(0, self.N_Task - 1)
            uav = UAV(Id, efficiency, task_selection)
            UAVs.append(uav)
        return UAVs

    # Initialize the attributes of the task
    def Init_Task(self):
        Tasks = []
        for i in range(self.N_Task):
            Id = i
            value = random.uniform(5, 10)
            Q = random.uniform(1, 1.2) * value
            beta = random.uniform(2, 3)
            p = random.uniform(5, 6)
            task = Task(Id, value, Q, beta, p)
            Tasks.append(task)
        return Tasks