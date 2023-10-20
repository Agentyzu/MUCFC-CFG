# -*- coding: utf-8 -*-
"""
@Time ： 2023-09-13 10:51
@Auth ： XinpengLu
@File ：Solution.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import random
from Coalition import Coalition
import copy

class Solution():
    'This class represents the specific procedure of the coalition formation algorithm'

    """
    The algorithm is a multi-UAV coalition formation algorithm based on marginal utility. 
    The algorithm is implemented through multiple rounds of iterations, and the preference
    of the UAV is considered to choose to join the coalition.
    """

    def Maiginal_utility(self, UAVs, Tasks, alpha, iteration):
        # Create a new coalition object
        coalition = Coalition(UAVs, Tasks, alpha)
        Iter_utility1 = []

        # The iterative process of the algorithm
        for rounds in range(iteration):
            UAV_j = random.randint(0, len(UAVs) - 1)
            Task_i = random.randint(0, len(Tasks) - 1)
            Original_coalition = [(i, sublist.index(UAV_j)) for i, sublist in enumerate(coalition.assignments) if UAV_j in sublist][0][0]

            # A coalition different from the current coalition is randomly selected
            while Task_i == Original_coalition:
                Task_i = random.randint(0, len(Tasks) - 1)
            Coalition_new = copy.deepcopy(coalition)
            Coalition_new.assignments[Original_coalition].remove(UAV_j)
            Coalition_new.assignments[Task_i].append(UAV_j)

            # Compute the utility of the members within the coalition
            U_original = coalition.revenue_coalition(Original_coalition) + coalition.revenue_coalition(Task_i)
            U_new = Coalition_new.revenue_coalition(Original_coalition) + Coalition_new.revenue_coalition(Task_i)

            # If the UAV prefers the new coalition, the coalition partition is updated
            if U_original < U_new :
                coalition = Coalition_new

            Overall_utility = sum(coalition.revenue_coalition(i) for i in range(len(Tasks)))
            Iter_utility1.append(Overall_utility)
        return Iter_utility1

    def Selfish(self, UAVs, Tasks, alpha, iteration):
        # Create a new coalition object
        coalition = Coalition(UAVs, Tasks, alpha)
        Iter_utility2 = []

        # The iterative process of the algorithm
        for rounds in range(iteration):
            UAV_j = random.randint(0, len(UAVs) - 1)
            Task_i = random.randint(0, len(Tasks) - 1)
            Original_coalition = [(i, sublist.index(UAV_j)) for i, sublist in enumerate(coalition.assignments) if UAV_j in sublist][0][0]

            # A coalition different from the current coalition is randomly selected
            while Task_i == Original_coalition:
                Task_i = random.randint(0, len(Tasks) - 1)
            Coalition_new = copy.deepcopy(coalition)
            Coalition_new.assignments[Original_coalition].remove(UAV_j)
            Coalition_new.assignments[Task_i].append(UAV_j)

            # Compute the utility allocated in the two coalitions
            Shapley_original = coalition.shapley_value(Original_coalition)[coalition.assignments[Original_coalition].index(UAV_j)]
            Shapley_new = Coalition_new.shapley_value(Task_i)[Coalition_new.assignments[Task_i].index(UAV_j)]

            # If the UAV prefers the new coalition, the coalition partition is updated
            if Shapley_original < Shapley_new:
                coalition = Coalition_new

            Overall_utility = sum(coalition.revenue_coalition(i) for i in range(len(Tasks)))
            Iter_utility2.append(Overall_utility)

        return Iter_utility2

    def Pareto(self, UAVs, Tasks, alpha, iteration):
        # Create a new coalition object
        coalition = Coalition(UAVs, Tasks, alpha)
        Iter_utility3 = []

        # The iterative process of the algorithm
        for rounds in range(iteration):
            UAV_j = random.randint(0, len(UAVs) - 1)
            Task_i = random.randint(0, len(Tasks) - 1)
            Original_coalition = [(i, sublist.index(UAV_j)) for i, sublist in enumerate(coalition.assignments) if UAV_j in sublist][0][0]

            # A coalition different from the current coalition is randomly selected
            while Task_i == Original_coalition:
                Task_i = random.randint(0, len(Tasks) - 1)
            Coalition_new = copy.deepcopy(coalition)
            Coalition_new.assignments[Original_coalition].remove(UAV_j)
            Coalition_new.assignments[Task_i].append(UAV_j)

            # Compute the utility allocated in the two coalitions
            Shapley_original = coalition.shapley_value(Original_coalition)[coalition.assignments[Original_coalition].index(UAV_j)]
            Shapley_new = Coalition_new.shapley_value(Task_i)[Coalition_new.assignments[Task_i].index(UAV_j)]

            # Calculate the utility difference in the coalition
            delta1 = Coalition_new.revenue_coalition(Original_coalition) - coalition.revenue_coalition(Original_coalition)
            delta2 = Coalition_new.revenue_coalition(Task_i) - coalition.revenue_coalition(Task_i)

            # If the UAV prefers the new coalition, the coalition partition is updated
            if Shapley_original < Shapley_new and delta1 > 0 and delta2 > 0:
                coalition = Coalition_new

            Overall_utility = sum(coalition.revenue_coalition(i) for i in range(len(Tasks)))
            Iter_utility3.append(Overall_utility)

        return Iter_utility3

