# -*- coding: utf-8 -*-
"""
@Time ： 2023-09-13 9:59
@Auth ： XinpengLu
@File ：Myoolhelper.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import matplotlib.pyplot as plt
from Initialization import Initialization
from Solution import Solution
import numpy as np
import os
from configparser import ConfigParser
from matplotlib.backends.backend_pdf import PdfPages

class Toolhelper():
    'This class represents the useful tools used in the program'

    # This function configures initialization parameters
    def load_configuration(self):
        config_file_path = 'config.ini'
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"Config file '{config_file_path}' does not exist")

        conn = ConfigParser()
        conn.read(config_file_path)

        # Read the configuration file and assign values to the parameters
        N_UAV = int(conn.get('config', 'N_UAV'))
        N_Task = int(conn.get('config', 'N_Task'))
        alpha = float(conn.get('config', 'alpha'))
        iteration = int(conn.get('config', 'iteration'))
        iter_avg = int(conn.get('config', 'iter_avg'))

        return N_UAV, N_Task, alpha, iteration, iter_avg


    # This function is used to save images as pdf files
    def save_multi_image(self, filename):
        pp = PdfPages(filename)
        fig_nums = plt.get_fignums()
        figs = [plt.figure(n) for n in fig_nums]
        for fig in figs:
            fig.savefig(pp, format='pdf')
        pp.close()


    def plot_iteration(self, iteration, average, matrices):
        plt.rcParams['font.family'] = ['Arial']
        plt.figure(figsize=(6, 5), dpi=300)
        min_average = np.min(average)
        max_average = np.max(average)
        x_axis_data = range(iteration)

        labels = [
            r'MUCNC-CFG (r=0.6)',
            r'Selfish Order (r=0.6)',
            r'Pareto Order (r=0.6)'
        ]
        colors = ['#D62627', '#1974B2', '#289E28']

        for i in range(3):
            plt.plot(x_axis_data, average[i], c=colors[i], linestyle='-', linewidth=2,
                     label=labels[i])

        for i, matrix in enumerate(matrices):
            matrix_max = np.percentile(np.array(matrix), 60, axis=1)
            matrix_min = np.percentile(np.array(matrix), 40, axis=1)
            plt.fill_between(x_axis_data, matrix_min, matrix_max, color=colors[i], alpha=0.2)

        plt.grid(ls="--", lw=0.5)
        plt.xlabel('Iterations', fontsize=12)
        plt.ylabel('The overall utility', fontsize=12)
        plt.legend(loc='lower right', fontsize=12)
        plt.axis([-5, iteration+5, min_average - 0.5, max_average + 1])
        filename = "Fig6.pdf"
        self.save_multi_image(filename)

    def plot_Task(self, x_min, x_max, utility, index):
        plt.rcParams['font.family'] = ['Arial']
        plt.figure(figsize=(5, 5), dpi=300)
        min_utility = np.min(utility)
        max_utility = np.max(utility)

        x_axis_data = [i for i in range(x_min, x_max, 2)]
        labels = [
            r'MUCNC-CFG(r=0.5%)',
            r'Selfish Order(r=0.5%)',
            r'Pareto Order(r=0.5%)',
            r'MUCNC-CFG(r=1%)',
            r'Selfish Order(r=1%)',
            r'Pareto Order(r=1%)'
        ]
        colors = ['#D62627', '#FF7F0E', '#289E28', 'c', '#1974B2', '#966ABF']
        markers = ['D', 's', 'o']

        for i in range(len(utility)):
            plt.plot(x_axis_data, utility[i], c=colors[i], marker=markers[i % 3], linestyle='-', linewidth=2,
                     label=labels[i])

        plt.grid(axis='y', ls="--", lw=0.5)
        x_label = ['The number of tasks', 'The number of UAVs']
        plt.xlabel(x_label[index])
        plt.ylabel('The overall utility')
        plt.legend(loc='upper left', fontsize=12)
        plt.axis([x_min - 2, x_max, min_utility - 0.5, max_utility + 2])
        filename = x_label[index] + ".pdf"
        self.save_multi_image(filename)

    def set_tick_color(self, tick, color):
        tick.set_color(color)

    def plot_5(self, utility1, utility2):
        plt.rcParams['font.family'] = ['Arial']
        fig = plt.figure(figsize=(18, 7), dpi=100)
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)

        x_axis_data = [i for i in range(4, 20, 2)]

        min_utility1 = np.min(utility1)
        max_utility1 = np.max(utility1)
        min_utility2 = np.min(utility2)
        max_utility2 = np.max(utility2)

        labels = [
            r'MUCNC-CFG(r=0.6)',
            r'Selfish Order(r=0.6)',
            r'Pareto Order(r=0.6)',
            r'MUCNC-CFG(r=1)',
            r'Selfish Order(r=1)',
            r'Pareto Order(r=1)'
        ]
        colors = ['#D62627', '#FF7F0E', '#289E28', 'c', '#1974B2', '#966ABF']
        markers = ['D', 's', 'o']
        x_label = ['The number of tasks', 'The number of UAVs']

        # ax1
        for i in range(6):
            ax1.plot(x_axis_data, utility1[i], c=colors[i], marker=markers[i % 3], markersize=3,
                     linestyle='-', linewidth=1, label=labels[i])
        ax1.axis([2, 20, min_utility1 - 0.5, max_utility1 + 1.3])
        ax1.set_xlabel(x_label[0], fontsize=12)
        ax1.set_ylabel('The overall utility', fontsize=12)
        ax1.grid(ls="--", lw=0.5)
        ax1.legend(loc='lower right', ncol=1, fontsize=12)

        # ax2
        ax2.axvline(x=12, color='red', linestyle='--')
        ax2.axvline(x=14, color='red', linestyle='--')
        for i in range(6):
            ax2.plot(x_axis_data, utility2[i], c=colors[i], marker=markers[i % 3], markersize=3,
                     linestyle='-', linewidth=1, label=labels[i])

        xticks = [5, 10, 12, 14, 15, 20]
        xtick_labels = ['5', '10', '12', '14', '15', '20']
        ax2.set_xticks(xticks)
        ax2.set_xticklabels(xtick_labels)

        xtick_objects = ax2.get_xticklabels()

        self.set_tick_color(xtick_objects[0], 'black')
        self.set_tick_color(xtick_objects[1], 'black')
        self.set_tick_color(xtick_objects[2], 'red')
        self.set_tick_color(xtick_objects[3], 'red')
        self.set_tick_color(xtick_objects[4], 'black')
        self.set_tick_color(xtick_objects[5], 'black')

        ax2.axis([2, 20, min_utility2 - 0.5, max_utility2 + 1.3])
        ax2.set_xlabel(x_label[1], fontsize=14)
        ax2.set_ylabel('The overall utility', fontsize=14)
        ax2.grid(ls="--", lw=0.5)
        ax2.legend(loc='lower right', ncol=1, fontsize=12)
        filename = "2.pdf"
        self.save_multi_image(filename)

    def plot_alpha(self, alphas, utility):
        plt.rcParams['font.family'] = ['Arial']
        fig, axes = plt.subplots(1, 4, figsize=(16.5, 3.5), dpi=100)

        labels = [
            r'MUCNC-CFG',
            r'Selfish Order',
            r'Pareto Order',
        ]
        colors = ['#D62627', '#FF7F0E', '#289E28', 'c', '#1974B2', '#966ABF']
        markers = ['D', 's', 'o']

        for i, ax in enumerate(axes):
            for j in range(len(utility[i])):
                ax.plot(alphas * 10, utility[i][j], c=colors[j], marker=markers[j], linestyle='-', linewidth=2,
                        label=labels[j])
            ax.grid(ls="--", lw=0.5)
            ax.set_xlabel('r%')
            ax.set_ylabel('The sum of utility')
        lines, labels = fig.axes[-1].get_legend_handles_labels()
        fig.legend(lines, labels, loc='upper center', ncol=3)
        filename = "alpha.pdf"
        self.save_multi_image(filename)

    """
    This function is used to iterate over the algorithm for multiple rounds and average the results. 
    To simulate the real environment, we change the simulation scenario by inputting the number of 
    UAVs, the number of tasks and the value of alpha, and return the average utility of the algorithm 
    in each round of iteration.
    """

    def avg_algorithm(self, N_UAV, N_Task, alpha):
        average = [[] for _ in range(3)]
        averages = [[] for _ in range(3)]
        iter_avg = Initialization().iter_avg
        iters = Initialization().iteration

        for _ in range(iter_avg):
            Init = Initialization()
            Init.N_UAV = N_UAV
            Init.N_Task = N_Task
            solution_instance = Solution()
            UAV_init = Init.Init_UAV()
            Task_init = Init.Init_Task()
            average[0].append(solution_instance.Maiginal_utility(UAV_init, Task_init, alpha, iters))
            average[1].append(solution_instance.Selfish(UAV_init, Task_init, alpha, iters))
            average[2].append(solution_instance.Pareto(UAV_init, Task_init, alpha, iters))

        matrices = [np.matrix(avg).T for avg in average[:3]]

        # Calculate the average utility in each iteration
        for i in range(3):
            for j in range(iters):
                avg = sum(average[i][k][j] for k in range(iter_avg)) / iter_avg
                averages[i].append(avg)
        return averages, matrices

    def test1(self):
        iters = Initialization().iteration
        Init = Initialization()
        averages, matrices = self.avg_algorithm(Init.N_UAV, Init.N_Task, Init.alpha)

        self.plot_iteration(iters, averages, matrices)

    def test2(self):
        min_task = 4
        max_task = 20
        N_UAV = 20
        alpha1 = 0.06
        alpha2 = 0.1
        utility = [[] for _ in range(6)]
        for N_Task in range(min_task, max_task, 2):
            print('N_Task:', N_Task)
            average1 = self.avg_algorithm(N_UAV, N_Task, alpha1)[0]
            for i in range(3):
                utility[i].append(average1[i][-1])
            average2 = self.avg_algorithm(N_UAV, N_Task, alpha2)[0]
            for i in range(3):
                utility[i + 3].append(average2[i][-1])
        # self.plot_Task(min_task, max_task, utility, 0)
        return utility

    def test3(self):
        min_UAV = 4
        max_UAV = 20
        N_Task = 4
        alpha1 = 0.06
        alpha2 = 0.1
        utility = [[] for _ in range(6)]

        for N_UAV in range(min_UAV, max_UAV, 2):
            average1 = self.avg_algorithm(N_UAV, N_Task, alpha1)[0]
            for i in range(3):
                utility[i].append(average1[i][-1])
            average2 = self.avg_algorithm(N_UAV, N_Task, alpha2)[0]
            for i in range(3):
                utility[i + 3].append(average2[i][-1])
        # self.plot_Task(min_UAV, max_UAV, utility, 1)
        return utility

    def test4(self):
        N_UAV = [20, 20, 20, 20]
        N_Task = [15, 15, 15, 15]
        alphas = np.arange(0.04, 0.101, 0.01)
        utility = [[[] for _ in range(3)] for _ in range(4)]

        for alpha in alphas:
            for i in range(4):
                average = self.avg_algorithm(N_UAV[i], N_Task[i], alpha)[0]
                for j in range(3):
                    utility[i][j].append(average[j][-1])
        self.plot_alpha(alphas, utility)

    def test5(self):
        utility1 = self.test2()
        utility2 = self.test3()
        self.plot_5(utility1, utility2)
