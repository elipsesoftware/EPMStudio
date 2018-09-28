# -*- coding: utf-8 -*-
'''Elipse Plant Manager - EPM Dataset Analysis Plug-ins - Plug-in sample
   Copyright (C) 2018 Elipse Software.
   Distributed under the MIT License.
   (See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
'''


# EPM Plugin modules
import Plugins as ep

# Numpy and other specific modules
import numpy as np


_g_DemoToolsCaption = 'EPM Python Plugin - Demo Tools'
_g_MissSinglePenTxt = 'Please select a single pen before applying this function!'
_g_MissDoublePenTxt = 'Please select two interpolated pens before applying this function!'
_g_MissPensMsgType = 'Warning'


@ep.DatasetFunctionPlugin('Remove NAN and Outliers', 1, 'noOutsNans')
def rmNanAndOutliers():
    """ Plot without NAN and outliers from selected pen
    """
    if len(ep.EpmDatasetPens.SelectedPens) < 1:
        ep.showMsgBox(_g_DemoToolsCaption, _g_MissSinglePenTxt, _g_MissPensMsgType)
        return None
    penName = ep.EpmDatasetPens.SelectedPens[0].Name + '_NoOutliers'
    epmData = ep.EpmDatasetPens.SelectedPens[0].Values
    t = epmData['Timestamp']
    v = epmData['Value']

    def _clearNANs(v, t):
        """ Deletes all NANs
            v: array of double values
            t: array of datetimes
        """
        nanPos = np.argwhere(np.isnan(v))
        v, t = np.delete(v, nanPos), np.delete(t, nanPos)
        return v, t

    def _clearOutliers(v, t, maxStdDevs = 6):
        """ Deletes all outliers
            v: array of double values
            t: array of datetimes
            maxStdDevs: cut-off limit for outliers (six-sigma by default)
        """
        smean = v.mean()
        s3 = np.floor(v.std() * maxStdDevs)
        outliers = np.argwhere(v < smean - s3)
        v, t = np.delete(v, outliers),  np.delete(t, outliers)
        outliers = np.argwhere(v > smean + s3)
        v, t = np.delete(v, outliers),  np.delete(t, outliers)
        return v, t

    v, t = _clearNANs(v, t)
    v, t = _clearOutliers(v, t)
    noOutsNans = _vta2epm(v, t)
    ep.plotValues(penName, noOutsNans)
    return noOutsNans


@ep.DatasetFunctionPlugin('Delta', 2, 'deltaCurves')
def deltasData():
    """ Plot deltas from selected pen
    """
    if len(ep.EpmDatasetPens.SelectedPens) != 1:
        ep.showMsgBox(_g_DemoToolsCaption, _g_MissSinglePenTxt, _g_MissPensMsgType)
        return None
    penName = ep.EpmDatasetPens.SelectedPens[0].Name + '_Delta'
    epmData = ep.EpmDatasetPens.SelectedPens[0].Values
    deltaCurves = epmData.copy();
    v = epmData['Value']
    delta = v[1:] - v[:-1]
    deltaValues = deltaCurves['Value']
    deltaValues[0] = 0
    deltaValues[1:] = delta
    ep.plotValues(penName, deltaCurves)
    return deltaCurves


@ep.DatasetFunctionPlugin('Remove Mean', 3, 'rmMean')
def removeMean():
    """ Plot removed mean data from selected pen
    """
    if len(ep.EpmDatasetPens.SelectedPens) != 1:
        ep.showMsgBox(_g_DemoToolsCaption, _g_MissSinglePenTxt, _g_MissPensMsgType)
        return None
    penName = ep.EpmDatasetPens.SelectedPens[0].Name + '_ZeroMean'
    epmData = ep.EpmDatasetPens.SelectedPens[0].Values
    rmMean = epmData.copy();
    v = epmData['Value']
    rmMean['Value'] = v - v.mean()
    ep.plotValues(penName, rmMean)
    return rmMean


@ep.DatasetFunctionPlugin('Normalize Curve', 4, 'normCurves')
def normalizeData():
    """ Plot normalized data from selected pen
    """
    if len(ep.EpmDatasetPens.SelectedPens) != 1:
        ep.showMsgBox(_g_DemoToolsCaption, _g_MissSinglePenTxt, _g_MissPensMsgType)
        return None
    penName = ep.EpmDatasetPens.SelectedPens[0].Name + '_Normalized'
    epmData = ep.EpmDatasetPens.SelectedPens[0].Values
    normCurves = epmData.copy();
    v = epmData['Value']
    normCurves['Value'] = (v - v.mean()) / v.std()
    ep.plotValues(penName, normCurves)
    return normCurves


@ep.DatasetFunctionPlugin('Statistics Info', 5, 'stats')
def statsInfos():
    """ Show basic statistics from selected pen
    """
    if len(ep.EpmDatasetPens.SelectedPens) != 1:
        ep.showMsgBox(_g_DemoToolsCaption, _g_MissSinglePenTxt, _g_MissPensMsgType)
        return None
    epmData = ep.EpmDatasetPens.SelectedPens[0].Values
    v = epmData['Value']
    stats = v.mean(), v.std(), v.min(), v.max()
    message = 'Mean: {:.3f}\nStdDev: {:.3f}\nMinimum: {:.3f}\nMaximum {:.3f}'
    # use only for debugging    print message.format(*stats)
    ep.showMsgBox(_g_DemoToolsCaption, message.format(*stats))
    return stats


@ep.DatasetFunctionPlugin('Count Changes', 6, 'changes')
def countChanges():
    """ Show direction changes count from selected pen
    """
    if len(ep.EpmDatasetPens.SelectedPens) != 1:
        ep.showMsgBox(_g_DemoToolsCaption, _g_MissSinglePenTxt, _g_MissPensMsgType)
        return None
    epmData = ep.EpmDatasetPens.SelectedPens[0].Values
    changes = _invCount(epmData['Value'])
    message = 'Number of changes: {}'
    # use only for debugging    print message.format(changes)
    ep.showMsgBox(_g_DemoToolsCaption, message.format(changes))
    return changes


@ep.DatasetFunctionPlugin('Integrate Curve', 7, 'curveArea')
def integralData():
    """ Show area from selected pen
    """
    if len(ep.EpmDatasetPens.SelectedPens) != 1:
        ep.showMsgBox(_g_DemoToolsCaption, _g_MissSinglePenTxt, _g_MissPensMsgType)
        return None
    epmData = ep.EpmDatasetPens.SelectedPens[0].Values
    from scipy import integrate
    curveArea = integrate.simps(epmData['Value'])
    message = 'Integral: {:.2f}'
    # use only for debugging    print message.format(curveArea)
    ep.showMsgBox(_g_DemoToolsCaption, message.format(curveArea))
    return curveArea


@ep.DatasetFunctionPlugin('Plot Min-Max', 8, 'minMax')
def plotMinMax():
    """ Plot Min-Max lines from selected pen
    """
    if len(ep.EpmDatasetPens.SelectedPens) != 1:
        ep.showMsgBox(_g_DemoToolsCaption, _g_MissSinglePenTxt, _g_MissPensMsgType)
        return None
    penName = ep.EpmDatasetPens.SelectedPens[0].Name
    penMin, penMax = penName + '_Min', penName + '_Max'
    epmData = ep.EpmDatasetPens.SelectedPens[0].Values
    vmin, vmax = epmData.copy(), epmData.copy()
    epmValues = epmData['Value']
    minValue, maxValue = epmValues.min(), epmValues.max()
    vmin['Value'][:] = minValue
    vmax['Value'][:] = maxValue
    ep.plotValues(penMin, vmin)
    ep.plotValues(penMax, vmax)
    return (minValue, maxValue)


@ep.DatasetFunctionPlugin('Plot XY', 9)
def plotXY():
    """ Plot XY from selected pens
    """
    if len(ep.EpmDatasetPens.SelectedPens) != 2:
        ep.showMsgBox(_g_DemoToolsCaption, _g_MissDoublePenTxt, _g_MissPensMsgType)
        return None
    epmData1 = ep.EpmDatasetPens.SelectedPens[0].Values
    epmData2 = ep.EpmDatasetPens.SelectedPens[1].Values
    from matplotlib.pylab import show, subplots, plot, figure, connect
    figure(figsize=(8, 6))
    plot(epmData1['Value'], epmData2['Value'])
    show()


@ep.DatasetFunctionPlugin('Get Points', 10, 'selPoints')
def plotGetPoints():
    """ Get data points from selected pen
    """
    if len(ep.EpmDatasetPens.SelectedPens) != 1:
        ep.showMsgBox(_g_DemoToolsCaption, _g_MissSinglePenTxt, _g_MissPensMsgType)
        return None
    epmData = ep.EpmDatasetPens.SelectedPens[0].Values
    y = epmData['Value'].copy()
    x = np.arange(len(y))
    from matplotlib.pylab import show, subplots, plot, figure, connect
    fig = figure(figsize=(8, 6))
    ax = fig.add_subplot(111, axisbg='#FFFFFF')
    ax.plot(x, y, '-o')
    selPoints = []

    def onclick(event):
        selPoints.append((event.xdata, event.ydata))

    from matplotlib.widgets import Cursor
    cursor = Cursor(ax, useblit=True, color='red', linewidth=1)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    show()
    return selPoints


@ep.DatasetFunctionPlugin('Get Data', 11, 'selData')
def plotGetSelection():
    """ Get data range from selected pen
    """
    if len(ep.EpmDatasetPens.SelectedPens) != 1:
        ep.showMsgBox(_g_DemoToolsCaption, _g_MissSinglePenTxt, _g_MissPensMsgType)
        return None
    epmData = ep.EpmDatasetPens.SelectedPens[0].Values
    y = epmData['Value'].copy()
    x = np.arange(len(y))
    from matplotlib.pylab import show, subplots, plot, figure, connect
    fig = figure(figsize=(8,6))
    ax = fig.add_subplot(211, axisbg='#FFFFCC')
    ax.plot(x, y, '-')
    ax.set_title('Press left mouse button and drag to test')
    ax2 = fig.add_subplot(212, axisbg='#FFFFCC')
    line2, = ax2.plot(x, y, '-')
    selData = []

    def onselect(xmin, xmax):
        selData.append([xmin, xmax])
        indmin, indmax = np.searchsorted(x, (xmin, xmax))
        indmax = min(len(x)-1, indmax)
        thisx = x[indmin:indmax]
        thisy = y[indmin:indmax]
        line2.set_data(thisx, thisy)
        ax2.set_xlim(thisx[0], thisx[-1])
        ax2.set_ylim(thisy.min(), thisy.max())
        fig.canvas.draw()

    from matplotlib.widgets import SpanSelector
    span = SpanSelector(
        ax,
        onselect,
        'horizontal',
        useblit=True,
        rectprops = dict(alpha=0.5, facecolor='red')
    )
    show()
    return selData


@ep.DatasetFunctionPlugin('Get Retangle', 12, 'selRect')
def plotGetRetangle():
    """ Get area selection from selected pen
    """
    if len(ep.EpmDatasetPens.SelectedPens) != 1:
        ep.showMsgBox(_g_DemoToolsCaption, _g_MissSinglePenTxt, _g_MissPensMsgType)
        return None
    epmData = ep.EpmDatasetPens.SelectedPens[0].Values
    y = epmData['Value'].copy()
    x = np.arange(len(y))
    from matplotlib.pylab import show, subplots, plot, figure, connect
    fig, current_ax = subplots()
    plot(x, y, lw=2, c='g', alpha=.3)
    selRect = []

    def line_select_callback(eclick, erelease):
        # eclick and erelease are the press and release events
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print "\n({:3.3f}, {:3.3f}) --> ({:3.3f}, {:3.3f})".format(x1, y1, x2, y2)
        selRect.append((int(x1), y1, int(x2), y2))

    def toggle_selector(event):
        if event.key in ['Q', 'q'] and toggle_selector.RS.active:
            toggle_selector.RS.set_active(False)
        if event.key in ['A', 'a'] and not toggle_selector.RS.active:
            toggle_selector.RS.set_active(True)

    from matplotlib.widgets import RectangleSelector
    toggle_selector.RS = RectangleSelector(
        current_ax,
        line_select_callback,
        drawtype='box',
        useblit=True,
        button=[1,3],
        minspanx=5,
        minspany=5,
        spancoords='pixels'
    )
    connect('key_press_event', toggle_selector)
    show()
    return selRect


###### Internal functions ######

def _invCount(v):
    """ Count values direction changes
        v: array of double values
    """
    delta = v[1:] - v[:-1]
    inv = (
        1 for i in xrange(len(delta) - 1)
        if np.sign(delta[i]) != np.sign(delta[i + 1])
    )
    # use only for debugging    print next(inv)
    return sum(inv)

def _vta2epm(v, t):
    """ Convert datetime array and values array into EPM (Numpy) Array
        v: array of double values
        t: array of datetimes
    """
    assert np.shape(v) == np.shape(t)
    assert np.size(v) == np.size(t)
    epmV = np.empty([np.size(v)], dtype = ep.EpmValueArrayType)
    epmV['Timestamp'] = t
    epmV['Quality'] = 0    # Status Code is Good by default
    epmV['Value'] = v
    return epmV

