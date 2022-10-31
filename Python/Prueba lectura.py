# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 08:43:38 2022

@author: ivanm
"""


import numpy as np

raw_data = open('qDots.csv')
qDots = np.loadtxt(raw_data, delimiter=",",skiprows=1)

raw_data = open('qCircle.csv')
qCircle = np.loadtxt(raw_data, delimiter=",",skiprows=1)

raw_data = open('qDejado.csv')
qDejado = np.loadtxt(raw_data, delimiter=",",skiprows=1)

raw_data = open('qLetter.csv')
qLetter = np.loadtxt(raw_data, delimiter=",",skiprows=1)

raw_data = open('qPar.csv')
qPar = np.loadtxt(raw_data, delimiter=",",skiprows=1)

raw_data = open('qRecolecccion.csv')
qRecoleccion = np.loadtxt(raw_data, delimiter=",",skiprows=1)

raw_data = open('qTriangle.csv')
qTriangle = np.loadtxt(raw_data, delimiter=",",skiprows=1)

print(qDots.shape)
print(qDots)