# coding: utf-8
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *

## agg backend is used to create plot as a .png file
# mpl.use('agg')

static_path = os.path.join(os.environ['PROJECT_ROOT'], '..', 'static')


# static_path = '/var/www/ubertool/ubertool_ecorest/static'


#################################################
# generate boxplots
#################################################
# from sam_rest import sam_dataqueries


def sam_figures_callable(jid, output_type, time_avg_option, tox_exceed_option, huc_output):
    if tox_exceed_option == '4':
        # month streak
        file_name = GenerateSAM_MonthStreakBoxplot(jid, huc_output)
    elif tox_exceed_option == '3':
        # year streak
        pass
    elif tox_exceed_option == '2':
        # month freq
        pass
    else:  # == '1'
        # year freq
        pass

    return file_name


## Average streak by month boxplot
def GenerateSAM_MonthStreakBoxplot(jobid, huc_output):
    # get sam monthly data array of streaks
    # sam_vector = sam_dataqueries.GetSAM_MonthlyArrayStreakOutput(jobid)

    # convert dictionary to numpy array using pandas dataframe
    sam_vector = pd.DataFrame.from_dict(huc_output, orient="index")
    sam_vector = sam_vector.astype('float16').as_matrix()

    # Create a figure instance
    fig = plt.figure(1, figsize=(10, 6))

    # Create an axes instance
    ax = fig.add_subplot(111)
    ax1 = fig.add_subplot(111)

    # Create a boxplot
    bp = ax.boxplot(sam_vector, notch=0, sym='+', vert=1, whis=1.5, patch_artist=True)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')
    colors = ['lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
              'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    ## Custom x-axis labels
    monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax.set_xticklabels(monthNames)

    ## Remove top axes and right axes ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Days')

    # Add a horizontal grid to the plot - light in color
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)
    ax1.set_axisbelow(True)
    fig.suptitle("Monthly Average Exceedance Streak Distribution across HUCs")

    # Save the figure
    file_name = jobid + "_month_streak_boxplot.png"
    out_path = os.path.join(static_path, file_name)
    fig.savefig(out_path, bbox_inches="tight")
    fig.canvas.set_window_title('Monthly Streak Average')
    fig.clf()

    return file_name


## Average streak by year boxplot
def GenerateSAM_AnnualStreakBoxplot(jobid):
    # get sam annual data array of streaks
    sam_vector = sam_dataqueries.GetSAM_AnnualArrayStreakOutput(jobid)

    # Create a figure instance
    fig = plt.figure(1, figsize=(10, 6))

    # Create an axes instance
    ax = fig.add_subplot(111)
    ax1 = fig.add_subplot(111)

    # Create a boxplot
    bp = ax.boxplot(sam_vector, notch=0, sym='+', vert=1, whis=1.5, patch_artist=True)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    plt.setp(bp['fliers'], color='red', marker='+')
    colors = ['lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
              'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
              'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
              'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
              'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    ## Custom x-axis labels
    yearNames = ['1984', '1985', '1986', '1987', '1988', '1989',
                 '1990', '1991', '1992', '1993', '1994', '1995',
                 '1996', '1997', '1998', '1999', '2000', '2001',
                 '2002', '2003', '2004', '2005', '2006', '2007',
                 '2008', '2009', '2010', '2011', '2012', '2013']
    ax.set_xticklabels(yearNames)

    ## Remove top axes and right axes ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Days')

    # Add a horizontal grid to the plot - light in color
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)
    ax1.set_axisbelow(True)
    fig.suptitle("Annual Average Exceedance Streak Distribution across HUCs")

    # Save the figure
    f = static_path + jobid + "_annual_streak_boxplot.png"
    fig.savefig(f, bbox_inches="tight")
    fig.canvas.set_window_title('Annual Streak Average')
    fig.clf()


## Average streak by month boxplot
def GenerateSAM_MonthFreqofExceedBoxplot(jobid):
    # get sam monthly data array of streaks
    sam_vector = sam_dataqueries.GetSAM_MonthlyArrayFreqofExceedOutput(jobid)

    # Create a figure instance
    fig = plt.figure(1, figsize=(10, 6))

    # Create an axes instance
    ax = fig.add_subplot(111)
    ax1 = fig.add_subplot(111)

    # Create a boxplot
    bp = ax.boxplot(sam_vector, notch=0, sym='+', vert=1, whis=1.5, patch_artist=True)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')
    colors = ['lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
              'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    ## Custom x-axis labels
    monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax.set_xticklabels(monthNames)

    ## Remove top axes and right axes ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Exceedance Proportion')

    # Add a horizontal grid to the plot - light in color
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)
    ax1.set_axisbelow(True)
    fig.suptitle("Monthly Proportion of Exceedance Distribution across HUCs")

    # Save the figure
    f = static_path + jobid + "_month_exceedance_boxplot.png"
    fig.savefig(f, bbox_inches="tight")
    fig.canvas.set_window_title('Monthly Proportion of Exceedance')
    fig.clf()


## Average streak by year boxplot
def GenerateSAM_AnnualFreqofExceedBoxplot(jobid):
    # get sam annual data array of streaks
    sam_vector = sam_dataqueries.GetSAM_AnnualArrayFreqofExceedOutput(jobid)

    # Create a figure instance
    fig = plt.figure(1, figsize=(10, 6))

    # Create an axes instance
    ax = fig.add_subplot(111)
    ax1 = fig.add_subplot(111)

    # Create a boxplot
    bp = ax.boxplot(sam_vector, notch=0, sym='+', vert=1, whis=1.5, patch_artist=True)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    plt.setp(bp['fliers'], color='red', marker='+')
    colors = ['lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
              'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
              'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
              'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue',
              'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue', 'lightblue']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    ## Custom x-axis labels
    yearNames = ['1984', '1985', '1986', '1987', '1988', '1989',
                 '1990', '1991', '1992', '1993', '1994', '1995',
                 '1996', '1997', '1998', '1999', '2000', '2001',
                 '2002', '2003', '2004', '2005', '2006', '2007',
                 '2008', '2009', '2010', '2011', '2012', '2013']
    ax.set_xticklabels(yearNames)

    ## Remove top axes and right axes ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Exceedance Proportion')

    # Add a horizontal grid to the plot - light in color
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)
    ax1.set_axisbelow(True)
    fig.suptitle("Annual Proportion of Exceedance Distribution across HUCs")

    # Save the figure
    f = static_path + jobid + "_annual_exceedance_boxplot.png"
    fig.savefig(f, bbox_inches="tight")
    fig.canvas.set_window_title('Annual Proportion of Exceedance')
    fig.clf()


#######################################################
# generate histograms
#######################################################

## Histogram of monthly streaks
def GenerateSAM_MonthStreakHistogram(jobid):
    # get sam data vector of streaks
    sam_vector = sam_dataqueries.GetSAM_MonthlyVectorStreakOutput(jobid)

    # Create a second figure instance
    fig2 = plt.figure(2, figsize=(10, 6))

    # Create an axes instance
    ax_2 = fig2.add_subplot(111)
    ax1_2 = fig2.add_subplot(111)

    # Add a horizontal grid to the plot - light in color
    ax1_2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                     alpha=0.5)
    ax1_2.set_axisbelow(True)

    # Create a histogram
    hist_fig = ax_2.hist(sam_vector, facecolor="darkseagreen")

    ## Remove top axes and right axes ticks
    ax_2.get_xaxis().tick_bottom()
    ax_2.get_yaxis().tick_left()
    ax1_2.set_xlabel('Days')
    ax1_2.set_ylabel('Frequency')

    # fig2.title('Streak Average across all Months and HUCs')
    ax_2.set_title('Streak Average across all Months and HUCs')

    # Save the figure
    f = static_path + jobid + "_month_streak_histogram.png"
    fig2.savefig(f, bbox_inches="tight")

    fig2.clf()


## Histogram of annual streaks
def GenerateSAM_AnnualStreakHistogram(jobid):
    # get sam data vector of streaks
    sam_vector = sam_dataqueries.GetSAM_AnnualVectorStreakOutput(jobid)

    # Create a second figure instance
    fig2 = plt.figure(2, figsize=(10, 6))

    # Create an axes instance
    ax_2 = fig2.add_subplot(111)
    ax1_2 = fig2.add_subplot(111)

    # Add a horizontal grid to the plot - light in color
    ax1_2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                     alpha=0.5)
    ax1_2.set_axisbelow(True)

    # Create a histogram
    hist_fig = ax_2.hist(sam_vector, facecolor="darkseagreen")

    ## Remove top axes and right axes ticks
    ax_2.get_xaxis().tick_bottom()
    ax_2.get_yaxis().tick_left()
    ax1_2.set_xlabel('Days')
    ax1_2.set_ylabel('Frequency')

    # fig2.title('Streak Average across all Years and HUCs')
    ax_2.set_title('Streak Average across all Years and HUCs')

    # Save the figure
    f = static_path + jobid + "_annual_streak_histogram.png"
    fig2.savefig(f, bbox_inches="tight")

    fig2.clf()


## Histogram of monthly frequency of exceedances
def GenerateSAM_MonthFreqofExceedHistogram(jobid):
    # get sam data vector of streaks
    sam_vector = sam_dataqueries.GetSAM_MonthlyVectorFreqofExceedOutput(jobid)

    # Create a second figure instance
    fig2 = plt.figure(2, figsize=(10, 6))

    # Create an axes instance
    ax_2 = fig2.add_subplot(111)
    ax1_2 = fig2.add_subplot(111)

    # Add a horizontal grid to the plot - light in color
    ax1_2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                     alpha=0.5)
    ax1_2.set_axisbelow(True)

    # Create a histogram
    hist_fig = ax_2.hist(sam_vector, facecolor="darkseagreen")

    ## Remove top axes and right axes ticks
    ax_2.get_xaxis().tick_bottom()
    ax_2.get_yaxis().tick_left()
    ax1_2.set_xlabel('Days')
    ax1_2.set_ylabel('Frequency')

    # fig2.title('Streak Average across all Months and HUCs')
    ax_2.set_title('Proportion of Exceedance across all Months and HUCs')

    # Save the figure
    f = static_path + jobid + "_month_exceedance_histogram.png"
    fig2.savefig(f, bbox_inches="tight")

    fig2.clf()


## Histogram of annual frequency of exceedances
def GenerateSAM_AnnualFreqofExceedHistogram(jobid):
    # get sam data vector of streaks
    sam_vector = sam_dataqueries.GetSAM_AnnualVectorFreqofExceedOutput(jobid)

    # Create a second figure instance
    fig2 = plt.figure(2, figsize=(10, 6))

    # Create an axes instance
    ax_2 = fig2.add_subplot(111)
    ax1_2 = fig2.add_subplot(111)

    # Add a horizontal grid to the plot - light in color
    ax1_2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                     alpha=0.5)
    ax1_2.set_axisbelow(True)

    # Create a histogram
    hist_fig = ax_2.hist(sam_vector, facecolor="darkseagreen")

    ## Remove top axes and right axes ticks
    ax_2.get_xaxis().tick_bottom()
    ax_2.get_yaxis().tick_left()
    ax1_2.set_xlabel('Days')
    ax1_2.set_ylabel('Frequency')

    # fig2.title('Streak Average across all Years and HUCs')
    ax_2.set_title('Proportion of Exceedance across all Years and HUCs')

    # Save the figure
    f = static_path + jobid + "_annual_exceedance_histogram.png"
    fig2.savefig(f, bbox_inches="tight")

    fig2.clf()


#########################################################
# generate huc time series
##########################################################
## huc time series for monthly average streak
def GenerateSAM_MonthStreakHUCPlot(jobid, hucid):
    # get sam streak data for a particular huc
    sam_huc = sam_dataqueries.GetSAM_MonthlyHUCStreakOutput(jobid, hucid)

    # month info
    months = range(12)
    monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Create a third figure instance
    fig3 = plt.figure(3, figsize=(10, 6))

    # Create an axes instance
    ax_3 = fig3.add_subplot(111)
    ax1_3 = fig3.add_subplot(111)

    # plot monthly series
    plt.plot(months, sam_huc, linestyle='-', marker='o')

    # Add a horizontal grid to the plot - light in color
    ax1_3.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                     alpha=0.5)
    ax1_3.set_axisbelow(True)

    ## Custom x-axis labels
    ax_3.set_xticklabels(monthNames)
    # set tick intervals to 12
    ax_3.locator_params(tight=True, nbins=12)
    ## Remove top axes and right axes ticks
    ax_3.get_xaxis().tick_bottom()
    ax_3.get_yaxis().tick_left()
    ax1_3.set_xlabel('Month')
    ax1_3.set_ylabel('Maximum Exceedance Streak (days)')

    # title
    huc_title = "Monthly Maximimum Streak for HUC " + hucid
    ax_3.set_title(huc_title)

    # Save the figure
    f = static_path + jobid + hucid + "_month_streaks_huc.png"
    fig3.savefig(f, bbox_inches="tight")

    fig3.clf()


## huc time series for annual average streak
def GenerateSAM_AnnualStreakHUCPlot(jobid, hucid):
    # get sam streak data for a particular huc
    sam_huc = sam_dataqueries.GetSAM_AnnualHUCStreakOutput(jobid, hucid)

    # month info
    years = range(30)
    yearNames = ['1984', '1985', '1986', '1987', '1988', '1989',
                 '1990', '1991', '1992', '1993', '1994', '1995',
                 '1996', '1997', '1998', '1999', '2000', '2001',
                 '2002', '2003', '2004', '2005', '2006', '2007',
                 '2008', '2009', '2010', '2011', '2012', '2013']

    # Create a third figure instance
    fig3 = plt.figure(3, figsize=(10, 6))

    # Create an axes instance
    ax_3 = fig3.add_subplot(111)
    ax1_3 = fig3.add_subplot(111)

    # plot annual series
    plt.plot(years, sam_huc, linestyle='-', marker='o')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)

    # Add a horizontal grid to the plot - light in color
    ax1_3.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                     alpha=0.5)
    ax1_3.set_axisbelow(True)

    ## Custom x-axis labels
    ax_3.set_xticklabels(yearNames)
    # set tick intervals to 12
    ax_3.locator_params(tight=True, nbins=30)
    ## Remove top axes and right axes ticks
    ax_3.get_xaxis().tick_bottom()
    ax_3.get_yaxis().tick_left()
    ax1_3.set_xlabel('Year')
    ax1_3.set_ylabel('Maximum Exceedance Streak (days)')

    # title
    huc_title = "Annual Maximum Streak for HUC " + hucid
    ax_3.set_title(huc_title)

    # Save the figure
    f = static_path + jobid + hucid + "_annual_streaks_huc.png"
    fig3.savefig(f, bbox_inches="tight")

    fig3.clf()


## huc time series for monthly average streak
def GenerateSAM_MonthFreqofExceedHUCPlot(jobid, hucid):
    # get sam streak data for a particular huc
    sam_huc = sam_dataqueries.GetSAM_MonthlyHUCFreqofExceedOutput(jobid, hucid)

    # month info
    months = range(12)
    monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Create a third figure instance
    fig3 = plt.figure(3, figsize=(10, 6))

    # Create an axes instance
    ax_3 = fig3.add_subplot(111)
    ax1_3 = fig3.add_subplot(111)

    # plot monthly series
    plt.plot(months, sam_huc, linestyle='-', marker='o')

    # Add a horizontal grid to the plot - light in color
    ax1_3.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                     alpha=0.5)
    ax1_3.set_axisbelow(True)

    ## Custom x-axis labels
    ax_3.set_xticklabels(monthNames)
    # set tick intervals to 12
    ax_3.locator_params(tight=True, nbins=12)
    ## Remove top axes and right axes ticks
    ax_3.get_xaxis().tick_bottom()
    ax_3.get_yaxis().tick_left()
    ax1_3.set_xlabel('Month')
    ax1_3.set_ylabel('Maximum Exceedance Streak (days)')

    # title
    huc_title = "Monthly Proportion of Exceedance for HUC " + hucid
    ax_3.set_title(huc_title)

    # Save the figure
    f = static_path + jobid + hucid + "_month_exceedance_huc.png"
    fig3.savefig(f, bbox_inches="tight")

    fig3.clf()


## huc time series for annual average streak
def GenerateSAM_AnnualFreqofExceedHUCPlot(jobid, hucid):
    # get sam streak data for a particular huc
    sam_huc = sam_dataqueries.GetSAM_AnnualHUCFreqofExceedOutput(jobid, hucid)

    # month info
    years = range(30)
    yearNames = ['1984', '1985', '1986', '1987', '1988', '1989',
                 '1990', '1991', '1992', '1993', '1994', '1995',
                 '1996', '1997', '1998', '1999', '2000', '2001',
                 '2002', '2003', '2004', '2005', '2006', '2007',
                 '2008', '2009', '2010', '2011', '2012', '2013']

    # Create a third figure instance
    fig3 = plt.figure(3, figsize=(10, 6))

    # Create an axes instance
    ax_3 = fig3.add_subplot(111)
    ax1_3 = fig3.add_subplot(111)

    # plot annual series
    plt.plot(years, sam_huc, linestyle='-', marker='o')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)

    # Add a horizontal grid to the plot - light in color
    ax1_3.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                     alpha=0.5)
    ax1_3.set_axisbelow(True)

    ## Custom x-axis labels
    ax_3.set_xticklabels(yearNames)
    # set tick intervals to 12
    ax_3.locator_params(tight=True, nbins=30)
    ## Remove top axes and right axes ticks
    ax_3.get_xaxis().tick_bottom()
    ax_3.get_yaxis().tick_left()
    ax1_3.set_xlabel('Year')
    ax1_3.set_ylabel('Proportion of Exceedance')

    # title
    huc_title = "Annual Proportion of Exceedance for HUC " + hucid
    ax_3.set_title(huc_title)

    # Save the figure
    f = static_path + jobid + hucid + "_annual_exceedance_huc.png"
    fig3.savefig(f, bbox_inches="tight")

    fig3.clf()
