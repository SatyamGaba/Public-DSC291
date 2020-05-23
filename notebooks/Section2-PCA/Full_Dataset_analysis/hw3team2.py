class ghcnd:
    def __init__(self, pdf):
        import numpy as np
        self.pdf = pdf
        self.years = np.unique(self.pdf['Year'])
        self.graphs=[]
        for i in range(self.pdf.shape[0]):
            self.graphs.append([0 if x is None else 1 for x in self.pdf.iloc[i,3]])
        self.graphs=np.stack(self.graphs)
        self.lastDay2020 = 135
        
def getYearlyStats(self):
    import numpy as np
    import scipy.stats as st
    self.byyear=[]
    self.yearmean = []
    self.yearstderr = []
    for year in self.years:
        thisyear = []
        for i in range(self.graphs.shape[0]):
            if self.pdf['Year'][i] == year:
                thisyear.append(self.graphs[i,:])
        self.byyear.append(np.mean(thisyear, axis=0))
        self.yearmean.append(np.mean(np.mean(np.array(thisyear)[:,:self.lastDay2020], axis=1)))
        self.yearstderr.append(np.std(np.mean(np.array(thisyear)[:,:self.lastDay2020], axis=1)) / np.sqrt(len(thisyear)))
    self.byyear=np.stack(self.byyear)
    self.byyear_mean = np.mean(self.byyear[:-1,:], axis=0)
    self.byyear_std = np.std(self.byyear[:-1,:], axis=0)

    self.data2020 = self.byyear[-1,:self.lastDay2020]
    self.n2020 = len(self.data2020)
    self.days2020 = np.arange(1,self.n2020+1)
    self.zScores = (self.byyear_mean[:self.n2020] - self.data2020) / (self.byyear_std[:self.n2020] / np.sqrt(len(self.years)-1))
    self.pVals = 1 - st.norm.cdf(self.zScores)
        
def plotMeanByYear(self):
    import matplotlib.pylab as plt
    import numpy as np
    # linear fit number of days of smogs vs year
    z = np.polyfit(self.years[:-1],self.yearmean[:-1], 1)
    p = np.poly1d(z)
    
    fig1 = plt.figure(figsize=(7, 3), dpi= 80, facecolor='w', edgecolor='k')
    ax1 = fig1.add_axes([0,0,1,1])
    meanplot, = ax1.plot(self.years[:-1],self.yearmean[:-1],color='black',linestyle='-',label='mean')
    stdplot, = ax1.plot(self.years[:-1],np.array(self.yearmean[:-1])+np.array(self.yearstderr[:-1]),
                        color='black',linestyle=':',label='standard error')
    ax1.plot(self.years[:-1],np.array(self.yearmean[:-1])-np.array(self.yearstderr[:-1]),color='black',linestyle=':')
    fitplot, = ax1.plot(self.years[:],p(self.years[:]),color='blue',linestyle='-', label="fitting line")
    # point2020 = ax1.scatter(self.years[-1], self.yearmean[-1], color ='red', label="2020")
    point2020 = ax1.errorbar(self.years[-1], self.yearmean[-1], yerr=self.yearstderr[-1], fmt='o',ecolor='r',
                             elinewidth=0.5,capthick=0.5,capsize=5,mfc='white',mec='red', ms=6, label="2020 mean and error")
    ax1.set_title('empirical mean likelihood of smog/haze in the US through May 14, by year \n(mean of all stations)')
    ax1.set_ylabel('mean fraction of stations for which smog was reported')
    ax1.set_xlabel('year')
    ax1.legend(handles=[meanplot,stdplot,fitplot,point2020], loc='upper right')
    ax1.grid()
        
def plotMeanDaysOfYear(self):
    import matplotlib.pylab as plt
    import numpy as np
    from matplotlib import cm
    colmap = cm.get_cmap('jet', len(self.years)-1)
    colors = colmap(range(len(self.years)-1))
    
    import matplotlib
    import matplotlib.gridspec as gridspec
    fig = plt.figure(figsize=(8, 7), dpi= 80, facecolor='w', edgecolor='k')
    # gs = fig.add_gridspec(3, 1)
    gs = gridspec.GridSpec(ncols=1, nrows=3)
    ax1 = fig.add_subplot(gs[0:2, :])
    theLines = []
    if len(self.years)>30:
        for i in range(len(self.years)-1):
            yrplot, = ax1.plot(np.arange(1,366),self.byyear[i,:],color=colors[i,:3],alpha=0.5,lw=0.1,label=str(self.years[i])+'s')
            if int(self.years[i]) % 10 == 0:
                theLines.append(yrplot)
    else:
        for i in range(len(self.years)-1):
            yrplot, = ax1.plot(np.arange(1,366),self.byyear[i,:],color=[0.3, 0.3, 0.3],alpha=0.5,lw=0.3,label='individual years')
            if i == 0:
                theLines.append(yrplot)
    stdplot, = ax1.plot(np.arange(1,366),self.byyear_mean+self.byyear_std,color='black',linestyle=':',label='std')
    ax1.plot(np.arange(1,366),self.byyear_mean-self.byyear_std,color='black',linestyle=':')
    meanplot, = ax1.plot(np.arange(1,366),self.byyear_mean,color='black',lw=3,label='mean')
    mean2020, = ax1.plot(np.arange(1,136),self.byyear[-1,:135],color='red',alpha=1,lw=2,label='2020')
    ax1.set_title('mean empirical likelihood of smog throughout the year in the US ('+str(self.years[0])+'-2020)')
    ax1.set_ylabel('fraction of stations with smog observed')
    ax1.set_xlabel('day')
    ax1.set_xlim([1,365])
    allLines = [meanplot, stdplot, mean2020]
    for i in range(len(theLines)):
        allLines.append(theLines[i])
    ax1.legend(handles=allLines, loc='upper right')
    
    ax2 = fig.add_subplot(gs[2, :])
    pplot, = ax2.plot(self.days2020,self.pVals,color='black',linestyle='-',label='p-values')
    confplot, = ax2.plot(self.days2020,[0.05] * len(self.days2020),color='red',linestyle=':',label='95% confidence threshold')
    ax2.set_title('p-Values for the historical mean being greater than the 2020 Values\n(one-tailed Z-test)')
    ax2.set_ylabel('p-Value')
    ax2.set_xlabel('Day')
    ax2.legend(handles=[pplot,confplot], loc='upper right')
    plt.tight_layout()