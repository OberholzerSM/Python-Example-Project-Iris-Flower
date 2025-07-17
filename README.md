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
  <p align="center">
  <img src="/Images/IrisSetosa.jpg" width="150"/>
  </p>
  <figcaption>
    <p align="center">
    Fig. 1: Iris Setosa.<br />
    CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=170298 (15.07.2025)
    </p>
  </figcaption>
</figure>

<figure>
  <p align="center">
  <img src="/Images/IrisVersicolor.jpg" width="150"/>
  </p>
  <figcaption>
    <p align="center">
    Fig. 2: Iris Versicolor.<br />
    By No machine-readable author provided. Dlanglois assumed (based on copyright claims). - No machine-readable source provided. <br />
    Own work assumed (based on copyright claims)., CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=248095 (15.07.2025)
    </p>
  </figcaption>
</figure>

<figure>
  <p align="center">
  <img src="/Images/IrisVirginica.jpg" width="150"/>
  </p>
  <figcaption>
    <p align="center">
    Fig. 3: Iris Virginica.<br />
    By Frank Mayfield - originally posted to Flickr as Iris virginica shrevei BLUE FLAG, CC BY-SA 2.0,<br />
    https://commons.wikimedia.org/w/index.php?curid=9805580 (15.07.2025)
    </p>
  </figcaption>
</figure>

## Choosing a Feature to Examine

<p align="justify"> 
In order to identify the species of a given iris, one ideally wants to only do as few measurements as necessary. In order to determine what feature one should pick, one can take a look on how the features are distributed for the different species of iris as shown in Fig. 4. For both the sepal lengths and widths, there is a considerable overlap between the three different iris, making them unsuited for identifying the species. The petal lengths and widths fare better in that regard, though there is still an overlap between versicolor and virginica.
</p>

<figure>
  <p align="center">
  <img src="/Images/01IrisHistograms.png" width="500"/>
  </p>
  <figcaption>
    <p align="center">
    Fig. 4: Histograms displaying the distribution of the four measured iris features.
    </p>
  </figcaption>
</figure>

<p align="justify"> 

In order to determine which of the four features one should pick, one needs a concrete way of quantifying how "different" two distributions are from each other: The larger the difference, the easier it will be to identify the species. One possible candidate for such a difference is the so-called *Kullback–Leibler divergence* $D_{KL}(P \parallel Q)$, which can be thought of as denoting how much information is lost when one goes from a "true" probability density $P$ to an approximation $Q$. We can reappropriate this as a distance-measure, since the information loss will be small for overlapping distributions and large otherwise. Unlike what is required for a distance-measure, the KL-divergence is however not symmetric,

$$ D_{KL}(P \parallel Q) = \int_{-\infty}^{+\infty} p(x) \\, ln \left( \frac{p(x)}{q(x)}  \right) \\: .$$

We can symmetrize our approach by simply taking the sum,

$$ D(P,Q) = D_{KL}(P \parallel Q) + D_{KL}(Q \parallel P) \\: .  $$

Furthermore, for two normal distributions the KL-divergence takes on the form,

$$ D_{KL}(\mathcal{N}_1 \parallel \mathcal{N}_2) = ln\\left(\frac{\sigma_2}{\sigma_1}\\right) + \frac{\sigma_1^2 + (\mu_1 - \mu_2)^2}{2 \sigma_2^2} - \frac{1}{2} \\: . $$

Next, we need to assign a probability distribution to the features. Based on the histograms in Fig. 4, we assume that the individual features are following a normal distribution $\mathcal{N}(\mu_{I_i},\sigma_{I_i})$, where $I_i$ denotes a given iris species, $I_i \in \\{ \text{setosa, versicolor, virginica} \\}$. However, we also need to take into account the measurement error of our data: While the error is not directly specified, the measurements are only given up to one digit of precicion. We therefor assume that if for example the data denotes a petal width of 1.4 cm, that the "true" petal width lies somewhere within the range of 1.35 cm to 1.45 cm. For the likelihoods, this yields:

$$ P[ Z = z | I_i ] = \int_{z-0.05}^{z+0.05} f(x|\mu_{I_i},\sigma_{I_i}) dx \\: , $$

where $Z$ represents one of the four features taking on the value $z$ and where $f(x|\mu_{I_i},\sigma_{I_i})$ is the probability density function of $\mathcal{N}(\mu_{I_i},\sigma_{I_i})$. <br /> The resulting likelihood distributions can be seen in Fig. 5. As can be seen, they more or less simply follow along the histograms of Fig. 4.

</p>

<figure>
  <p align="center">
  <img src="/Images/02Likelihoods.png" width="500"/>
  </p>
  <figcaption>
    <p align="center">
    Fig. 5: Likelihood probability distributions for the four features.
    </p>
  </figcaption>
</figure>

<p align="justify"> 
We can now determine the distance between the different likelihood distributions, summarized in the table below. As expected, for the sepal length and width the distances are rather small, making them unsuited for identifying the iris species. The petal length is optimal for differentiating between a setosa and the other two species, while the petal width is best suited for differentiating between a versicolor and a virginica. Since the distance between the versicolor and virginica distributions are always unfortunately small for all features, the major difficulty will always be to differeniate these two species. For setosa on the other hand, the distance to the other species for both the petal length and width is rather large, making it easy to identify a setosa either way. Hence, if one only wishes to measure a single feature per flower, the petal width should be chosen in order to best identify the species.
</p>

| Iris                  | Sepal Length  |  Sepal Width  |  Petal Length  |  Petal Width   |
| -------------         | ------------- | ------------- |  ------------- |  ------------- |
| setosa/versicolor     | 5.41          |  3.78         |   150.25       |   68.33        |
| setosa/virginica      | 13.95         |  1.76         |   308.89       |   166.11       |
| versicolor/virginica  | 1.41          |  0.41         |   6.57         |   9.74         |

## Determining the Posterior Distributions for a Single Variable

<p align="justify"> 


  
</p>

tba
