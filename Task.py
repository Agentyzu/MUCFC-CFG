# -*- coding: utf-8 -*-
"""
@Time ： 2023-09-13 9:58
@Auth ： XinpengLu
@File ：Task.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
class Task:
    """This class represents each task, including all of its attributes

    Attributes:
        ID       The ID of the Task
        value    The value of the Task
        Q        The workload of a task
        beta     The critical value of coalition payoff
        p        The maximum working capacity of the coalition
    """

    def __init__(self, Id, value, Q, beta, p):
        self.Id = Id
        self.value = value
        self.Q = Q
        self.beta = beta
        self.p = p
