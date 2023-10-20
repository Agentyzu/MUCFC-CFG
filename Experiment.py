# -*- coding: utf-8 -*-
"""
@Time ： 2023-09-06 13:19
@Auth ： XinpengLu
@File ：experiment.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""

import matplotlib.pyplot as plt
import math
import random
import copy
from itertools import combinations

# 联盟工作能力
def Sum_efficency(Coalition, i):
    if len(Coalition[i]) != 0:
        return sum(UAV_Efficiency[j] for j in Coalition[i])
    else:
        return 0

# 联盟完成任务时间
def Time_coalition(Coalition, i):
    if len(Coalition[i]) != 0:
        return Task_Q[i] / Sum_efficency(Coalition, i)
    else:
        return 0

# 联盟完成任务成本
def Cost_coalition(Coalition, i):
    return Time_coalition(Coalition, i) * len(Coalition[i]) * alpha

# 联盟完成任务收益
def Revenue_coalition(Coalition, i):
    if len(Coalition[i]) != 0:
        if Sum_efficency(Coalition, i) < Task_beta[i]:
            return Task_Value[i] * Sum_efficency(Coalition, i) / Task_beta[i]
        elif Sum_efficency(Coalition, i) < Task_p[i]:
            return Task_Value[i] * (Sum_efficency(Coalition, i) - Task_p[i]) / (Task_beta[i] - Task_p[i])
        else:
            return 0
    else:
        return 0

# 联盟完成任务效用
def Utility_coalition(Coalition, i):
    return Revenue_coalition(Coalition, i) - Cost_coalition(Coalition, i)

# for i in range(N_Task):
#     print(Utility_coalition(Coalition, i))

# 计算联盟i中无人机j的边际贡献
def marginal_contribution(i, j, coalition):
    coalition_copy1 = copy.deepcopy(Coalition)
    coalition_copy1[i] = coalition
    coalition_copy1 = copy.deepcopy(coalition_copy1)
    coalition_copy2 = copy.deepcopy(coalition_copy1)
    coalition_copy2[i].remove(j)
    return Utility_coalition(coalition_copy1, i) - Utility_coalition(coalition_copy2, i)

# 计算联盟效用
def Shapley_value(Coalition, i):
    num = len(Coalition[i])
    shapley_values = [0 for _ in range(num)]
    for j in Coalition[i]:
        for coalition_size in range(1, num + 1):
            for coalition in combinations(Coalition[i], coalition_size):
                if j not in coalition:
                    continue
                w = math.factorial(coalition_size - 1) * math.factorial(num - coalition_size) / math.factorial(num)
                shapley_values[Coalition[i].index(j)] += w * marginal_contribution(i, j, list(coalition))
    return shapley_values

# 初始化无人机和任务参数
N_UAV = 10
N_Task = 5
alpha = 0.01
alpha2 = 0.02
iteration = 5
iteravg = 3
Iter_utility1 = [[] for _ in range(iteration)]
Iter_utility2 = [[] for _ in range(iteration)]
Iter_utility3 = [[] for _ in range(iteration)]

# Marginal utility order
for iter in range(iteravg):
    Task_Value = [random.uniform(5, 10) for _ in range(N_Task)]
    Task_Q = [random.uniform(5, 10) for _ in range(N_Task)]
    Task_beta = [random.uniform(2, 3) for _ in range(N_Task)]
    Task_p = [random.uniform(5, 6) for _ in range(N_Task)]
    print('Task_p:', Task_p)

    UAV_Efficiency = [random.uniform(0.5, 1) for _ in range(N_UAV)]
    UAV_Utiliity = [0 for _ in range(N_UAV)]

    # 随机生成初始联盟
    S = [random.randint(0, N_Task - 1) for _ in range(N_UAV)]
    Coalition = [[] for _ in range(N_Task)]
    for i in range(N_UAV):
        Coalition[S[i]].append(i)
    print(Coalition)
    print('efficiency:', [Sum_efficency(Coalition, i) for i in range(N_Task)])

    # 输出当前联盟下所有无人机分配到的效用值
    for i in range(N_Task):
        item = Shapley_value(Coalition, i)
        for j in Coalition[i]:
            UAV_Utiliity[j] = item[Coalition[i].index(j)]
        print(Utility_coalition(Coalition, i))

    print(UAV_Utiliity)

    for rounds in range(iteration):
        UAV_j = random.randint(0, N_UAV - 1)  # 随机选出一架无人机
        print('随机选出的无人机：' + str(UAV_j))

        Task_i = random.randint(0, N_Task - 1)  # 随机选出一个任务
        Original_coalition = [(i, sublist.index(UAV_j)) for i, sublist in enumerate(Coalition) if UAV_j in sublist][0][0]
        while Task_i == Original_coalition:
            Task_i = random.randint(0, N_Task - 1)
        print('随机选出的任务：' + str(Task_i))

        # 得到新联盟（转换操作）
        Coalition_new = copy.deepcopy(Coalition)
        Coalition_new[Original_coalition].remove(UAV_j)
        Coalition_new[Task_i].append(UAV_j)
        print('Coalition:', Coalition)
        print('NEW Coalition:', Coalition_new)

        # 计算边际效用
        Shapley_original = Shapley_value(Coalition, Original_coalition)[Coalition[Original_coalition].index(UAV_j)]
        Shapley_new = Shapley_value(Coalition_new, Task_i)[Coalition_new[Task_i].index(UAV_j)]
        print('Shapley_original:', Shapley_original)
        print('Shapley_new:', Shapley_new)

        # 计算离开联盟和加入联盟的效用
        delta1 = Revenue_coalition(Coalition_new, Original_coalition) - Revenue_coalition(Coalition, Original_coalition)
        delta2 = Revenue_coalition(Coalition_new, Task_i) - Revenue_coalition(Coalition, Task_i)
        print('delta1:', delta1)
        print('delta2:', delta2)

        # 基于marginal utility顺序计算效用值
        U_original = Revenue_coalition(Coalition, Original_coalition) + Revenue_coalition(Coalition, Task_i)
        U_new = Revenue_coalition(Coalition_new, Original_coalition) + Revenue_coalition(Coalition_new, Task_i)

        print('original:', U_original)
        print('new:', U_new)

        if U_original < U_new :
            Coalition = Coalition_new

        print(Coalition)

        Overall_utility = [sum(Revenue_coalition(Coalition, i) for i in range(N_Task))][0]
        Iter_utility1[rounds].append(Overall_utility)

# Selfish Order
for iter in range(iteravg):
    Task_Value = [random.uniform(5, 10) for _ in range(N_Task)]
    Task_Q = [random.uniform(5, 10) for _ in range(N_Task)]
    Task_beta = [random.uniform(2, 3) for _ in range(N_Task)]
    Task_p = [random.uniform(5, 6) for _ in range(N_Task)]

    UAV_Efficiency = [random.uniform(0.5, 1) for _ in range(N_UAV)]
    UAV_Utiliity = [0 for _ in range(N_UAV)]

    # 随机生成初始联盟
    S = [random.randint(0, N_Task - 1) for _ in range(N_UAV)]
    Coalition = [[] for _ in range(N_Task)]
    for i in range(N_UAV):
        Coalition[S[i]].append(i)

    # 输出当前联盟下所有无人机分配到的效用值
    for i in range(N_Task):
        item = Shapley_value(Coalition, i)
        for j in Coalition[i]:
            UAV_Utiliity[j] = item[Coalition[i].index(j)]

    for rounds in range(iteration):
        UAV_j = random.randint(0, N_UAV - 1)  # 随机选出一架无人机

        Task_i = random.randint(0, N_Task - 1)  # 随机选出一个任务
        Original_coalition = [(i, sublist.index(UAV_j)) for i, sublist in enumerate(Coalition) if UAV_j in sublist][0][0]
        while Task_i == Original_coalition:
            Task_i = random.randint(0, N_Task - 1)

        # 得到新联盟（转换操作）
        Coalition_new = copy.deepcopy(Coalition)
        Coalition_new[Original_coalition].remove(UAV_j)
        Coalition_new[Task_i].append(UAV_j)

        # 计算边际效用
        Shapley_original = Shapley_value(Coalition, Original_coalition)[Coalition[Original_coalition].index(UAV_j)]
        Shapley_new = Shapley_value(Coalition_new, Task_i)[Coalition_new[Task_i].index(UAV_j)]

        if Shapley_original < Shapley_new:
            Coalition = Coalition_new

        Overall_utility = [sum(Revenue_coalition(Coalition, i) for i in range(N_Task))][0]
        Iter_utility2[rounds].append(Overall_utility)

# Pareto Order
for iter in range(iteravg):
    Task_Value = [random.uniform(5, 10) for _ in range(N_Task)]
    Task_Q = [random.uniform(5, 10) for _ in range(N_Task)]
    Task_beta = [random.uniform(2, 3) for _ in range(N_Task)]
    Task_p = [random.uniform(5, 6) for _ in range(N_Task)]

    UAV_Efficiency = [random.uniform(0.5, 1) for _ in range(N_UAV)]
    UAV_Utiliity = [0 for _ in range(N_UAV)]

    # 随机生成初始联盟
    S = [random.randint(0, N_Task - 1) for _ in range(N_UAV)]
    Coalition = [[] for _ in range(N_Task)]
    for i in range(N_UAV):
        Coalition[S[i]].append(i)

    # 输出当前联盟下所有无人机分配到的效用值
    for i in range(N_Task):
        item = Shapley_value(Coalition, i)
        for j in Coalition[i]:
            UAV_Utiliity[j] = item[Coalition[i].index(j)]

    for rounds in range(iteration):
        UAV_j = random.randint(0, N_UAV - 1)  # 随机选出一架无人机

        Task_i = random.randint(0, N_Task - 1)  # 随机选出一个任务
        Original_coalition = [(i, sublist.index(UAV_j)) for i, sublist in enumerate(Coalition) if UAV_j in sublist][0][0]
        while Task_i == Original_coalition:
            Task_i = random.randint(0, N_Task - 1)

        # 得到新联盟（转换操作）
        Coalition_new = copy.deepcopy(Coalition)
        Coalition_new[Original_coalition].remove(UAV_j)
        Coalition_new[Task_i].append(UAV_j)

        # 计算边际效用
        Shapley_original = Shapley_value(Coalition, Original_coalition)[Coalition[Original_coalition].index(UAV_j)]
        Shapley_new = Shapley_value(Coalition_new, Task_i)[Coalition_new[Task_i].index(UAV_j)]

        # 计算离开联盟和加入联盟的效用
        delta1 = Revenue_coalition(Coalition_new, Original_coalition) - Revenue_coalition(Coalition, Original_coalition)
        delta2 = Revenue_coalition(Coalition_new, Task_i) - Revenue_coalition(Coalition, Task_i)

        if Shapley_original < Shapley_new and delta1 > 0 and delta2 > 0:
            Coalition = Coalition_new

        Overall_utility = [sum(Revenue_coalition(Coalition, i) for i in range(N_Task))][0]
        Iter_utility3[rounds].append(Overall_utility)

print(Iter_utility1)
average_list1 = [sum(sublist) / len(sublist) for sublist in Iter_utility1]
print(average_list1)
average_list2 = [sum(sublist) / len(sublist) for sublist in Iter_utility2]
print(average_list2)
average_list3 = [sum(sublist) / len(sublist) for sublist in Iter_utility3]
print(average_list3)

# print(average_list)
plt.figure(figsize=(5, 5.5), dpi=150)
plt.axis([0, iteration, 20, 26])
x_axis_data = [i for i in range(0, iteration)]
plt.plot(x_axis_data, average_list1, c='r', marker='o', linestyle='-', linewidth=1, label=r'MUCNC-CFG($\alpha$=0.01)')
plt.plot(x_axis_data, average_list2, c='b', marker='o', linestyle='-', linewidth=1, label=r'Selfish Order($\alpha$=0.01)')
plt.plot(x_axis_data, average_list3, c='g', marker='o', linestyle='-', linewidth=1, label=r'Pareto Order($\alpha$=0.01)')

plt.grid(axis='y', ls="--", lw=0.5)
plt.xlabel('Iterations')
plt.ylabel('The sum of utility')
plt.legend(loc='upper left')
plt.show()
