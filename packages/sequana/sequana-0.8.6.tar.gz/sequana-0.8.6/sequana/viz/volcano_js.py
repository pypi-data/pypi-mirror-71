# coding=utf-8
# -*- python -*-
#
#  This file is part of GDSCTools software
#
#  Copyright (c) 2015 - Wellcome Trust Sanger Institute
#  All rights reserved
#
#  File author(s): Thomas Cokelaer <cokelaer@gmail.com>
#
#  Distributed under the BSD 3-Clause License.
#  See accompanying file LICENSE.txt distributed with this software
#
#  website: http://github.com/CancerRxGene/gdsctools
#
##############################################################################
"""Volcano plot utilities

The :class:`VolcanoJS` is derived from gdstools

"""
import os

from sequana.lazy import pandas as pd
from sequana.lazy import pylab
from sequana.lazy import numpy as np
import easydev

from easydev import Progress, AttrDict

import jinja2
from jinja2 import Environment, PackageLoader


__all__ = ["VolcanoJS"]


class VolcanoJS(object):
    """Utilities related to volcano plots

    """
    def __init__(self):
        data = pd.DataFrame(index=range(len(qvals)))
        data['pvalue'] = pvals
        data['signed_effect'] = signed_effects
        data['Feature'] = list(subdf[self._colname_feature])
        data['Drug'] = list(subdf[self._colname_drugid])
        data['text'] = texts.values
        data['FDR'] = subdf[self._colname_qvalue].values

        colors = list(data['color'].values)
        pvalues = data['pvalue'].values
        signed_effects = data['signed_effect'].values
        markersize = data['markersize'].values
        Y = -np.log10(list(pvalues)) # should be cast to list ?

        num = 1
        #pylab.close(num)
        fig = pylab.figure(num=1)
        fig.clf()
        ax = fig.add_subplot(111)
        try:
            ax.set_facecolor('#EEEEEE') #matplotlib 2.0
        except:
            ax.set_axis_bgcolor('#EEEEEE')
        ax.cla()

        # TODO signed effects may be inf why ?


        X = [easydev.precision(x, digit=2) for x in signed_effects]
        Y = [easydev.precision(y, digit=2) for y in Y]

        # Using scatter() is slow as compared to plot()
        # However, plot cannot take different sizes/colors
        scatter = ax.scatter(X, Y, s=markersize,
                alpha=0.3, c=colors, linewidth=1, picker=True)
        scatter.set_zorder(11)

        m = abs(signed_effects.min())
        M = abs(signed_effects.max())
        pylab.xlabel("Signed effect size", fontsize=self.settings.fontsize)
        pylab.ylabel('-log10(pvalues)', fontsize=self.settings.fontsize)
        l = max([m, M]) * 1.1
        pylab.xlim([-l, l])
        ax.grid(color='white', linestyle='solid')

        # some aliases
        fdr = self.settings.FDR_threshold
        if fdr < self.df[self._colname_qvalue].min():
            fdr = self.df[self._colname_qvalue].min()


        fdrs = sorted(self.settings.volcano_additional_FDR_lines)
        fdrs = fdrs[::-1] # reverse sorting

        styles = ['--', ':', '-.']
        if self.settings.volcano_FDR_interpolation is True:
            get_pvalue_from_fdr = self._get_pvalue_from_fdr_interp
        else:
            get_pvalue_from_fdr = self._get_pvalue_from_fdr

        pvalue = get_pvalue_from_fdr(fdr)
        ax.axhline(-np.log10(pvalue), linestyle='--', lw=2,
            color='red', alpha=1, label="FDR {:.2f} ".format(fdr) + " %")


        for i, this in enumerate(fdrs):
            if this < self.df[self._colname_qvalue].min() or\
                this > self.df[self._colname_qvalue].max():
                    continue
            pvalue = get_pvalue_from_fdr(this)
            ax.axhline(-np.log10(pvalue), linestyle=styles[i],
                color='red', alpha=1, label="FDR {:.2f} ".format(this) +" %")

        pylab.ylim([0, pylab.ylim()[1]*1.2]) # times 1.2 to put the legend

        ax.axvline(0, color='gray', alpha=0.8, lw=2)
        axl = pylab.legend(loc='best')
        axl.set_zorder(10) # in case there is a circle behind the legend.

        # For the static version
        title_handler = pylab.title("%s" % str(title).replace("_","  "),
                fontsize=self.settings.fontsize/1.2)
        labels = []

        # This code allows the ipython user to click on the matplotlib figure
        # to get information about the drug and feature of a given circles.
        def onpick(event):
            ind = event.ind[0]
            try:
                title = str(str(data.iloc[ind]['Drug'])) + " / " + str(data.iloc[ind].Feature)
                title += "\nFDR=" + "%.4e" % data.iloc[ind]['FDR']
                title_handler.set_text(title.replace("_","  "))
            except:
                print('Failed to create new title on click')
            print(data.iloc[ind].T)
            fig.canvas.draw()

        # keep track on the id for further memory release
        # For more info search for "matplotlib memory leak mpl_connect"
        self.cid = fig.canvas.mpl_connect('pick_event', onpick)

        # for the JS version
        # TODO: for the first 1 to 2000 entries ?
        labels = []
        self.data = data
        for i, row in data[['Drug', 'Feature', 'FDR']].iterrows():

            template = """
<table border="1" class="dataframe">
  <tbody>
    <tr>
      <th>Drug</th>
      <td>%(Drug)s</td>
    </tr>
    <tr>
      <th>Feature</th>
      <td>%(Feature)s</td>
    </tr>
    <tr>
      <th>FDR</th>
      <td>%(FDR)s</td>
    </tr>
  </tbody>
</table>""" % row.to_dict()
            labels.append(template)

            # this is more elegant but slower
            #label = row.to_frame()
            #label.columns = ['Row {0}'.format(i)]
            #labels.append(str(label.to_html(header=False)))
        self.scatter = scatter
        self.current_fig = fig

    def savefig(self, filename, size_inches=(10, 10)):
        # Save the PNG first. The savefig automatically set the size
        # to a defined set and back to original figsize.
        self.figtools.savefig(filename + '.png', size_inches=size_inches)


class VolcanoANOVAJS():
    def __init__(self, pvalue, fc, data):

        self.pvalue = -np.log10(pvalue)
        self.fc = fc
        self.data = data

    def _render_data(self, name="all associations"):

        self.data['color'] = self.data['color'].apply(lambda x:
                x.replace("black", "not_significant"))
        self.data['color'] = self.data['color'].apply(lambda x:
                x.replace("green", "sensitive"))
        self.data['color'] = self.data['color'].apply(lambda x:
                x.replace("red", "resistant"))

        # We have 3 colors but sometimes you may have only one or 2.
        # This may be an issue with canvasXpress. It seems essential
        # to sort the color column so that names are sorted alphabetically
        # and to include colors that are present in the sale order
        try:
            self.data.sort_values(by='color', inplace=True)
        except:
            self.data.sort("color", inplace=True)
        colors = []
        if "not_significant" in self.data.color.values:
            colors.append("rgba(0,0,0,0.5)")  # black
        if "resistant" in self.data.color.values:
            colors.append("rgba(205,0,0,0.5)")  # red
        if "sensitive" in self.data.color.values:
            colors.append("rgba(0,205,0,0.5)")  # green

        env = Environment()

        from easydev import get_package_location

        env.loader = jinja2.FileSystemLoader(
                        get_package_location("gdsctools")
                        + "/gdsctools/data/templates/")
        template = env.get_template("volcano.html")

        jinja = {}

        jinja["colors"] = colors
        jinja["Group"] = list(self.data['color'].values)
        jinja['xlabel'] = "Signed Effect Size"
        jinja['ylabel'] = "-log10(pvalue)"

        text = []
        for x,y,z in zip(self.data['Drug'].values,
            self.data['Feature'].values,
            self.data['FDR'].values):

            text.append("<b>Drug:</b>%s <br><b>Feature:</b>%s <br><b>FDR:</b>%s" % (x,y,z))
        jinja['vars'] = text

        """
        # does not work in the JS somehow some points do not appear
        # disabled for now
        markersize = self.data['markersize']
        markersize -= markersize.min()
        markersize /= markersize.max()
        markersize = (3*markersize).round()
        #markersize[markersize == 0] = 1

        FC = list(markersize.astype(int).astype(str))
        jinja['FC'] = FC
        """
        self.data.markersize /= (self.data.markersize.max()/3.)

        #First value is Y, second is X, following will be used in the
        try: # introduced in pandas > 0.16.2
            jinja['data'] = self.data[["signed_effect", "log10pvalue",
                "markersize"]].round(3).values.tolist()
        except: #for py3.3 on travis
            jinja['data'] = np.around(self.data[["signed_effect", "log10pvalue",
                "markersize"]]).values.tolist()
        jinja['title'] = '"%s"' % name

        fdrs = self.get_fdr_ypos()
        fdrs = [0 if np.isnan(x) else x for x in fdrs]
        jinja['additional_fdrs'] = ""
        for i,this in enumerate(fdrs):
            line = '\n{"color": "red", "width": 1, "type": "dashed", "y":  %s}'
            if i == len(fdrs)-1:
                pass
            else:
                line += ","
            jinja['additional_fdrs'] += line % this

        m = abs(self.data.signed_effect.min())
        M = abs(self.data.signed_effect.max())
        jinja['minX'] = -max([m, M]) * 1.1
        jinja['maxX'] =  max([m, M]) * 1.1
        jinja['maxY'] = self.data["log10pvalue"].max() * 1.2
        if max(fdrs) > jinja['maxY']:
            jinja['maxY'] = max(fdrs) * 1.2

        self.html = template.render(jinja)
        return self.html



