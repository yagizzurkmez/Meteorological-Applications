#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 21:20:34 2024

@author: yagizcanurkmez
taken from Nimantha source : https://stackoverflow.com/questions/67907069/label-taylor-diagram-with-number-by-python
"""

#Taylor Diagram for multiple models and different regions
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.projections import PolarAxes
import mpl_toolkits.axisartist.grid_finder as gf
import mpl_toolkits.axisartist.floating_axes as fa
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

class TaylorDiagram(object):
    def __init__(self, STD, fig=None, rect=111, label='Reference 1'):
        self.STD = STD
        tr = PolarAxes.PolarTransform()

        rlocs = np.concatenate((np.linspace(-1, 1, 21), [-0.99, -0.95, 0.95, 0.99]))
        rlocs = np.clip(rlocs, -1, 1)
        tlocs = np.arccos(rlocs)
        gl1 = gf.FixedLocator(tlocs)
        tf1 = gf.DictFormatter(dict(zip(tlocs, map(str, np.round(rlocs, 2)))))

        self.smin = 0
        self.smax = 3 * self.STD
        gh = fa.GridHelperCurveLinear(
            tr, extremes=(0, np.pi, self.smin, self.smax),
            grid_locator1=gl1, tick_formatter1=tf1
        )

        if fig is None:
            fig = plt.figure()
        ax = fa.FloatingSubplot(fig, rect, grid_helper=gh)
        fig.add_subplot(ax)

        ax.axis['top'].set_axis_direction('bottom')
        ax.axis['top'].label.set_text("Correlation coefficient")
        ax.axis['top'].toggle(ticklabels=True, label=True)
        ax.axis['top'].major_ticklabels.set_axis_direction('top')
        ax.axis['top'].label.set_axis_direction('top')

        ax.axis['left'].set_axis_direction('bottom')
        ax.axis["left"].label.set_text("Standard deviation")
        ax.axis['left'].toggle(ticklabels=True, label=True)
        ax.axis['left'].major_ticklabels.set_axis_direction('left')
        ax.axis['left'].label.set_rotation(360)
        ax.axis['left'].label.set_verticalalignment('center')
        ax.axis['left'].label.set_horizontalalignment('right')

        ax.axis['right'].set_axis_direction('top')
        ax.axis["right"].label.set_text("Standard deviation")
        ax.axis['right'].toggle(ticklabels=True, label=True)
        ax.axis['right'].major_ticklabels.set_axis_direction('left')
        ax.axis['right'].label.set_axis_direction('top')
        ax.axis['right'].label.set_rotation(360)
        ax.axis['right'].label.set_verticalalignment('center')
        ax.axis['right'].label.set_horizontalalignment('left')

        ax.axis['bottom'].set_visible(False)
        ax.grid()

        self._ax = ax
        self.ax = ax.get_aux_axes(tr)

        # First reference
        self.ax.plot([0], [self.STD], 'k*', ms=12, label=label)
        t = np.linspace(0, np.pi)
        r = np.zeros_like(t) + self.STD
        self.ax.plot(t, r, 'k--', label='_')

        self.samplePoints = []

    def add_sample(self, std, corr, *args, **kwargs):
        corr = np.clip(corr, -1, 1)
        theta = np.arccos(corr)
        l, = self.ax.plot(theta, std, *args, **kwargs)
        self.samplePoints.append(l)
        return l

    def add_reference(self, std, label='Reference 2', symbol='*', color='red', linestyle=':'):
        self.ax.plot([0], [std], symbol, ms=12, color=color, label=label)
        t = np.linspace(0, np.pi)
        r = np.zeros_like(t) + std
        self.ax.plot(t, r, linestyle, color=color, label='_')

    def add_contours(self, levels=5, **kwargs):
        rs, ts = np.meshgrid(
            np.linspace(self.smin, self.smax),
            np.linspace(0, np.pi)
        )
        RMSE = np.sqrt(
            self.STD**2 + rs**2 - 2.0 * self.STD * rs * np.cos(ts)
        )
        contours = self.ax.contour(ts, rs, RMSE, levels, **kwargs)
        return contours

def srl2(obsSTD1, obsSTD2, s, r, l, title):
    fig = plt.figure(figsize=(10, 10))
    dia = TaylorDiagram(obsSTD1, fig=fig, rect=111, label='Reference 1')
    plt.clabel(dia.add_contours(colors='gray'), inline=1, fontsize=10)

    # Add second reference
    dia.add_reference(obsSTD2, label='Reference 2', symbol='*', color='red', linestyle=':')

    region_marker_dict = {
        l[0]: 'o',
        l[1]: '^'
                                                                          
    }

    mec_values = ['steelblue', 'lightskyblue',"dodgerblue","goldenrod","orange","khaki","darkkhaki"]
    legend_names = ["NEU", "WCE", "MED", "NCA", "ENA", "WNA", "CNA"]

    for region_idx, (region_label, s_vals, r_vals) in enumerate(zip(l, s, r)):
        for model_num, (s_val, r_val) in enumerate(zip(s_vals, r_vals)):
            marker = region_marker_dict.get(region_label, 'x')
            mec = mec_values[model_num]
            dia.add_sample(s_val, r_val, label=f'{region_label}_{model_num+1}',
                           marker=marker, mec=mec, mfc='none', mew=2)

    # Legends
    patches = [mpatches.Patch(color=color, label=name) for color, name in zip(mec_values, legend_names)]
    markers = [Line2D([0], [0], marker=marker, color='black', linestyle='',
                      label=region, markersize=10)
               for region, marker in region_marker_dict.items()]
    star1 = Line2D([0], [0], marker='*', color='black', linestyle='', label='EL NINO REF 1', markersize=15)
    star2 = Line2D([0], [0], marker='*', color='red', linestyle='', label='NAO REF 2', markersize=15)

    fig.legend(handles=patches + markers + [star1, star2], loc='upper left')
    fig.text(0.4, 1, f"{title}", fontsize=16)
    plt.tight_layout()
    plt.show()
