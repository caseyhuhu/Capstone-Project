#Imports
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
from tslearn.utils import *
from tslearn.clustering import TimeSeriesKMeans
from contextlib import redirect_stdout


def plotClusters(clusterPredictions, formatted_dataset, km, numClusters,companyNames):
    ##alternative for putting all clusters in one window
    ##plt.figure(figsize=(15,15))
    for cluster in range(numClusters):
        plt.figure()
        ##plt.subplot(numClusters, 1, cluster + 1)
        for j in range(0,len(formatted_dataset)):
            if(clusterPredictions[j] == cluster):
                xx = formatted_dataset[j]
                plt.plot(xx.ravel(), alpha=.2, label=companyNames[j]) #"k-"
        plt.plot(km.cluster_centers_[cluster].ravel(), "r-", label='Cluster Center') 
        plt.title("KMCluster " + str(cluster+1))
        plt.legend(bbox_to_anchor=(1, 1))
        #plt.show()
    
    #plt.tight_layout()
    plt.show()

    #Split companies into their own data structures
#Format each company to a time series for use with tslearn
def formatCompanies(companiesCSV,numCompanies,numQuarters = 33):
    companyNames = []
    companyStockPrices = []
    formatted_time_series = []
    
    for company in range(0,numCompanies):
        companyNames.append(companiesCSV.index.values[company*numQuarters])
        companyStockPrices.append(companiesCSV[company*numQuarters:(
            company+1)*numQuarters].filter(items=['Stock price']))
        
        initialStockPrice = companyStockPrices[company].iloc[0,0]
        for stockPrice in range(0,len(companyStockPrices[company])):
            companyStockPrices[company].iloc[stockPrice,0] -= initialStockPrice
        companyStockPrices[company] = companyStockPrices[company].T
        companyStockPrices[company] = companyStockPrices[company].to_numpy()
        formatted_time_series.append(to_time_series(companyStockPrices[company]))
    return companyNames, companyStockPrices, formatted_time_series


def getInertia(capturedOutput):
    inertiaOutput = capturedOutput.getvalue()
    allInertias = str.split(inertiaOutput,' --> ')
    finalInertia = allInertias[-2]
    return finalInertia

def runKMeans(formatted_dataset, seed, numCompanies):
    numClusters = runKMeansPlusPLus(formatted_dataset, seed, numCompanies)
    km = TimeSeriesKMeans(n_clusters=numClusters,metric="euclidean",
                                  random_state=seed,n_init=3)   
    return km.fit_predict(formatted_dataset), km

def runKMeansPlusPLus(formatted_dataset, seed, numCompanies):
    allInertias = []
    companyAxis = []
    for i in range(1,numCompanies+1):
        numClusters = i
        km = TimeSeriesKMeans(n_clusters=numClusters,metric="euclidean",verbose=True,
                                  random_state=seed,n_init=3)
       
        capturedOutput = io.StringIO()
        with redirect_stdout(capturedOutput):
            clusterPredictions = km.fit_predict(formatted_dataset)
        inertia = getInertia(capturedOutput)
        allInertias.append(float(inertia))
        companyAxis.append(i)
        
    
    
    plt.figure()
    plt.scatter(companyAxis,allInertias)

    inDistances = getLineDistances(allInertias)
    print(inDistances)

    plt.scatter(companyAxis,inDistances)
    plt.show()
    #return min{inDistancesIndex}

    return 4
   


def getLineDistances(allInertias):
    """
    firstInertia = allInertias[0]
    firstInertiaSquared = firstInertia**2
    numCompanies = len(allInertias)
    denominator = math.sqrt(firstInertiaSquared+(len(allInertias)-1)**2)
    distances = []
    for i in range(numCompanies):
        numerator = firstInertia*(numCompanies-i) - ((numCompanies-1)*allInertias[i])
        distances.append(numerator/denominator)
    return distances
    """
    
    numCompanies = len(allInertias)
    slope = (-1)*allInertias[0]/(numCompanies-1)
    slopeSquared = slope**2
    #denominator = math.sqrt(slopeSquared+1)
    #print("denominator: " + str(denominator))
    distances = []
    a = slope
    b = -1
    c = allInertias[0] - slope
    denominator = math.sqrt(a*a + b*b)
    for i in range(numCompanies):
        x = i
        y = allInertias[i]
        numerator = math.fabs(a*x + b*y + c)
        print("numerator" + str(i) + ": " + str(numerator))
        distances.append(numerator/denominator)
    x = np.linspace(0,10,100)
    y = slope*x+allInertias[0] - slope
    plt.plot(x,y,'-r')
    return distances



def main():
    numCompanies = 9
    seed = 0
    np.random.seed(seed)
    
    #Get Companies
    companiesCSV = pd.read_csv('Combined_data.csv',index_col = 0)
    companyNames, companyStockPrices, formatted_time_series = formatCompanies(
        companiesCSV,numCompanies)
    
    formatted_dataset = to_time_series_dataset(formatted_time_series)
    sz = formatted_dataset.shape[1]
    
    clusterPredictions, km = runKMeans(formatted_dataset, seed,numCompanies)
    
    #plotClusters(clusterPredictions, formatted_dataset, km, 4,companyNames)
    
    
    
if __name__ == "__main__":
    main()