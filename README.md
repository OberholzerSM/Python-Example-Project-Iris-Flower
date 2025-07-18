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

## Choosing a Feature to Determine the Species

<p align="justify"> 
In order to identify the species of a given iris, one ideally wants to only do as few measurements as necessary. We will start with the assumption that measuring a single feature will be sufficient in determining the species. In order to determine what feature one should pick, one can take a look on how the features are distributed for the different irises as shown in Fig. 4. For both the sepal lengths and widths, there is a considerable overlap between the three different irises, making them unsuited for identifying the species. The petal lengths and widths fare better in that regard, though there is still an overlap between versicolor and virginica.
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

In order to use the KL-divergence, we need to assign a probability distribution to the features. Based on the histograms in Fig. 4, we assume that the individual features are following a normal distribution $\mathcal{N}(\mu_{I_i},\sigma_{I_i})$, where $I_i$ denotes a given iris species, $I_i \in \\{ \text{setosa, versicolor, virginica} \\}$, and where $\mu_{I_i}$ and $\sigma_{I_i}$ can be guessed by simply taking the mean value resp. the standard deviation. However, we also need to take into account the measurement error of our data: While the error is not directly specified, the measurements are only given up to one digit of precicion. We therefor assume that if for example the data denotes a petal width of 1.4 cm, that the "true" petal width lies somewhere within the range of 1.35 cm to 1.45 cm. For the likelihoods, this yields:

$$ P[ Z = z | I_i ] = \int_{z-0.05}^{z+0.05} f(x|\mu_{I_i},\sigma_{I_i}) dx \\: , $$

where $Z$ represents one of the four features taking on the value $z$ and where $f(x|\mu_{I_i},\sigma_{I_i})$ is the probability density function of $\mathcal{N}(\mu_{I_i},\sigma_{I_i})$. If one does not wish to perform a numerical integration, one can also determine the likelihoods using the cumulative distribution function:

$$ P[ Z = z | I_i ] = CDF(z+0.05|\mu_{I_i},\sigma_{I_i}) - CDF(z-0.05|\mu_{I_i},\sigma_{I_i}) \\: . $$

The resulting likelihood distributions are shown in Fig. 5. As can be seen, they more or less simply follow along the histograms of Fig. 4.

</p>

<figure>
  <p align="center">
  <img src="/Images/02Likelihoods.png" width="500"/>
  </p>
  <figcaption>
    <p align="center">
    Fig. 5: Likelihood probability distributions for the four features given in percentage. Values are only valid in steps of 0.1 cm.
    </p>
  </figcaption>
</figure>

<p align="justify"> 
We can now determine the distance between the different likelihood distributions, summarized in the table below. As expected, for the sepal length and width the distances are rather small, making them unsuited for identifying the iris species. The petal length is optimal for differentiating between a setosa and the other two species, while the petal width is best suited for differentiating between a versicolor and a virginica. Since the distance between the versicolor and virginica distributions are always unfortunately small for all features, the major difficulty will always be to differeniate these two species. For setosa on the other hand, the distance to the other species for both the petal length and width is rather large, making it easy to identify either way. Hence, if one only wishes to measure a single feature per flower, the petal width should be chosen in order to best identify the species.
</p>

| Iris                  | Sepal Length  |  Sepal Width  |  Petal Length  |  Petal Width   |
| -------------         | ------------- | ------------- |  ------------- |  ------------- |
| setosa/versicolor     | 5.41          |  3.78         |   150.25       |   68.33        |
| setosa/virginica      | 13.95         |  1.76         |   308.89       |   166.11       |
| versicolor/virginica  | 1.41          |  0.41         |   6.57         |   9.74         |

## Determining the Species using the Petal Width

<p align="justify"> 

So far, we have determined the likelihood distributions $P[ Z = z | I_i ]$, which for a given iris gives us the probability of a particular feature $Z$ having some specific value. What we want however is the exact opposite: We wish to find the probability of having found a specific species of iris given that we measured some feature, $P[I_i | Z=z]$. We can find this so-called posterior probability by employing Bayes' theorem:

$$ P[I_i | Z=z] = \frac{ \pi(I_i) \\, P[ Z = z | I_i ] }{ \sum_{i=1}^3 \pi(I_i) \\, P[ Z = z | I_i ] } \\: .$$

$\pi(I_i)$ is the so-called prior probability and, as the name suggests, denotes our "prior knowledge" of having found a given iris species without having taken any measurements. In this instance, the prior corresponds to the relative frequency of the iris species: If we would for example know that 99% of all irises are setosa, then we could more or less assume any iris we find to be a setosa unless our measuremnts were to strongly suggest otherwise. The dataset provided to us does not list the frequency of the different iris species and each species of iris has the same amount of measurements assigned to it. We hence will perhaps naively assume that the three iris species appear with the same frequency, so that $\pi(I_i) = \frac{1}{3}$. Conviniently, this means that the prior will cancel out of the formula for the posterior, so that we can disregard it from now on.

We can now determine our posterior probabilities using the likelihoods, as displayed in Fig. 5. For the sepal length and width, the posteriors of the three irises intersect frequently and have little distance between them. At each intersection, the probabilities of having found one species of iris becomes the exact same as having found the other species of iris, making identification impossible. For the petal length and width on the other hand, only two such intersections occure.

</p>

<figure>
  <p align="center">
  <img src="/Images/03Posteriors.png" width="500"/>
  </p>
  <figcaption>
    <p align="center">
    Fig. 5: Posterior probability distributions for the four features given in percentage. Values are only valid in steps of 0.1 cm.
    </p>
  </figcaption>
</figure>

<p align="justify"> 

As discussed in the previous section, we will now examine the petal width more closely, shown in Fig. 6. We have two intersections and hence two regions where we might struggle with identifying the iris. 

- The first intersection is between setosa and versicolor and occurs somewhere around a petal width of ~0.65 cm. According to the data, we can however only measure petal widths up to a millimetre, meaning we do not actually have to worry about the intersection itself. At a petal width of 0.6 cm and 0.7 cm, the probability of it being either one of the irises is still at around 85%.

- The second intersection happens between versicolor and virginica at a petal width of around ~1.65 cm. This time, it proves to be much more of a problem, as at 1.6 cm and 1.7 cm the probability of having found either iris drops to only around 65%, meaning that confusing a versicolor for a virginica with those petal widths or vice versa is somewhat likely to happen.

</p>

<figure>
  <p align="center">
  <img src="/Images/04PosteriorPW.png" width="500"/>
  </p>
  <figcaption>
    <p align="center">
    Fig. 6: Posterior probability distributions for the petal width. The dots represent the actual values that can be measured.
    </p>
  </figcaption>
</figure>

<p align="justify"> 
So far, we can conclude that by only measuring the petal width, we are for the most part able to identify the species of an iris reasonably well. Only when we find an iris with a petal width between 1.6 cm and 1.7 cm do we encounter some larger uncertainties as to whether we have found a versicolor or a virginica.
</p>

## Correlation: Is it Worth Measuring Two Features?

<p align="justify"> 

</p>

tba

## Determining the Species using both the Petal Width and Petal Length

<p align="justify"> 

</p>

tba

## Conclusion

<p align="justify"> 

</p>

tba
