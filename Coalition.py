# -*- coding: utf-8 -*-
"""
@Time ： 2023-09-13 10:07
@Auth ： XinpengLu
@File ：Coalition.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import math
import copy
from itertools import combinations
import random

class Coalition():
    """This class represents functions related to coalitions, including utility computation and allocation

        Attributes:
            UAV         The list of the UAV
            tasks       The list of the tasks
            alpha       The fixed flight cost of the UAV
            assignment  The division of coalitions
    """

    def __init__(self, UAVs, tasks, alpha):
        self.UAVs = UAVs
        self.tasks = tasks
        self.alpha = alpha
        self.assignments = [[] for _ in range(len(self.tasks))]
        S = [random.randint(0, len(self.tasks) - 1) for _ in range(len(self.UAVs))]
        for i in range(len(self.UAVs)):
            self.assignments[S[i]].append(i)

    # Calculate the total working capacity of the coalition
    def sum_efficiency(self, i):
        if len(self.assignments[i]) != 0:
            return sum(self.UAVs[j].efficiency for j in self.assignments[i])
        else:
            return 0

    # The time for the coalition to complete the task
    def time_coalition(self, i):
        if len(self.assignments[i]) != 0:
            return self.tasks[i].Q / self.sum_efficiency(i)
        else:
            return 0

    # The flight cost of the coalition to complete the task
    def cost_coalition(self, i):
        return self.time_coalition(i) * len(self.assignments[i]) * self.alpha

    # The payoff of completing the task for the coalition
    def revenue_coalition(self, i):
        # If there are UAVs to do the task
        if len(self.assignments[i]) != 0:
            if self.sum_efficiency(i) < self.tasks[i].beta:
                return self.tasks[i].value * self.sum_efficiency(i) / self.tasks[i].beta
            elif self.sum_efficiency(i) < self.tasks[i].p:
                return self.tasks[i].value * (self.sum_efficiency(i) - self.tasks[i].p) / (self.tasks[i].beta - self.tasks[i].p)
            else:
                return 0
        # If there are no UAVs to complete the task
        else:
            return 0

    # The utility of completing the task for the coalition
    def utility_coalition(self, i):
        return self.revenue_coalition(i) - self.cost_coalition(i)

    # Calculate the marginal contribution of UAV j to accomplish task i
    def marginal_contribution(self, i, j, coalition):
        initial = self.assignments
        # The coalition of the current task is replaced by a subset
        coalition_copy1 = copy.deepcopy(self.assignments)
        coalition_copy1[i] = coalition
        self.assignments = coalition_copy1
        utility1 = self.utility_coalition(i)

        # Remove the UAV j within this coalition
        coalition_copy2 = copy.deepcopy(coalition_copy1)
        coalition_copy2[i].remove(j)
        self.assignments = coalition_copy2
        utility2 = self.utility_coalition(i)
        self.assignments = initial

        # The return utility difference is then the marginal contribution of UAV j in the coalition
        return utility1 - utility2

    # The Shapley value is used to calculate the utility allocation of UAVs within the coalition
    def shapley_value(self, i):
        num = len(self.assignments[i])
        shapley_values = [0 for _ in range(num)]
        for j in self.assignments[i]:
            for coalition_size in range(1, num + 1):
                # Generate all nonempty subsets of the coalition (combination)
                for coalition in combinations(self.assignments[i], coalition_size):
                    if j not in coalition:
                        continue
                    w = math.factorial(coalition_size - 1) * math.factorial(num - coalition_size) / math.factorial(num)
                    shapley_values[self.assignments[i].index(j)] += w * self.marginal_contribution(i, j, list(coalition))
        return shapley_values
