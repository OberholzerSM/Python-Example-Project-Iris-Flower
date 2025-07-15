#%% Import Libraries and the Data

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import multivariate_normal

df = pd.read_csv('Iris_data.csv', sep = ';')
df = df.drop(columns = ["Index"])

attributes = np.array(["Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width"])
names = np.array(["setosa","versicolor","virginica"])

#%% Histogram Plots

maxdf = df.max()
maxValue = math.ceil(max(maxdf["Sepal.Length"],maxdf["Petal.Length"]))

binWidth = 0.5
binCustom=np.arange(0.0, maxValue + binWidth, binWidth)

for i in range(0,attributes.size):
    attribute = attributes[i]
    for name in names:
        plt.subplot(2,2,i+1)
        df[attribute].loc[df.Species == name].hist(bins=binCustom, edgecolor='black',grid=False)
    plt.xlabel(attribute + " [cm]")
    plt.ylim([0,50])
plt.legend(names)
plt.suptitle("Histograms Flower Properties")
plt.tight_layout()
plt.savefig("01IrisHistograms.png")
plt.show()

#%% posteriorPL Petal Length
muPL = np.zeros(3)
sigmaPL = np.zeros(3)
for i in range(0,3):
    name = names[i]
    muPL[i] = df["Petal.Length"].loc[df.Species == name].mean()
    sigmaPL[i] = df["Petal.Length"].loc[df.Species == name].std()

valuesPL = np.linspace(0.0,maxValue,num=(2*maxValue+1))
likelihoodPL = np.zeros((names.size,valuesPL.size))
evidencePL = np.zeros(valuesPL.size)
posteriorPL = np.zeros((names.size,valuesPL.size))

for j in range(0,valuesPL.size):
    for i in range(0,names.size):
        likelihoodPL[i][j] = norm.cdf(valuesPL[j]+0.05,loc=muPL[i],scale=sigmaPL[i]) - norm.cdf(valuesPL[j]-0.05,loc=muPL[i],scale=sigmaPL[i])
        evidencePL[j] += likelihoodPL[i][j]
    for i in range(0,names.size):
        posteriorPL[i][j] = likelihoodPL[i][j] / evidencePL[j]

#%% posteriorPL Petal Length Plots

for i in range(0,names.size):
    plt.plot(valuesPL,100*likelihoodPL[i])
plt.legend(names)
for i in range(0,names.size):
    plt.scatter(valuesPL,100*likelihoodPL[i])
plt.xlabel("Petal.Length [cm]")
plt.ylabel("Likelihood [%]")
plt.title("Likelihood Distribution Petal Length")
plt.savefig("02IrisLikelihoodPL.png")
plt.show()

for i in range(0,names.size):
    plt.plot(valuesPL,100*posteriorPL[i])
plt.legend(names)
for i in range(0,names.size):
    plt.scatter(valuesPL,100*posteriorPL[i])
plt.xlabel("Petal Length [cm]")
plt.ylabel("Posterior [%]")
plt.title("Posterior Distribution Petal Length")
plt.savefig("03IrisPosteriorPL.png")
plt.show()

#%% Correlation Plots Petal Length

attributes2 = ["Sepal.Length","Sepal.Width","Petal.Width"]
i = 1
for attribute in attributes2:
    for name in names:
        plt.subplot(2,2,i)
        plt.scatter(df[attribute].loc[df.Species == name],df["Petal.Length"].loc[df.Species == name])
    plt.xlabel(attribute + " [cm]")
    plt.ylabel("Petal.Length [cm]")
    i += 1
plt.suptitle("Correlation Plots for Petal Length")
plt.tight_layout()
plt.legend(names,loc = "upper right", bbox_to_anchor=(2.0, 0.75))
plt.savefig("04IrisCorrelationPL.png")
plt.show()

#%% Average Correlation

avgSL = 0
avgSW = 0
avgPW = 0

for name in names:
    print(name)
    corr = df.loc[df.Species==name].corr(numeric_only=True)
    avgSL += corr["Petal.Length"][0]
    avgSW += corr["Petal.Length"][1]
    avgPW += corr["Petal.Length"][3]
    print(corr)
    print("")

print(avgSL/3)
print(avgSW/3)
print(avgPW/3)

#%% Posterior Petal Length and Sepal Width

attributes3 = ["Petal.Length","Sepal.Width"]

mu = np.zeros((3,2))
sigma = np.zeros((3,2,2))
for i in range(0,3):
    name = names[i]
    for j in range(0,2):
        attribute = attributes3[j]
        mu[i][j] = df[attribute].loc[df.Species == name].mean()
    sigma[i] = np.cov(df.loc[df.Species==name]["Petal.Length"],df.loc[df.Species==name]["Sepal.Width"])

valuesPL = np.linspace(0.0,8.0,num=(2*8+1))
valuesSW = np.linspace(2.0,5.0,num=(2*(5-2)+1))
likelihood = np.zeros((names.size,valuesPL.size,valuesSW.size))
evidence = np.zeros((valuesPL.size,valuesSW.size))
posterior = np.zeros((names.size,valuesPL.size,valuesSW.size))

def L_Calculator(i,j,k):
    termLL = multivariate_normal.cdf([valuesPL[j]-0.05,valuesSW[k]-0.05],mean=mu[i],cov=sigma[i], allow_singular=True)
    termUU = multivariate_normal.cdf([valuesPL[j]+0.05,valuesSW[k]+0.05],mean=mu[i],cov=sigma[i], allow_singular=True)
    termLU = multivariate_normal.cdf([valuesPL[j]-0.05,valuesSW[k]+0.05],mean=mu[i],cov=sigma[i], allow_singular=True)
    termUL = multivariate_normal.cdf([valuesPL[j]+0.05,valuesSW[k]-0.05],mean=mu[i],cov=sigma[i], allow_singular=True)
    return termLL + termUU - termLU - termUL

for j in range(0,valuesPL.size):
    for k in range(0,valuesSW.size):
        for i in range(0,names.size):
            likelihood[i][j][k] = L_Calculator(i,j,k)
            evidence[j][k] += likelihood[i][j][k]
        for i in range(0,names.size):
            posterior[i][j][k] = likelihood[i][j][k] / evidence[j][k]

#%% Posterior Petal Length and Sepal Width Plots

for j in range(9,11):
    for i  in range(0,3):
        plt.plot(valuesSW,100*posterior[i][j])
    plt.legend(names,loc="upper right")
    for i  in range(0,3):
        plt.scatter(valuesSW,100*posterior[i][j])
    plt.hlines(100*posteriorPL[1][j],valuesSW[0],valuesSW[6],colors=['C1'],linestyles='dashed')
    plt.hlines(100*posteriorPL[2][j],valuesSW[0],valuesSW[6],colors=['C2'],linestyles='dashed')
    plt.xlabel("Sepal.Width [cm]")
    plt.ylabel("Posterior [%]")
    plt.title(f"Posterior Distribution Sepal Width for Petal Length {valuesPL[j]} cm")
    plt.savefig(f"0{j-4}IrisPosteriorPLSW{valuesPL[j]}.png")
    plt.show()

#%% Posterior Petal Length and Sepal Width Heatmap

for i in range(0,3):
    plt.subplot(3,1,i+1)
    plt.imshow( np.transpose(posterior[i]), cmap='hot', interpolation='nearest', extent = (min(valuesPL),max(valuesPL),min(valuesSW),max(valuesSW)))
    if(i==1):
        plt.ylabel("Sepal Width [cm]")
    plt.title(names[i])
plt.xlabel("Petal.Length [cm]")
plt.tight_layout()
plt.savefig("07IrisPosteriorPLSWHeatmap.png")
plt.show()