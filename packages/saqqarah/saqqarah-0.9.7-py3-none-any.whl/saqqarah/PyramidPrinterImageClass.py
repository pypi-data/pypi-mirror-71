#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 13:01:37 2020

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

from . import PyramidPrinter
from . import PrinterCoordinates
from . import filename_prepare, ensure_attr
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from time import strftime
    
def get_size_from_param(param):
    # param.unit is already set to pixel ?

    size = PrinterCoordinates(param)
    size.xy =  ( param.size * param.boxw + 2*param.outw,
                 param.size * param.boxh + 2*param.outh
                 )

    return round(size)

def center_text(draw, bounding_box, msg, *, font=None, fill='black'):
    x1, y1, x2, y2 = bounding_box

    # Calculate the width and height of the text to be drawn, given font size
    w, h = draw.textsize(msg, font=font)
    
    # Calculate the mid points and offset by the upper left corner of the bounding box
    x = (x2 - x1 - w)/2 + x1
    y = (y2 - y1 - h)/2 + y1

    # Write the text to the image, where (x,y) is the top left corner of the text
    draw.text((x, y), msg, align='center', font=font, fill=fill)
    
class PyramidPrinterImage(PyramidPrinter):
    """
    Implements prining as image
    """
    def __init__(self, pyramid):
        super().__init__(pyramid)
        Image.init()
        self.param.unit = 'px'
        self.param.outw = 1
        self.param.outh = 1
        # introspection
        # needed to load the ttf font file
        my_path = Path(__loader__.path).parent
        # ttf font file. 
        self.param.ttf_file = Path(my_path, 'fonts', 'AerialBd.ttf')
        self.param.memory_images=False
        self.param.images = {}
        
    def get_images(self):
        return self.param.images
            
    class PrinterCM(PyramidPrinter.PrinterCM):
        def __init__(self, param):
            self.param = param

            timestamp = strftime('-%Y%m%dT%H%M%S')
            ensure_attr(self.param, 'filename', f"pyramid{timestamp}")
            ext = 'png' if 'PNG' in Image.SAVE else list(Image.SAVE.keys())[0].lower()

            self.param.basename, self.param.extension = filename_prepare(self.param.filename, Image.SAVE, ext)
            self.param.images = {}
            
        def __enter__(self):
            return self
        
        def __exit__(self, *args):
            pass
        
    class PyramidCM(PyramidPrinter.PyramidCM):
        def __init__(self, param):
            self.param = param
            basename = self.param.basename
            extension = self.param.extension
            stream = self.param.stream.lower()
            self.filename = str(Path(self.param.directory, f"{basename}-{stream}.{extension}"))
            self.im_size = get_size_from_param(param)
            
        def __enter__(self):
            # Create blank rectangle to write on
            # round return a tuple of rounded values
            self.image = Image.new('RGB', self.im_size, 'white')
            self.draw = ImageDraw.Draw(self.image)
            return self
        
        def __exit__(self, *args):
            # self.image.show()
            if not self.param.memory_images:
                self.image.save(self.filename)  
                self.param.log(f"Saved image {self.filename}.")
            else:
                self.param.images[self.param.stream.lower()] = self.image

    def print_pyramid(self, param):
        for i in range(param.size):
            y = i 
            self.__print_line__(y, i+1, param)

    def __print_line__(self, y, no, param):
        for x in range(param.size-no,param.size+no,2):
            self.__print_box__(x,y, param)
            self.__print_node__(x,y, param)
            
    def __print_box__(self, x, y, param):
        draw = param.pyramid_printer.draw
        c1, c3, = (PrinterCoordinates(param) for c in range(2))
        c1.xy = x, y
        c3.xy = x + param.boxw, y + param.boxh
        # width 5 pt
        # TODO: add a parameter
        width = round(self.param.pt(2))
        draw.rectangle([c1.x, c1.y, c3.x, c3.y], outline='black', width=width)

    def __print_node__(self, x, y, param):
        if not param.values:
            return
        value = param.values.pop()
        if value == "_":
            return
        draw = param.pyramid_printer.draw
        
        c1, c2 = (PrinterCoordinates(param) for c in range(2))
        c1.xy = x, y
        c2.xy = x + param.boxw, y + param.boxh
        
        # puzzle
        if type(value) is str:
            color='red'
        else:
            color='black'
        
        fontsize = param.pt(10)
        font = ImageFont.FreeTypeFont(str(self.param.ttf_file), size=fontsize, index=0, encoding="")
        
        center_text(draw, [c1.x, c1.y, c2.x, c2.y], str(value), font=font, fill=color)
    

    