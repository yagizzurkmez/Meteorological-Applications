#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 21:20:34 2024

@author: yagizcanurkmez
"""

#Taylor Diagram for multiple models and different regions

# TAYLOR DIAGRAM  -----------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.projections import PolarAxes
import mpl_toolkits.axisartist.grid_finder as gf
import mpl_toolkits.axisartist.floating_axes as fa


class TaylorDiagram(object):
  def __init__(self, STD ,fig=None, rect=111, label='_'):
    self.STD = STD
    tr = PolarAxes.PolarTransform()
    # Correlation labels
    rlocs = np.concatenate(((np.arange(11.0) / 10.0), [0.95, 0.99]))
    tlocs = np.arccos(rlocs) # Conversion to polar angles
    gl1 = gf.FixedLocator(tlocs) # Positions
    tf1 = gf.DictFormatter(dict(zip(tlocs, map(str, rlocs))))
    # Standard deviation axis extent
    self.smin = 0
    self.smax = 3 * self.STD
    gh = fa.GridHelperCurveLinear(tr,extremes=(0,(np.pi/2),self.smin,self.smax),grid_locator1=gl1,tick_formatter1=tf1,)
    if fig is None:
      fig = plt.figure()
    ax = fa.FloatingSubplot(fig, rect, grid_helper=gh)
    fig.add_subplot(ax)
    # Angle axis
    ax.axis['top'].set_axis_direction('bottom')
    ax.axis['top'].label.set_text("Correlation coefficient")
    ax.axis['top'].toggle(ticklabels=True, label=True)
    ax.axis['top'].major_ticklabels.set_axis_direction('top')
    ax.axis['top'].label.set_axis_direction('top')
    # X axis
    ax.axis['left'].set_axis_direction('bottom')
    ax.axis['left'].label.set_text("Standard deviation")
    ax.axis['left'].toggle(ticklabels=True, label=True)
    ax.axis['left'].major_ticklabels.set_axis_direction('bottom')
    ax.axis['left'].label.set_axis_direction('bottom')
    # Y axis
    ax.axis['right'].set_axis_direction('top')
    ax.axis['right'].label.set_text("Standard deviation")
    ax.axis['right'].toggle(ticklabels=True, label=True)
    ax.axis['right'].major_ticklabels.set_axis_direction('left')
    ax.axis['right'].label.set_axis_direction('top')
    # Useless
    ax.axis['bottom'].set_visible(False)
    # Contours along standard deviations
    ax.grid()
    self._ax = ax # Graphical axes
    self.ax = ax.get_aux_axes(tr) # Polar coordinates
    # Add reference point and STD contour
    l , = self.ax.plot([0], self.STD, 'k*', ls='', ms=12, label=label)
    l1 , = self.ax.plot([0], self.STD, 'k*', ls='', ms=12, label=label)
    t = np.linspace(0, (np.pi / 2.0))
    t1 = np.linspace(0, (np.pi / 2.0))
    r = np.zeros_like(t) + self.STD
    r1 = np.zeros_like(t) + self.STD
    self.ax.plot(t, r, 'k--', label='_')
    # Collect sample points for latter use (e.g. legend)
    self.samplePoints = [l]
    self.samplePoints = [l1]
  def add_sample(self,STD,r,*args,**kwargs):
    l,= self.ax.plot(np.arccos(r), STD, *args, **kwargs) # (theta, radius)
    self.samplePoints.append(l)
    return l

  def add_sample(self,STD,r1,*args,**kwargs):
    l1,= self.ax.plot(np.arccos(r1), STD, *args, **kwargs) # (theta, radius)
    self.samplePoints.append(l1)
    return l1

  def add_contours(self,levels=5,**kwargs):
    rs, ts = np.meshgrid(np.linspace(self.smin, self.smax), np.linspace(0, (np.pi / 2.0)))
    RMSE=np.sqrt(np.power(self.STD, 2) + np.power(rs, 2) - (2.0 * self.STD * rs  *np.cos(ts)))
    contours = self.ax.contour(ts, rs, RMSE, levels, **kwargs)
    return contours


import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

def srl(obsSTD, s,r,l):
    
  fig=plt.figure(figsize=(15,15))
  
  dia=TaylorDiagram(obsSTD, fig=fig, rect=111, label='ref')
  plt.clabel(dia.add_contours(colors='#808080'), inline=1, fontsize=10)

  region_marker_dict = {l[0]: 'o', l[1]: '^',l[2]:"v"} #ADD markers for more regions
  mec_values = ['red', 'blue', 'purple',"orange"] #ADD colors for more models
  legend_names = ["Model1","Model2","Model3","Model4"]
  
  

    # Iterate over the data and plot points
  for label, s_list, r_list in zip(l, s, r):
      for model_num, (s_val, r_val) in enumerate(zip(s_list, r_list), start=1):
          marker = region_marker_dict[label]  # Use marker from the dictionary based on the region
          mec = mec_values[model_num - 1]  # Use red, blue, or purple based on the model
          dia.add_sample(s_val, r_val, label=label, marker=marker, mec=mec, mfc='none', mew=2)


    
  spl = [p.get_label() for p in dia.samplePoints]
  # fig.legend(dia.samplePoints, spl, numpoints=1, prop=dict(size='small'), loc=[0.8,0.7
                                                                               
  #                                                                              ])
  #ADD legend manually for model Names
  patch1 = mpatches.Patch(color=mec_values[0], label=legend_names[0])
  patch2 = mpatches.Patch(color=mec_values[1], label=legend_names[1])
  patch3 = mpatches.Patch(color=mec_values[2], label=legend_names[2])
  patch4 = mpatches.Patch(color=mec_values[3], label=legend_names[3])
  line1 = Line2D([0], [0], marker='o', color='black', label=l[0],markersize=9)
  line2 = Line2D([0], [0], marker='^', color='black', label=l[1],markersize=9)
  line3 = Line2D([0], [0], marker='v', color='black', label=l[2],markersize=9)
  line4 = Line2D([1], [1], marker='*', color='black', label="Reference",linestyle="",markersize=15)
  fig.legend(handles=[patch1,patch2,patch3,patch4,line1,line2,line3,line4],loc=[0.8,0.7])
  plt.show()
  

obsSTD = 7


# Values
l = ['WCE & NEU',"MED", "EU"]
s= [0.2,0.5,4,5],[0.3,0.7,10,2],[0.1,3,7,5] # first bracelet defines region and first value of each bracelet comes from model1 and then model2 ...
r= [0.4,0.6,0.8,0.1],[0.2,0.3,0.7,0.2],[0.3,0.6,0.4,-0.1]


srl(obsSTD, s,r,l)