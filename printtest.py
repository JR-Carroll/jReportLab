#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
PrintTest is a one-trick-pony for ReportLab - it prints an on-the-fly PDf 
with all the ReportLab colors that are in shapes.colors.  

The list of available colors certainly isn't exhaustive, but it _is_ 
comprehensive enough to do quick printer check to see which colors print
to your desired standards (whether you are printing in color or in grayscale).

There are no options to modify, simply run the script, and check your source 
folder for the generated PDF (which should be called "grid_print.pdf").  

The main purpose of this script originated from needing to print ECG strip 
charts (very precise grids used as the coordinate graphing chart paper for 
ECG heart rhythms).  Original attempts to print produced odd prints, but
beautiful charts on the screen.  Confused, we finally tracked down the 
discrepancy to the types of colors we were using in the charts - our printers
were printing in grayscale and the formulas used to convert colors to 
grayscale were also producing antialiasing side-effects that printed
"patternesque" (plaid) at the printer.  To approach a solution, this script
was drafted to produce all colors showing a small strip chart and what the
result would look like at the printer and on the screen so we could select
the best color to match our needs!
'''

__author__ = 'J. R. Carroll'
__copyright__ = 'Copyright 2012'
__credits__ = 'J. R. Carroll'

__maintainer__ = 'J. R. Carroll <jrcarroll@jrcresearch.net'
__email__ = 'jrcarroll@jrcresearch.net'
__status__ = 'production'

import reportlab.pdfgen.canvas as canvas
import reportlab.graphics.shapes as shapes

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import LETTER
from reportlab.graphics import renderPDF

__all_colors__ = shapes.colors.getAllNamedColors()
__style_sheets__ = getSampleStyleSheet()
__margin__ = 40
__gutter__ = 15

class Grid_test():
    """Makes a small grid for test printing using the color specified.
    
    A class was decided on over a function because of the techniques
    used by ReportLab to 'paint' objects to the canvas.  Since this script
    is not taking advantage of 'flowables', it was necessary to control the
    flow of elements being painted - the only way to do that was to create 
    a class.
    
    To create a Grid_test() object, you can do the following:
    
    Ex:
       Grid_test(colorIndex=(color, __all_colors__.get(color)), dimensions=grid_dim)
        
    
    The following parameters are allowed when creating a new grid:
    
    dimensions
        Should be a tuple with values representing the dimensions of the grid.
    
    colorIndex
        Should be a tuple representing the color name, and the dictionary call.
        You should not have to adjust this!
    
    scale
        If you want to build a grid using different dimensions you can pass
        your own scale adjustment.
        
    minor_grid
        Adjust this value if you want to alter the stroke of the minor grid 
        lines (default is set to "0" which is PostScript magic for the smallest
        stroke possible.
    
    major_grid
        Adjust this value if you want to alter the stroke of the major grid
        lines (default is set to .3).
    """
    
    def __init__(self, colorIndex=(None, None), dimensions=(None, None), 
                 scale=1*mm, minor_grid=0, major_grid=.3):
        self.iCanvas = shapes.Drawing()
        self.colorName = colorIndex[0]
        self.colorRGB = colorIndex[1]
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.grid_size = scale
        self.grid_minor = minor_grid
        self.grid_major = major_grid
            
    def draw_grid(self):
        """Draws my grid!"""
        
        # Draw vertical lines first!
        _h = self.height*self.grid_size
        _w = self.width*self.grid_size
         
        for i in range(0, self.width, 1):
            l = i*self.grid_size
            if (i % 5.0 == 0):
                self.iCanvas.add(shapes.Line(l, 0, l, _h, 
                                             strokeWidth=self.grid_major, 
                                             strokeColor=self.colorRGB))
            else:    
                self.iCanvas.add(shapes.Line(l, 0, l, _h, 
                                             strokeWidth=self.grid_minor,
                                             strokeColor=self.colorRGB))
    
        # Draw horizontal lines next!
        
        for n in range(0, self.height, 1):
            l = n*self.grid_size            
            if (n % 5.0 == 0):
                self.iCanvas.add(shapes.Line(0, l, _w, l, 
                                             strokeWidth=self.grid_major, 
                                             strokeColor=self.colorRGB))
            else:   
                self.iCanvas.add(shapes.Line(0, l, _w, l, 
                                             strokeWidth=self.grid_minor,
                                             strokeColor=self.colorRGB))
                
        return self.iCanvas
        
page = canvas.Canvas("grid_print.pdf", pagesize=LETTER)

aW = LETTER[0]-__margin__
aH = LETTER[1]-__margin__

top_start = [__margin__, aH-__margin__]

startX = 0 + __margin__
startY = 0 + __margin__
advX = startX + __gutter__
advY = startY + __gutter__
maxX = aW - (__margin__*2) 
maxY = aH - (__margin__*2)

grid_dim = (40, 10)

_wide = 4
_tall = 11

# Manual removal of values from the dictionary that are not colors used.
del __all_colors__['_CMYK_black']
del __all_colors__['_PCMYK_white']
del __all_colors__['_CMYK_white']
del __all_colors__['_PCMYK_black']
  
for color in __all_colors__:
    v = Grid_test(colorIndex=(color, __all_colors__.get(color)), dimensions=grid_dim)
    color_Info = [str(color).capitalize(), str(__all_colors__.get(color))]
    page.setFontSize(7)
    
    if _tall >= 0:
        if _wide >= 1:
            renderPDF.draw(v.draw_grid(), page, top_start[0], top_start[1])
            page.drawString(top_start[0], (top_start[1]-11), color_Info[0])
            page.drawString(top_start[0], (top_start[1]-20), color_Info[1])
            top_start[0] += 142
            _wide += -1
        
        elif _wide == 0:
            if _tall == 0:
                _wide = 4
                _tall = 12
                page.showPage()
                page.setFontSize(7)
                _tall = 11
                _wide = 4
                top_start = [__margin__, aH-__margin__]
                
                renderPDF.draw(v.draw_grid(), page, top_start[0], top_start[1])
                page.drawString(top_start[0], (top_start[1]-11), color_Info[0])
                page.drawString(top_start[0], (top_start[1]-20), color_Info[1])
                top_start[0] += 142
                _wide += -1
                
            else:
                _tall += -1
            
                top_start[0] = __margin__
                top_start[1] += -60
                
                renderPDF.draw(v.draw_grid(), page, top_start[0], top_start[1])
                page.drawString(top_start[0], (top_start[1]-11), color_Info[0])
                page.drawString(top_start[0], (top_start[1]-20), color_Info[1])
                top_start[0] += 142
            
                _wide += 3
            
    else:
        pass

page.save()
print("GEOJ")





