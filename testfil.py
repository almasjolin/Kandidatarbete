# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 15:34:47 2026

@author: idagu
"""

import testgenerator
from ILP import solve_ilp
from maskintilldelning import maskintilldelning

T,t = solve_ilp(*testgenerator.testgenerator(5,10,20 ))
