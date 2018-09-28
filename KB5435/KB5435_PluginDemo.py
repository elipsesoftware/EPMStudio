'''Elipse Plant Manager - EPM Dataset Analysis Plugin - Plugin sample
Copyright (C) 2015 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
'''

# EPM Plugin modules
import Plugins as ep

# Import modules
import numpy as np
import pandas as pd
import datetime as dt

# Modules to find MyDoc's
import ctypes
from ctypes.wintypes import MAX_PATH

dll = ctypes.windll.shell32
myDocsDir = ctypes.create_unicode_buffer(MAX_PATH + 1)
dll.SHGetSpecialFolderPathW(None, myDocsDir, 0x0005, False)
csvFile = myDocsDir.value + u'\\Elipse Software\\EPM Studio\\Plugins\\dailyMinMaxTemps.csv'

# *** Plugins EPM Studio - Dataset Analysis ***
@ep.DatasetFunctionPlugin('Find daily min-max', 2)
def findDailyMinMax():
    """Finda daily min-max values.
    All outliers will be removed from data before proceed with min-max search.
    """
    if len(ep.EpmDatasetPens.SelectedPens) != 1:
        ep.showMsgBox('EPM Python Plugin - Demo KB5435', 'Please select a single pen before applying this function!', 'Warning')
        return 0

    # Get data from selected pen
    data = ep.EpmDatasetPens.SelectedPens[0].Values
    
    # Crating a Pandas Time Series object
    ts = pd.Series(data['Value'], index=data['Timestamp'])
    
    # Removing outliers based on percentile [5th; 95th]
    perct = np.percentile(ts.values, [5, 95])
    tsNoOutliers = ts[(ts.values > perct[0]) & (ts.values < perct[1])]
    
    # Resampling daily based on min-max
    tsMin = tsNoOutliers.resample('D').min()
    tsMax = tsNoOutliers.resample('D').max()
    
    # Converting to Pandas Dataframe (to save all results in one CSV file)
    df = tsMin.to_frame()
    df.columns=['Min']
    df['Max'] = tsMax.values
    
    # Export to CSV file
    df.to_csv(csvFile, sep =';', decimal=',') # Note: decimal separator for Brazil
    
    # Plot results in EPM Dataset Analyis environment
    # Prepare data to plot
    desc = np.dtype([('Value', '>f8'), ('Timestamp', 'object'), ('Quality', 'object')])
    epmDataMin = np.empty(len(df), dtype = desc)
    epmDataMax = np.empty(len(df), dtype = desc)
    epmDataMin['Value'] = df.Min
    epmDataMin['Timestamp'] = np.array([pd.to_datetime(x).to_datetime() for x in df.index])
    epmDataMin['Quality'] = 0
    epmDataMax['Value'] = df.Max
    epmDataMax['Timestamp'] = epmDataMin['Timestamp'].copy()
    epmDataMax['Quality'] = 0
    # ploting
    ep.plotValues('Temp_Min_plugin', epmDataMin)
    ep.plotValues('Temp_Max_plugin', epmDataMax)
