#!/usr/bin/python3
# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # #
# Real-Time Systems Group
# Hunan University HNU
# Fang YJ
# # # # # # # # # # # # # # # #


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
import requests
import latexify
import itertools
import tracemalloc

import numpy as np
import pandas as pd
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

# import paramiko
# from z3.z3 import Int, Sum, If, Solver, Or, IntNumRef, Bool, And, Implies


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
