#%% Import Libraries and load the Data

from os import chdir, getcwd
chdir(getcwd())

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, multivariate_normal

df = pd.read_csv('Iris_data.csv', sep = ';')
df = df.drop(columns = ["Index"])

features = np.array(["Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width"])
names = np.array(["setosa","versicolor","virginica"])
    
maxdf = df.max()
maxValue = math.ceil(max(maxdf["Sepal.Length"],maxdf["Petal.Length"]))
values = np.arange(0.0,maxValue+0.1,0.1)

#%% Histogram Plots

binWidth = 0.5
binCustom=np.arange(0.0, maxValue + binWidth, binWidth)

for i in range(0,features.size):
    feature = features[i]
    for name in names:
        plt.subplot(2,2,i+1)
        df[feature].loc[df.Species == name].hist(bins=binCustom, edgecolor='black',grid=False)
    plt.xlabel(feature + " [cm]")
    plt.ylim([0,50])
plt.legend(names)
plt.suptitle("Histograms Iris Features")
plt.tight_layout()
plt.savefig("01IrisHistograms.png")
plt.show()

#%% Likelihoods

mu = np.zeros((names.size,features.size))
sigma = np.zeros((names.size,features.size))
likelihood = np.zeros((names.size,features.size,values.size))

for i in range(0,names.size):
    name = names[i]
    for j in range(0,features.size):
        feature = features[j]
        mu[i][j] = df[feature].loc[df.Species == name].mean()
        sigma[i][j] = df[feature].loc[df.Species == name].std()
        likelihood[i][j] = norm.cdf(values+0.05,loc=mu[i][j],scale=sigma[i][j]) - norm.cdf(values-0.05,loc=mu[i][j],scale=sigma[i][j])


#%% Likelihood Plots

for j in range(0,features.size):
    feature = features[j]
    for i in range(0,names.size):
        plt.subplot(2,2,j+1)
        plt.plot(values,100*likelihood[i][j])
    plt.xlabel(feature + " [cm]")
    plt.ylim([0,35])
plt.legend(names)
plt.suptitle("Likelihood Probability Distributions")
plt.tight_layout()
plt.savefig("02Likelihoods.png")
plt.show()

#%% KL-Divergence

def KLDiv(mu1,mu2,sigma1,sigma2):
    return ( ( math.pow(sigma1,2) + math.pow(mu1-mu2,2)) / (2.0*math.pow(sigma2,2)) ) - 0.5

for name in names[1:3]:
    print("setosa,",name)
    for feature in features:
        mu1 = df[feature].loc[df.Species == "setosa"].mean()
        mu2 = df[feature].loc[df.Species == name].mean()
        sigma1 = df[feature].loc[df.Species == "setosa"].std()
        sigma2 = df[feature].loc[df.Species == name].std()
        
        kl1 = KLDiv(mu1,mu2,sigma1,sigma2)
        kl2 = KLDiv(mu2,mu1,sigma2,sigma1)
        
        print(feature,"\t",f"{kl1+kl2:.2f}")
    print("")

print("versicolor,","virginica")
for feature in features:
    mu1 = df[feature].loc[df.Species == "versicolor"].mean()
    mu2 = df[feature].loc[df.Species == "virginica"].mean()
    sigma1 = df[feature].loc[df.Species == "versicolor"].std()
    sigma2 = df[feature].loc[df.Species == "virginica"].std()
    
    kl1 = KLDiv(mu1,mu2,sigma1,sigma2)
    kl2 = KLDiv(mu2,mu1,sigma2,sigma1)
    
    print(feature,"\t",f"{kl1+kl2:.2f}")

#%% Posterior Single Values

evidence = np.zeros((features.size,values.size))
posterior = np.zeros((names.size,features.size,values.size))

for j in range (0,features.size):
    feature = features[j]
    for i in range(0,names.size):
        evidence[j] += likelihood[i][j]
    for i in range(0,names.size):
        for k in range(0,values.size):
            if(evidence[j][k] > 0.0):
                posterior[i][j][k] = likelihood[i][j][k] / evidence[j][k]
            elif (likelihood[i][j][k] > 0.0):                   #Evidence much smaller than likelihood
                posterior[i][j][k] = 1.0
            elif(k > 0):                                        #Continue the previous trend
                posterior[i][j][k] = posterior[i][j][k-1]
            else:                                               #Region of complete underflow
                posterior[i][j][k] = 0.0
            posterior[i][j][k] = min( 1.0, posterior[i][j][k] )

#%% Posterior Single Values Plot

for j in range(0,features.size):
    feature = features[j]
    for i in range(0,names.size):
        plt.subplot(2,2,j+1)
        plt.plot(values,100*posterior[i][j])
    plt.xlabel(feature + " [cm]")
plt.legend(names)
plt.suptitle("Posterior Probability Distributions")
plt.tight_layout()
plt.savefig("03Posteriors.png")
plt.show()

#%% Posterior Petal Width Plot

feature = "Petal.Width"
for i in range(0,names.size):
    plt.plot(values[0:31],100*posterior[i][3][0:31])
plt.legend(names)
for i in range(0,names.size):
    plt.scatter(values[0:31],100*posterior[i][3][0:31])
plt.grid()
plt.xlabel(feature + " [cm]")
plt.ylabel("Posterior [%]")
plt.title("Posterior Petal Width")
plt.tight_layout()
plt.savefig("04PosteriorPW.png")
plt.show()

#%% Correlations Petal Width Plot

for j in range(0,3):
    feature = features[j]
    for name in names:
        plt.subplot(2,2,j+1)
        plt.scatter(df[feature].loc[df.Species == name],df["Petal.Width"].loc[df.Species == name])
    plt.xlabel(feature + " [cm]")
    plt.ylabel("Petal.Width [cm]")
plt.suptitle("Correlation Plots for Petal Width")
plt.tight_layout()
plt.legend(names,loc = "upper right", bbox_to_anchor=(2.0, 0.75))
plt.savefig("05CorrelationPW.png")
plt.show()

#%% Posterior Petal Width and Petal Length

#Covariance Matrix
mu2 = mu[:,2:4]
Sigma2 = np.zeros((names.size,2,2))
for i in range(0,names.size):
    name = names[i]
    Sigma2[i] = np.cov(df.loc[df.Species==name]["Petal.Length"],df.loc[df.Species==name]["Petal.Width"])
        
def L_Calculator(i,k1,k2):
    termLL = multivariate_normal.cdf([values[k1]-0.05,values[k2]-0.05],mean=mu2[i],cov=Sigma2[i], allow_singular=True)
    termUU = multivariate_normal.cdf([values[k1]+0.05,values[k2]+0.05],mean=mu2[i],cov=Sigma2[i], allow_singular=True)
    termLU = multivariate_normal.cdf([values[k1]-0.05,values[k2]+0.05],mean=mu2[i],cov=Sigma2[i], allow_singular=True)
    termUL = multivariate_normal.cdf([values[k1]+0.05,values[k2]-0.05],mean=mu2[i],cov=Sigma2[i], allow_singular=True)
    result = termLL + termUU - termLU - termUL
    if(result > 0):
        return result
    else:
        return 0

valuesPL = values
valuesPW = values[0:31]
likelihood2 = np.zeros((names.size,valuesPL.size,valuesPW.size))
evidence2 = np.zeros((valuesPL.size,valuesPW.size))
posterior2 = np.zeros((names.size,valuesPL.size,valuesPW.size))

for k1 in range(0,valuesPL.size):
    for k2 in range(0,valuesPW.size):
        for i in range(0,names.size):
            likelihood2[i][k1][k2] = L_Calculator(i,k1,k2)
            evidence2[k1][k2] += likelihood2[i][k1][k2]
        for i in range(0,names.size):            
            if(evidence2[k1][k2] > 0):
                posterior2[i][k1][k2] = likelihood2[i][k1][k2] / evidence2[k1][k2]
            elif (likelihood2[i][k1][k2] > 0):
                posterior2[i][k1][k2] = 1.0
            elif (k1 > 0 and k2 > 0):
                posterior2[i][k1][k2] = (posterior2[i][k1-1][k2-1] + posterior2[i][k1][k2-1]  + posterior2[i][k1-1][k2]) / 3.0
            else:
                posterior2[i][k1][k2] = 0
            
            posterior2[i][k1][k2] = min(1.0, posterior2[i][k1][k2])

#%% Posterior Petal Width and Petal Length Heatmap

for i in range(0,3):
    plt.subplot(3,1,i+1)
    plt.imshow( posterior2[i], cmap='hot', interpolation='nearest', extent=(0.0,3.0,8.0,0.0), aspect='auto')
    if(i==1):
        plt.ylabel("Petal.Length [cm]")
    plt.title(names[i])
plt.xlabel("Petal.Width [cm]")
plt.tight_layout()
plt.savefig("06PosteriorPLPWHeatmap.png")
plt.show()

#%% Posterior Petal Width and Petal Length Plots

for i in range(0,names.size):
    plt.plot(valuesPL,100*posterior2[i,:,16])
plt.legend(names)
plt.grid()
plt.hlines(100*posterior[1][3][16], 0.0,8.0, colors=['C1'],linestyles='dashed')
plt.hlines(100*posterior[2][3][16], 0.0,8.0, colors=['C2'],linestyles='dashed')
plt.xlabel("Petal.Length [cm]")
plt.ylabel("Posterior [%]")
plt.title("Posterior Distributin Petal Length for Petal Width = 1.6 cm")
plt.savefig("07PosteriorPLPW.png")
plt.show()

for i in range(0,names.size):
    plt.plot(valuesPL,100*posterior2[i,:,17])
plt.legend(names)
plt.grid()
plt.hlines(100*posterior[1][3][17], 0.0,8.0, colors=['C1'],linestyles='dashed')
plt.hlines(100*posterior[2][3][17], 0.0,8.0, colors=['C2'],linestyles='dashed')
plt.xlabel("Petal.Length [cm]")
plt.ylabel("Posterior [%]")
plt.title("Posterior Distributin Petal Length for Petal Width = 1.7 cm")
plt.savefig("08PosteriorPLPW17.png")
plt.show()