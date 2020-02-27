#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018 Topcoder Inc. All Rights Reserved.

@author: TCSCODER
"""
import numpy as np
import math


def degree_to_radian(degree):
    return math.pi/180.0*degree


def radian_to_degree(radian):
    return 180.0/math.pi*radian


def rotx(theta):
    return np.array([[1, 0, 0],
                     [0, np.cos(theta), -np.sin(theta)],
                     [0, np.sin(theta), np.cos(theta)]])


def roty(theta):
    return np.array([[np.cos(theta), 0, np.sin(theta)],
                     [0, 1, 0],
                     [-np.sin(theta), 0, np.cos(theta)]])


def rotz(theta):
    return np.array([[np.cos(theta), -np.sin(theta), 0],
                     [np.sin(theta), np.cos(theta), 0],
                     [0, 0, 1]])


if __name__ == '__main__':
    m = rotx(degree_to_radian(90))
    v = np.array([0.0, 1.0, 0.0])
    print(np.matmul(m, v))
