#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 21:25:09 2020

@author: yves

    This file is part of Saqqarah.

    Saqqarah is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Saqqarah is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Saqqarah.  If not, see <https://www.gnu.org/licenses/>
"""

class Parameters:
    # unit cm
    boxw = 2
    outw = 0
    boxh = 1
    outh = 0
    # pt
    linewidth = 5
    
    # cm related

    __resolution = 300

    units = {
            'cm' : 1,
            'mm':  1/10,
            'inch': 2.54,
            'pt': 2.54/72.27,
            # change it changing resolution
            'px': 2.54/__resolution
            }
    scale = 1
    unit = 'cm'
    
    def u(self, l, to_unit = None):
        """
        change value cm to unit
        """
        to_unit = to_unit or self.unit
        return l*self.scale/self.units[to_unit]
    
    def pt(self,val):
        """
        change from pt to unit
        used for text size
        """
        return round(self.u(val*2.54/72.27))

    @property
    def resolution(self):
        return self.__resolution

    @resolution.setter
    def resolution(self, r):
        # ignore if none
        try:
            r = int(r)
        except:
            return
        if r:
            self.__resolution = r
            self.units['px'] = 2.54/r
        
class PrinterCoordinates:
    """
    Automagicly change x et y properties to
    unit given by parameters class
    """
    def __init__(self, parameters):
        self.param = parameters
        self.shift = self.param.outw or self.param.outh

    def __str__(self):
        return f" {self.__x}, {self.__y} "

    def __iter__(self):
        yield self.__x
        yield self.__y
        
    __x = None
    __y = None
    __shift = False
    __shift_x = 0
    __shift_y = 0


    def __round__(self):
        return round(self.__x), round(self.__y)

    @property
    def shift(self):
        return self.__shift
    
    @shift.setter
    def shift(self, bool):
        self.__shift = bool
        if bool:
            self.__shift_x = self.param.u(self.param.outw)
            self.__shift_y = self.param.u(self.param.outh)
        else:
            self.__shift_x = 0
            self.__shift_y = 0
            

    @property
    def xy(self):
        return self.__x+self.__shift_x, self.__y + self.__shift_y
    
    @xy.setter
    def xy(self, coord):
        self.x = coord[0]
        self.y = coord[1]
        
    @property
    def x(self):
        return self.__x+self.__shift_x
    
    @x.setter
    def x(self, val):
        self.__x = self.param.u(val)
        
    @property
    def y(self):
        return self.__y+self.__shift_y

    @y.setter
    def y(self, val):
        self.__y = self.param.u(val)
        
