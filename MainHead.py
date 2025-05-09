#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
###################################
主 头文件整理；
###################################
"""

import re
import io
import os
import gc
import sys
import glob
import time
import json
import math
import copy
import mmap
import sympy
import shutil
import psutil
import pickle
import random
import hashlib
import sqlite3
import datetime
import paramiko
import requests
import itertools
import tracemalloc

import numpy as np
import pandas as pd
import pynauty as pn
import pathlib as plx
import seaborn as sns
import networkx as nx
import graphviz as gz
import matplotlib.pyplot as plt

from threading import Thread
from datetime import datetime
from scipy.sparse import csr_matrix
from scipy.ndimage import gaussian_filter1d
from scipy.sparse.csgraph import connected_components
from random import random, sample, uniform, randint
from collections import defaultdict, Counter, namedtuple
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait, as_completed
from multiprocessing import cpu_count, Pool, Manager, Event, Process, Queue, queues, current_process, Semaphore, Value
from itertools import chain, accumulate, groupby, product, zip_longest,  permutations, combinations, combinations_with_replacement


# from z3.z3 import Int, Sum, If, Solver, Or, IntNumRef, Bool, And, Implies


# # # # # # # # # # # # # # # #
# (1) combination
# A004250
# 1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176, 231, 297, 385, 490, 627, 792, 1002, 1255, 1575, 1958,
# 2436, 3010, 3718, 4565, 5604, 6842, 8349, 10143, 12310, 14883, 17977, 21637, 26015, 31185, 37338, 44583, 53174, 63261,
# 75175, 89134, 105558, 124754, 147273, 173525
# # # # # # # # # # # # # # # #
# def combination_exhaustion(node_num, shape_min=0, shape_max=float('Inf')):
#     ret_list = []
#     for local_n in range(max(shape_min, 1), min(node_num + 1, shape_max)):
#         input_node_num = node_num - local_n
#         if input_node_num == 0:
#             ret_list.append((node_num,))
#         else:
#             sat_list = combination_exhaustion(input_node_num, local_n, shape_max)
#             for sat_list_x in sat_list:
#                 ret_list.append((local_n,) + sat_list_x)
#     return ret_list

# # # # # # # # # # # # # # # #
# (2) permutation
# 输入 combination不同的组合；
# 根据组合合成不同的排序；
# 不同的组合一定无法得到同样的排列；
# # # # # # # # # # # # # # # #
# def permutation_exhaustion(combination_list):
#     ret_list = []
#     for combination_x in combination_list:
#         ret_list += list(set(itertools.permutations(combination_x, len(combination_x))))
#     return ret_list



# # # # # # # # # # # # # # # #
# (1) combination: A004250
# 1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176, 231, 297, 385, 490, 627, 792, 1002, 1255, 1575, 1958,
# 2436, 3010, 3718, 4565, 5604, 6842, 8349, 10143, 12310, 14883, 17977, 21637, 26015, 31185, 37338, 44583, 53174, 63261,
# 75175, 89134, 105558, 124754, 147273, 173525
# # # # # # # # # # # # # # # #
def Comb(_n:int, _s:tuple=(1, float('Inf')), _l:tuple=(1, float('Inf'))):
    _nsd, _nsu = max(1, _s[0]),                         min(_n, _s[1])
    _nld, _nlu = max(_l[0], 1, math.ceil(_n / _nsu)),   min(_l[1], _n, math.floor(_n / _nsd))
    if _nsd <= _nsu and _nld <= _nlu:
        if _nlu > 1:
            for _Xl in range(_nsd, math.floor(_nsu)):
                _Xp = _n - _Xl
                for _SubC in Comb(_Xp, (_Xl, min(_Xp, _nsu))):
                    yield _SubC + (_Xl,)
        if _nld == 1:
            if _nsd <= _n <= _nsu:
                yield (_n,)


# # # # # # # # # # # # # # # #
# (2) permutation 
# 输入 combination不同的组合；
# 根据组合合成不同的排序；
# 不同的组合一定无法得到同样的排列；
# # # # # # # # # # # # # # # #
def Perm(_c:tuple, _Xs:int=0, _id=float('Inf')):
    for _Xl in set(_c):
        if _Xl * _id >= _Xs:
            if len(_c) == 1:
                yield (_Xl,)
            elif len(_c) > 1:
                _tc = list(_c)
                _tc.remove(_Xl)
                for _SnbS in Perm(tuple(_tc), _Xl, _id):
                    yield _SnbS + (_Xl, )
            else:
                assert False



def shape_generation(_n: int, _lr: tuple, _sr: tuple):
    """ 尾结点数小者优先；"""
    if 1 <= _lr[0] <= _lr[1] and 1 <= _sr[0] <= _sr[1] and _lr[0] * _sr[0] <= _n <= _lr[1] * _sr[1]:
        for __X_l in range(_sr[0], _sr[1] + 1):
            __X_p = _n - __X_l
            __nlr = (max(1, _lr[0] - 1), min(_lr[1] - 1, __X_p))
            __nsr = (max(1, _sr[0]),     min(_sr[1],     __X_p))
            for __s_p in shape_generation(__X_p, __nlr, __nsr):
                yield __s_p + (__X_l, )
        if _lr[0] == 1 and _sr[0] <= _n <= _sr[1]:
            yield (_n, )



def shape_enumator(node_num, last_shape_num_list):
    reset_node_num = node_num - sum(last_shape_num_list)
    assert reset_node_num > 0
    if reset_node_num == 1:
        temp_new_last_shape_num_list = copy.deepcopy(last_shape_num_list)
        temp_new_last_shape_num_list.append(1)
        return [temp_new_last_shape_num_list]
    else:
        ret_list = []
        for slevel_node_num in range(1, reset_node_num):
            temp_new_last_shape_num_list = copy.deepcopy(last_shape_num_list)
            temp_new_last_shape_num_list.append(slevel_node_num)
            ret_list += shape_enumator(node_num, temp_new_last_shape_num_list)
        return ret_list
    

def exam_pic_show(dag_x, node_num, title):
    dot = gz.Digraph()
    dot.attr(rankdir='LR')
    for node_x in dag_x.nodes(data=True):
        temp_label = 'Node_ID:{0}'.format(str(node_x[0]))
        dot.node('%s' % node_x[0], temp_label, color='black')
    for edge_x in dag_x.edges():
        dot.edge('%s' % edge_x[0], '%s' % edge_x[1])
    # dot.view('./test.png')
    address = f'./generator_test/{node_num}/'
    os.makedirs(address, mode=0o777, exist_ok=True)
    # dot.view(address + f'{title}')
    dot.render(address + f'{title}', view=False)

