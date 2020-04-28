# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 14:24:49 2020

@author: michael.mclaughlin
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
import os
import urllib.request as www
#plt.ion()
covidDir='c:/gen/covid19'

def cvprocess(covidDir):
    IRLCasesToday=229          # if new data announced put here otherwise set to 0
    IRLDeathsToday=59
    if not(os.path.isdir(covidDir)):
        try:
            os.mkdir(covidDir)
        except OSError:
            print("Creation of the directory {} failed".format(covidDir))
            print("Please create a directory name {}".format(covidDir))
            return
        else:
            print("Successfully created the directory {}".format(covidDir))

    today=time.asctime()
    today=today[4:10]
    today=today.replace(' ','')

    fname=os.path.join(covidDir, 'download'+today+'.csv')
    if not(os.path.isfile(fname)):
        print('Retrieving todays new data')
        www.urlretrieve('https://opendata.ecdc.europa.eu/covid19/casedistribution/csv',fname)
    else:
        print('File already retrieved')
    nDaysLine=27            # No. of days to plot on line charts
    nDaysBar=14             # No. of days to plot on bar charts
    eurCountries=['AUT','BLR','BEL','BIH','BGR','HRV','CYP','DNK','EST','FIN','FRA','DEU','GRC','IRL',
                     'ITA','LUX','NLD','POL','PRT','ROU','SRB','SVK','SVN','ESP','SWE','CHE','GBR']
    #countries=['AUS','JPN']
    countries=['IRL','FRA',         'ITA',    'USA',  'ESP',       'GBR',      'SWE'       ]
    countries=['IRL','SWE','ISL',         'ITA']
    colors=[[0,0.7,0],[0,0.25,0.85],[0,0.7,1],[1,0,0],[0.0,0.0,0.0],[1,0.7,0],[0.63,0.63,0],[0.85,0.9,0],[0.7,0.0,0.7],[0.0,0.55,0.70]]
    
    nCountries=len(countries)
    maxDays=200
    allCases=np.zeros((maxDays,nCountries))
    allCumCases=allCases
    allDeaths=allCases
    allCumDeaths=allCases
    stats=pd.read_csv(fname)
    euNewCases=np.zeros(maxDays)
    euNewDeaths=np.zeros(maxDays)
    euPop=0;
    nullxy=np.arange(0,0.01,0.01)
    # Go through data for each Euro country
    for iEurCountry in range(len(eurCountries)):
        popd=stats.popData2018[stats.countryterritoryCode==eurCountries[iEurCountry]]
        pop=popd[popd.first_valid_index()]
        euPop=euPop+pop
        newCases=np.flipud(np.array(stats.cases[stats.countryterritoryCode==eurCountries[iEurCountry]]))
        newDeaths=np.flipud(np.array(stats.deaths[stats.countryterritoryCode==eurCountries[iEurCountry]]))
        euNewCases[-len(newCases):]=euNewCases[-len(newCases):]+newCases
        euNewDeaths[-len(newCases):]=euNewDeaths[-len(newCases):]+newDeaths
        
    allCNames = pd.DataFrame(columns=['CNames'])
    dayWidth=1      # width of each day
    countryWidth=dayWidth/(nCountries+2)
    cms=['NewCases', 'NewDeaths', 'TotalCases', 'TotalDeaths','CaseFatalityRate','CaseRateIncrease','DeathRateIncrease','DeathInc4DayAve','CasesPer1M', 'DeathsPer1M','Deaths Curve Shape (if DperM 20+)','DeathsPerM Since 10perM']
    barchart=np.array([1 ,       1,          0,             0,             0,                  1,           1,           0,              0,            0,            0,            0])
    percent =np.array([0 ,       0,          0,             0,             1,                  1,           1,           1,              0,            0,            1,            0])
    # Need an array of axes, there must be a better way to do it than this:
    fig, ax = plt.subplots(nrows=1, ncols=len(cms), figsize=(8, 20))
    plt.close(fig)
    for iAx in range(len(cms)):
        newf=plt.figure(iAx,figsize=(18, 10))
        plt.gcf().canvas.set_window_title(cms[iAx])
        if iAx>0:
            fig=np.append(fig,newf)
        else:
            fig=newf
        ax[iAx]=plt.axes()
    nCmsTotal=len(cms)*len(countries)
    allData=np.zeros((maxDays,nCmsTotal))
    iCol=0
    dates=[0]
    maxy=np.zeros( len(cms) )
    for iCountry in range(len(countries)):
        if countries[iCountry]=='EUR':
            pop=euPop
            newCases=euNewCases
            newDeaths=euNewDeaths
        else:
            popd=stats.popData2018[stats.countryterritoryCode==countries[iCountry]]
            pop=popd[popd.first_valid_index()]
            cdates=stats.dateRep[stats.countryterritoryCode==countries[iCountry]]
            if len(cdates)>len(dates):
                dates=cdates
            newCases=np.flipud(np.array(stats.cases[stats.countryterritoryCode==countries[iCountry]]))
            newDeaths=np.flipud(np.array(stats.deaths[stats.countryterritoryCode==countries[iCountry]]))
        if iCountry==0 and IRLCasesToday>0:
            newCases=np.append(newCases[1:],IRLCasesToday)        # Add latest IRL cases
            newDeaths=np.append(newDeaths[1:],IRLDeathsToday)     # Add latest IRL deaths
        allCases[-len(newCases):,iCountry]=newCases
        cumCases=np.cumsum(newCases)+0.00000001;
        allCumCases[-len(newCases):,iCountry]=np.cumsum(newCases)
        allDeaths[-len(newDeaths):,iCountry]=newDeaths
        cumDeaths=np.cumsum(newDeaths)
        allCumDeaths[-len(newDeaths):,iCountry]=cumDeaths
        roi=newCases[1:]/(cumCases[:-1]+1)
        rod=newDeaths[1:]/(cumDeaths[:-1]+1)
        rod[rod>1]=0;
        rod4=np.convolve(rod,np.ones(4),mode='same')/4
        allData[-len(newCases):,iCol]=newCases
        allData[-len(newDeaths):,iCol+1]=newDeaths
        allData[-len(cumCases):,iCol+2]=cumCases
        allData[-len(cumDeaths):,iCol+3]=cumDeaths
        allData[-len(cumDeaths):,iCol+4]=cumDeaths/(cumCases+1)
        allData[-len(roi):,iCol+5]=roi
        allData[-len(rod):,iCol+6]=rod
        allData[-len(rod):,iCol+7]=rod4
        allData[-len(cumCases):,iCol+8]=cumCases/pop*1000000
        allData[-len(cumDeaths):,iCol+9]=cumDeaths/pop*1000000
        allData[-len(cumDeaths):,iCol+10]=cumDeaths/pop*1000000
        allData[-len(cumDeaths):,iCol+11]=cumDeaths/pop*1000000
        xBar=np.arange(nDaysBar)*dayWidth
        for iCms in range(len(cms)):
            if barchart[iCms]==1:
                maxThis=np.max(allData[-nDaysBar:,iCol+iCms]);
                ax[iCms].bar(xBar+iCountry*countryWidth+dayWidth/10,allData[-nDaysBar:,iCol+iCms],
                             countryWidth,label=countries[iCountry],color=colors[iCountry])
            elif iCms!=11 and iCms!=10:
                maxThis=np.max(allData[-nDaysLine:,iCol+iCms]);
                ax[iCms].plot(dates[nDaysLine-1::-1],allData[-nDaysLine:,iCol+iCms],marker='o',
                              color=colors[iCountry],linewidth=3)
            elif iCms==10:
                 maxThis=1.0;
                 data=allData[-len(cumDeaths):,iCol+iCms]
                 if max(data)>20  and pop>3000000:            # Don't plot countries with <50 deaths per million
                     data=data/max(data)
                     data=data[data>0.01]
                     if len(data)>0:
                         ax[iCms].plot(np.arange(len(data))/len(data),data,marker='o',color=colors[iCountry],linewidth=3)
                 else:
                     ax[iCms].plot(nullxy,nullxy,'o',color=colors[iCountry],linewidth=3)
            elif iCms==11:
                 maxThis=np.max(allData[-nDaysLine:,iCol+iCms]);
                 data=allData[-len(cumDeaths):,iCol+iCms]
                 data=data[data>10]
                 ax[iCms].plot(range(len(data)),data,marker='o',color=colors[iCountry],linewidth=3)
            if maxy[iCms]<maxThis:
                maxy[iCms]=maxThis
            allCNames=allCNames.append({'CNames':countries[iCountry]+cms[iCms]},ignore_index=True)
        iCol=iCol+len(cms)
        #plt.pause(0.1)
        print(countries[iCountry],len(newCases),pop)
    dates=dates[0:nDaysLine]
    daysPerLabelBar=int(np.round(nDaysBar/14))
    daysPerLabelLine=int(np.round(nDaysLine/14))
    for iAx in range(len(cms)):
        plt.figure(iAx)
        ax[iAx].grid('on', linewidth=0.5)
        axs=np.array(plt.axis('tight'))
        ax[iAx].legend(countries)
        ax[iAx].set_title(cms[iAx])
        axs[2]=0;axs[0]=0;
        if barchart[iAx]==1:
            axs[1]=nDaysBar
            ax[iAx].set_xticklabels(dates[nDaysBar-1::-daysPerLabelBar])
            ax[iAx].set_xticks(np.arange(0,nDaysBar,daysPerLabelBar))
        elif iAx==10:
            axs[1]=1
            ax[iAx].set_xticks(np.arange(0,1,0.1))
        else:
            axs[1]=nDaysLine
            ax[iAx].set_xticks(np.arange(0,nDaysLine,daysPerLabelLine))
        if percent[iAx]==1:
            if maxy[iAx]<0.2:
                ax[iAx].set_yticks(np.arange(0,maxy[iAx],0.01))
            else:    
                ax[iAx].set_yticks(np.arange(0,maxy[iAx],0.05))
            ax[iAx].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))
        plt.axis(axs)
        plt.xlabel('Day')
        plt.tight_layout()
        plt.savefig(os.path.join(covidDir, cms[iAx]+today+'.png'))
    df=pd.DataFrame(allData[-len(dates):,:],dates[::-1],allCNames.CNames)
    df.to_csv(os.path.join(covidDir, today+'.csv'))
    plt.show()
    time.sleep(0.01)
    print('The End')
    #plt.close('all')

#
plt.close('all')
cvprocess(covidDir)


