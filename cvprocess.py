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
    IRLCasesToday=22        # if new data announced put here otherwise set to 0
    IRLDeathsToday=2
    nDaysLine=30            # No. of days to plot on line charts
    nDaysBar=14             # No. of days to plot on bar charts
    nDaysAverage=7          # no of days to average
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
    eurCountries=['AUT','BLR','BEL','BIH','BGR','HRV','CYP','DNK','EST','FIN','FRA','DEU','GRC','IRL',
                     'ITA','LUX','NLD','POL','PRT','ROU','SRB','SVK','SVN','ESP','SWE','CHE','GBR']
    #countries=['AUS','JPN']
    countries=['FRA','ITA', 'USA'        ,  'RUS',       'GBR','BRA',      'SWE','NLD','IRL']
    countries=['FRA','ITA', 'USA'        ,'PER',       'GBR','DEU','BRA',      'SWE','IRL']
    #countries=['IRL','SWE','BEL','USA','ITA','GBR','ISL','FIN','NZL']
    #countries=['NZL','JPN']
    colors=[[0,0.25,0.85],[0,0.7,1],[1,0,0],
            [0.0,0.0,0.0],[1,0.7,0],[0.63,0.63,0],
            [0.85,0.9,0],[0.7,0.0,0.7],[0,0.7,0],
            [0.45,0.45,0.45],[0.75,0.75,0.75],[0.0,0.55,0.70]]
    
    nCountries=len(countries)
    maxDays=200
    allCases=np.zeros((maxDays,nCountries))
    allCumCases=allCases
    allDeaths=allCases
    allCumDeaths=allCases
    stats=pd.read_csv(fname)
    euNewCases=np.zeros(maxDays)
    euNewDeaths=np.zeros(maxDays)
    euPop=0
    pop=np.zeros(len(countries))
    nullxy=np.arange(0,0.01,0.01)
    # Go through data for each Euro country
    for iEurCountry in range(len(eurCountries)):
        popd=stats.popData2019[stats.countryterritoryCode==eurCountries[iEurCountry]]
        popN=popd[popd.first_valid_index()]
        euPop=euPop+popN
        newCases=np.flipud(np.array(stats.cases[stats.countryterritoryCode==eurCountries[iEurCountry]]))
        newDeaths=np.flipud(np.array(stats.deaths[stats.countryterritoryCode==eurCountries[iEurCountry]]))
        euNewCases[-len(newCases):]=euNewCases[-len(newCases):]+newCases
        euNewDeaths[-len(newCases):]=euNewDeaths[-len(newCases):]+newDeaths
        
    allCNames = pd.DataFrame(columns=['CNames'])
    dayWidth=1      # width of each day
    countryWidth=dayWidth/(nCountries+2)
    deathAve='Deaths % Inc '+str(nDaysAverage)+' Day Ave'
    caseAve='Cases % Inc' +str(nDaysAverage)+' Day Ave'
    cms=['NewCases', 'NewDeaths', 'TotalCases',
         'TotalDeaths','CaseFatalityRate','CaseRateIncrease',
         'DeathRateIncrease',deathAve,caseAve,'CasesPer1M',
         'DeathsPer1M','Deaths Curve Shape (if DperM 20+)',
         'DeathsPerM Since 10perM',
         'NewCases '+str(nDaysAverage)+' Day Ave per Millon',
         'NewDeaths '+str(nDaysAverage)+' Day Ave per Million']
    barchart=np.array([1 ,       1,          0,             0,             0,                  1,           1,           0,              0,            0,            0,            0,            0,  0, 0])
    percent =np.array([0 ,       0,          0,             0,             1,                  1,           1,           1,              1,            0,            0,            1,            0, 0, 0])
    # Need an array of axes, there must be a better way to do it than this:
    fig, ax = plt.subplots(nrows=1, ncols=len(cms), figsize=(8, 20))
    plt.close(fig)
    for iChart in range(len(cms)):
        newf=plt.figure(iChart,figsize=(18, 10))
        plt.gcf().canvas.set_window_title(cms[iChart])
        if iChart>0:
            fig=np.append(fig,newf)
        else:
            fig=newf
        ax[iChart]=plt.axes()
    nCmsTotal=len(cms)*len(countries)
    allData=np.zeros((maxDays,nCmsTotal))
    iCol=0
    dates=[0]
    maxy=np.zeros( len(cms) )
    for iCountry in range(len(countries)):
        if countries[iCountry]=='EUR':
            pop[iCountry]=euPop
            newCases=euNewCases
            newDeaths=euNewDeaths
        else:
            popd=stats.popData2019[stats.countryterritoryCode==countries[iCountry]]
            pop[iCountry]=popd[popd.first_valid_index()]
            cdates=stats.dateRep[stats.countryterritoryCode==countries[iCountry]]
            if len(cdates)>len(dates):
                dates=cdates
            newCases=np.flipud(np.array(stats.cases[stats.countryterritoryCode==countries[iCountry]]))
            newDeaths=np.flipud(np.array(stats.deaths[stats.countryterritoryCode==countries[iCountry]]))
        if countries[iCountry]=='IRL' and IRLCasesToday>0:
            newCases=np.append(newCases[1:],IRLCasesToday)        # Add latest IRL cases
            newDeaths=np.append(newDeaths[1:],IRLDeathsToday)     # Add latest IRL deaths
        if countries[iCountry]=='IRL':
            iJump=np.where(newDeaths>200)[0][0]
            newDeaths[iJump-20:iJump]=newDeaths[iJump-20:iJump]+10
            newDeaths[iJump]=newDeaths[iJump]-200
            iJump=np.where(newCases==426)[0][0]
            newCases[iJump-40:iJump]=newCases[iJump-40:iJump]+6
            newCases[iJump]=newCases[iJump]-240
        allCases[-len(newCases):,iCountry]=newCases
        cumCases=np.cumsum(newCases)+0.00000001;
        allCumCases[-len(newCases):,iCountry]=np.cumsum(newCases)
        allDeaths[-len(newDeaths):,iCountry]=newDeaths
        cumDeaths=np.cumsum(newDeaths)
        allCumDeaths[-len(newDeaths):,iCountry]=cumDeaths
        roi=newCases[1:]/(cumCases[:-1]+1)
        rod=newDeaths[1:]/(cumDeaths[:-1]+1)
        rod[rod>1]=0;
        rodAve=np.convolve(rod,np.ones(nDaysAverage),mode='valid')/nDaysAverage
        roiAve=np.convolve(roi,np.ones(nDaysAverage),mode='valid')/nDaysAverage
        nCasesAve=np.convolve(newCases,np.ones(nDaysAverage),mode='valid')/nDaysAverage
        nDeathsAve=np.convolve(newDeaths,np.ones(nDaysAverage),mode='valid')/nDaysAverage
        allData[-len(newCases):,iCol]=newCases
        allData[-len(newDeaths):,iCol+1]=newDeaths
        allData[-len(cumCases):,iCol+2]=cumCases
        allData[-len(cumDeaths):,iCol+3]=cumDeaths
        allData[-len(cumDeaths):,iCol+4]=cumDeaths/(cumCases+1)
        allData[-len(roi):,iCol+5]=roi
        allData[-len(rod):,iCol+6]=rod
        allData[-len(rodAve):,iCol+7]=rodAve
        allData[-len(rodAve):,iCol+8]=roiAve
        allData[-len(cumCases):,iCol+9]=cumCases/pop[iCountry]*1000000
        allData[-len(cumDeaths):,iCol+10]=cumDeaths/pop[iCountry]*1000000
        allData[-len(cumDeaths):,iCol+11]=cumDeaths/pop[iCountry]*1000000
        allData[-len(cumDeaths):,iCol+12]=cumDeaths/pop[iCountry]*1000000
        allData[-len(nCasesAve):,iCol+13]=nCasesAve
        allData[-len(nDeathsAve):,iCol+14]=nDeathsAve
        xBar=np.arange(nDaysBar)*dayWidth
        for iChart in range(len(cms)):
            if barchart[iChart]==1:
                maxThis=np.max(allData[-nDaysBar:,iCol+iChart]);
                ax[iChart].bar(xBar+iCountry*countryWidth+dayWidth/10,allData[-nDaysBar:,iCol+iChart],
                             countryWidth,label=countries[iCountry],color=colors[iCountry])
            elif iChart==13 or iChart==14:
                maxThis=1;
                ax[iChart].plot(dates[nDaysLine-1::-1],allData[-nDaysLine:,iCol+iChart]/pop[iCountry]*1000000,marker='o',
                              color=colors[iCountry],linewidth=3)
            elif iChart!=12 and iChart!=11:
                maxThis=np.max(allData[-nDaysLine:,iCol+iChart]);
                ax[iChart].plot(dates[nDaysLine-1::-1],allData[-nDaysLine:,iCol+iChart],marker='o',
                              color=colors[iCountry],linewidth=3)
            elif iChart==11:
                 maxThis=1.0;
                 data=allData[-len(cumDeaths):,iCol+iChart]
                 if max(data)>20  and pop[iCountry]>3000000:            # Don't plot countries with <50 deaths per million
                     data=data/max(data)
                     data=data[data>0.01]
                     if len(data)>0:
                         ax[iChart].plot(np.arange(len(data))/len(data),data,marker='o',color=colors[iCountry],linewidth=3)
                 else:
                     ax[iChart].plot(nullxy,nullxy,'o',color=colors[iCountry],linewidth=3)
            elif iChart==12:
                 maxThis=np.max(allData[-nDaysLine:,iCol+iChart]);
                 data=allData[-len(cumDeaths):,iCol+iChart]
                 data=data[data>10]
                 ax[iChart].plot(range(len(data)),data,marker='o',color=colors[iCountry],linewidth=3)
            if maxy[iChart]<maxThis:
                maxy[iChart]=maxThis
            allCNames=allCNames.append({'CNames':countries[iCountry]+cms[iChart]},ignore_index=True)
        iCol=iCol+len(cms)
        #plt.pause(0.1)
        print(countries[iCountry],pop[iCountry])
        if countries[iCountry]=='IRL':
            print('IRL - Todays Cases average : '+str(int(nCasesAve[-1:]*10)/10))
            print('IRL - Todays Death average : '+str(int(nDeathsAve[-1:]*100)/100))
    dates=dates[0:nDaysLine]
    daysPerLabelBar=int(np.round(nDaysBar/14))
    daysPerLabelLine=int(np.round(nDaysLine/14))
    for iChart in range(len(cms)):
        plt.figure(iChart)
        ax[iChart].grid('on', linewidth=0.5)
        axs=np.array(plt.axis('tight'))
        ax[iChart].legend(countries)
        ax[iChart].set_title(cms[iChart])
        axs[2]=0;axs[0]=0;
        if barchart[iChart]==1:
            axs[1]=nDaysBar
            ax[iChart].set_xticklabels(dates[nDaysBar-1::-daysPerLabelBar])
            ax[iChart].set_xticks(np.arange(0,nDaysBar,daysPerLabelBar))
        elif iChart==11:
            axs[1]=1
            ax[iChart].set_xticks(np.arange(0,1,0.1))
        else:
            axs[1]=nDaysLine
            ax[iChart].set_xticks(np.arange(0,nDaysLine,daysPerLabelLine))
        if percent[iChart]==1:
            if maxy[iChart]<0.3:
                ax[iChart].set_yticks(np.arange(0,maxy[iChart],0.01))
            else:    
                ax[iChart].set_yticks(np.arange(0,maxy[iChart],0.05))
            ax[iChart].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))
        plt.axis(axs)
        plt.xlabel('Day')
        plt.tight_layout()
        plt.savefig(os.path.join(covidDir, cms[iChart]+today+'.png'))
    df=pd.DataFrame(allData[-len(dates):,:],dates[::-1],allCNames.CNames)
    df.to_csv(os.path.join(covidDir, today+'.csv'))
    nRow=int(np.round(np.sqrt(len(countries))))
    nCol=int(np.ceil((len(countries)/nRow)))
    titlestr=str(nDaysAverage)+' Day Average: Cases to Deaths Lag'
    fig, ax = plt.subplots(nrows=nRow, ncols=nCol, figsize=(18, 10),num=titlestr)
    labels = ['']*nDaysLine
    labels[-1:]=dates[:1]
    labels[:1]=dates[-1:]
    for ir in range(nRow):
        for ic in range(nCol):
            iChart=ir*nCol+ic
            ax[ir,ic].plot(dates[nDaysLine-1::-1],allData[-nDaysLine:,iChart*len(cms)+13]/max(allData[-nDaysLine:,iChart*len(cms)+13]),
                color=colors[iChart],linewidth=2)
            ax[ir,ic].plot(dates[nDaysLine-1::-1],allData[-nDaysLine:,iChart*len(cms)+14]/max(allData[-nDaysLine:,iChart*len(cms)+14]),
                color=colors[iChart],linewidth=4)
            ax[ir,ic].set_yticks(np.arange(0,1,0.1))
            ax[ir,ic].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))
            ax[ir,ic].set_xticks(np.arange(0,nDaysLine,3))
            ax[ir,ic].set_xticklabels(labels)
            ax[ir,ic].legend(['Cases','Deaths'])
            ax[ir,ic].grid('on', linewidth=0.5)
            plt.subplot(ax[ir,ic])
            plt.title(countries[iChart])
    fig.suptitle(titlestr, fontsize=24)
    plt.savefig(os.path.join(covidDir, 'DeathLag'+today+'.png'))
    titlestr=str(nDaysAverage)+' Day Averages by Population'
    fig, ax = plt.subplots(nrows=nRow, ncols=nCol, figsize=(18, 10),num=titlestr)
    labels = ['']*nDaysLine
    labels[-1:]=dates[:1]
    labels[:1]=dates[-1:]
    for ir in range(nRow):
        for ic in range(nCol):
            iChart=ir*nCol+ic
            ax[ir,ic].plot(dates[nDaysLine-1::-1],allData[-nDaysLine:,iChart*len(cms)+13]/pop[iChart]*100000,
                color=colors[iChart],linewidth=2)
            ax[ir,ic].plot(dates[nDaysLine-1::-1],allData[-nDaysLine:,iChart*len(cms)+14]/pop[iChart]*1000000,
                color=colors[iChart],linewidth=4)
            #ax[ir,ic].set_yticks(np.arange(0,1,0.1))
            #ax[ir,ic].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))
            ax[ir,ic].set_xticks(np.arange(0,nDaysLine,3))
            ax[ir,ic].set_xticklabels(labels)
            ax[ir,ic].legend(['Cases/day/100k','Deaths/day/1M'])
            ax[ir,ic].grid('on', linewidth=0.5)
            plt.subplot(ax[ir,ic])
            plt.title(countries[iChart])
            axs=np.array(plt.axis('tight'))
            axs[2]=0;axs[3]=18;
            plt.axis(axs)
    fig.suptitle(titlestr, fontsize=24)
    plt.savefig(os.path.join(covidDir, 'DeathLagPerM'+today+'.png'))
    plt.show()
    time.sleep(0.01)
    print('\nThe End')
    #plt.close('all')

#
plt.close('all')
cvprocess(covidDir)


