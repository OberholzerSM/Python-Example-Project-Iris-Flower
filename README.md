# Python Example Project: Iris Flower

## Introduction

<p align="justify"> 
The iris genus includes three species of flowers: setosa, versicolor and virginica. In this example project, we will examine a dataset that contains measurements of the petal length and width as well as the sepal length and width of 150 irises. The goal is to determine whether one can use one or more of these features to uniquely identify the species of an iris.
<p align="justify"> 

The dataset was first published by R. A. Fisher:<br />
_Fisher, R. A. (1936) The use of multiple measurements in taxonomic problems. Annals of Eugenics, 7, Part II, 179–188._ <br /> 
_doi:10.1111/j.1469-1809.1936.tb02137.x._ 

The data itself was collected by E. Anderson:<br />
_Anderson, Edgar (1935). The irises of the Gaspe Peninsula, Bulletin of the American Iris Society, 59, 2–5._ 

<figure>
  <img src="/Images/IrisSetosa.jpg" width="150"/>
  <figcaption>
    Fig. 1: Iris Setosa.<br />
    CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=170298 (15.07.2025)
  </figcaption>
</figure>

<figure>
  <img src="/Images/IrisVersicolor.jpg" width="150"/>
  <figcaption>
    Fig. 2: Iris Versicolor.<br />
    By No machine-readable author provided. Dlanglois assumed (based on copyright claims). - No machine-readable source provided. <br />
    Own work assumed (based on copyright claims)., CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=248095 (15.07.2025)
  </figcaption>
</figure>

<figure>
  <img src="/Images/IrisVirginica.jpg" width="150"/>
  <figcaption>
    Fig. 3: Iris Virginica.<br />
    By Frank Mayfield - originally posted to Flickr as Iris virginica shrevei BLUE FLAG, CC BY-SA 2.0,<br />
    https://commons.wikimedia.org/w/index.php?curid=9805580 (15.07.2025)
  </figcaption>
</figure>

## Choosing a Feature to Examine

<p align="justify"> 
In order to identify the species of a given iris, one ideally wants to only do as few measurements as necessary. Hence, we will start by only examining a single feature. In order to determine what feature one should pick, one can take a look on how the features are distributed among the different species of iris, as shown in Fig. 4. For both the sepal lengths and widths, there is a considerable overlap between the three different iris, making them unsuited for identifying the species. The petal lengths and widths fare better in that regard, though there is still an overlap between versicolor and virginica.
wip
</p>

<figure>
  <img src="/Images/01IrisHistograms.png" width="500"/>
  <figcaption>
    Fig. 4: Histograms displaying the distribution of the four measured iris features.
  </figcaption>
</figure>

## Determining the Posterior Distribution for a Single Variable

<p align="justify"> 
Based on the histograms in Fig. 4, we assume that the petal widths $pw$ are following a normal distribution $\mathcal{N}(\mu_{I_i},\sigma_{I_i})$, where $I_i$ denotes a given iris species, $I_i \in \{ \text{setosa, versicolor, virginica} \}$. However, we also need to take into account the measurement error of our data: While the error is not directly specified, the petal widths are given up to one digit of precicion. We therefor assume for the likelihoods:

$$ P[ pw = PW | I_i ] = \int_{PW-0.05}^{PW+0.05} f(x|\mu_{I_i},\sigma_{I_i}) dx $$

where $f(x|\mu_{I_i},\sigma_{I_i})$ is the probability density function of $\mathcal{N}(\mu_{I_i},\sigma_{I_i})$. The resulting Likelihood distribution can be seen in Fig. 5.
  
</p>

wip
