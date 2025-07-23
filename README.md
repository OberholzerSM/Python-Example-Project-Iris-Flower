# Data Analysis Example Project: Iris Flower

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
    By No machine-readable author provided. Dlanglois assumed (based on copyright claims). - No machine-readable source provided.
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
    By Frank Mayfield - originally posted to Flickr as Iris virginica shrevei BLUE FLAG, CC BY-SA 2.0,
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

In order to use the KL-divergence, we need to assign a probability distribution to the features. Based on the histograms in Fig. 4, we assume that the individual features are following a normal distribution $\mathcal{N}(\mu_{I_i},\sigma_{I_i})$, where $I_i$ denotes a given iris species, $I_i \in \\{ \text{setosa, versicolor, virginica} \\}$, and where $\mu_{I_i}$ and $\sigma_{I_i}$ can be guessed by simply taking the mean value resp. the standard deviation. However, we also need to take into account the measurement error of our data: While the error is not directly specified, the measurements are only given up to one digit of precision. We therefor assume that if for example the data denotes a petal width of 1.4 cm, that the "true" petal width lies somewhere within the range of 1.35 cm to 1.45 cm. For the likelihoods, this yields:

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
We can now determine the distance between the different likelihood distributions, summarized in the table below. As expected, for the sepal length and width the distances are rather small, making them unsuited for identifying the iris species. The petal length is optimal for differentiating between a setosa and the other two species, while the petal width is best suited for differentiating between a versicolor and a virginica. Since the distance between the versicolor and virginica distributions are always unfortunately small for all features, the major difficulty will always be to differentiate these two species. For setosa on the other hand, the distance to the other species for both the petal length and width is rather large, making it easy to identify either way. Hence, if one only wishes to measure a single feature per flower, the petal width should be chosen in order to best identify the species.
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

$\pi(I_i)$ is the so-called prior probability and, as the name suggests, denotes our "prior knowledge" of having found a given iris species without having taken any measurements. In this instance, the prior corresponds to the relative frequency of the iris species: If we would for example know that 99% of all irises are setosa, then we could more or less assume any iris we find to be a setosa unless our measurements were to strongly suggest otherwise. The dataset provided to us does not list the frequency of the different iris species and each species of iris has the same amount of measurements assigned to it. We hence will perhaps naively assume that the three iris species appear with the same frequency, so that $\pi(I_i) = \frac{1}{3}$. Conveniently, this means that the prior will cancel out of the formula for the posterior, so that we can disregard it from now on.

We can now determine our posterior probabilities using the likelihoods, as displayed in Fig. 5. For the sepal length and width, the posteriors of the three irises intersect frequently and have little distance between them. At each intersection, the probabilities of having found one species of iris becomes the exact same as having found the other species of iris, making identification impossible. For the petal length and width on the other hand, only two such intersections occur.

</p>

<figure>
  <p align="center">
  <img src="/Images/03Posteriors.png" width="500"/>
  </p>
  <figcaption>
    <p align="center">
    Fig. 6: Posterior probability distributions for the four features given in percentage. Values are only valid in steps of 0.1 cm.
    </p>
  </figcaption>
</figure>

<p align="justify"> 

As discussed in the previous section, we will now examine the petal width more closely, shown in Fig. 7. We have two intersections and hence two regions where we might struggle with identifying the iris. 

- The first intersection is between setosa and versicolor and occurs somewhere around a petal width of ~0.65 cm. According to the data, we can however only measure petal widths up to a millimetre, meaning we do not actually have to worry about the intersection itself. At a petal width of 0.6 cm and 0.7 cm, the probability of it being either one of the irises is still at around 85%. Furthermore, the likelihood of actually measuring a petal width of either 0.6 cm or 0.7 cm for either species is nearly zero (see Fig. 5).

- The second intersection happens between versicolor and virginica at a petal width of around ~1.65 cm. This time around it proves to be much more of a problem, as at 1.6 cm and 1.7 cm the probability of having found either iris drops to only around 65%, meaning that confusing a versicolor for a virginica with those petal widths or vice versa is somewhat likely to happen. The likelihoods of measuring a petal width of 1.6 cm or 1.7 cm is also not small enough for us to be able to ignore the issue.

</p>

<figure>
  <p align="center">
  <img src="/Images/04PosteriorPW.png" width="500"/>
  </p>
  <figcaption>
    <p align="center">
    Fig. 7: Posterior probability distributions for the petal width. The dots are in steps of 0.1 cm and represent the actual values that can be measured.
    </p>
  </figcaption>
</figure>

<p align="justify"> 
So far, we can conclude that by only measuring the petal width, we are for the most part able to identify the species of an iris reasonably well. Only when we find an iris with a petal width between 1.6 cm and 1.7 cm do we encounter some larger uncertainties as to whether we have found a versicolor or a virginica.
</p>

## Correlation: Is it Worth Measuring more than One Feature?

<p align="justify"> 

In the previous section, it was found that for petal widths between 1.6 cm and 1.7 cm, the species becomes uncertain. To remedy this, the first thought would naturally be to measure an additional feature alongside the petal width to clear things up. However, when measuring more than one feature at once, one must also take the correlation into consideration: The width of the petals will for example naturally scale up alongside its length, making it in a sense redundant to measure both. To this end, Fig. 8 displays the correlation plots between the petal width and the other three features. Unfortunately for us, the correlation appears rather strong between all of them.

</p>

<figure>
  <p align="center">
  <img src="/Images/05CorrelationPW.png" width="500"/>
  </p>
  <figcaption>
    <p align="center">
    Fig. 8: Correlation Plot between the Petal Width and the other three features.
    </p>
  </figcaption>
</figure>

<p align="justify"> 

What's more, as evident by the likelihoods in Fig. 5, the sepal length and width is virtually useless when it comes to differentiating between versicolor and virginica, even if they were completely independent from the sepal width. This only leaves us with the sepal length, which is naturally strongly correlated with the sepal width. As such, we conclude that measuring any other of the features provided by the data will provide us with little to no additional information and is not worth the hassle.

</p>

## Determining the Species using both the Petal Width and Petal Length

<p align="justify"> 

For the sake of exercise, we can ignore our previous warning and see what changes if we measure two features instead of just one. In addition to the petal width $PW$, we will now also include the petal length $PL$ in our model. Both features are again assumed to follow along a normal distribution and to have a precision of up to a millimetre. However, this time around we also need to take into account the correlation between the two features. In practice, this means that the likelihood will take on the form of a multivariate normal distribution:

```math
P[ PL = pl, PW = pw | I_i ] = \int_{pl-0.05}^{pl+0.05} \int_{pw-0.05}^{pw+0.05} f(x,y | \vec{\mu}_{I_i}, \Sigma_{I_i}) \\, dx \\, dy
```

where $f\left(x,y | \vec{\mu}, \Sigma\right)$ is the PDF of the bivariate normal distribution, $\vec{\mu}$ is the vector of expected values and $\Sigma$ is the correlation matrix. Again, we can determine the likelihoods with the help of the CDF function,

```math
P[ PL = pl, PW = pw | I_i ] = CDF(pl+0.05, pw+0.05) + CDF(pl-0.05, pw-0.05) - CDF(pl+0.05, pw-0.05) - CDF(pl-0.05, pw+0.05) .
```

Note however that the more features we include into our model, the larger the risk of numerical errors occurring in regions of small probabilities due to underflow. In particular, the previous formula may yield negative values for the likelihood, which is logically nonsensical. In such cases, it should be simply set to zero.

As previously, we can calculate the posterior probabilities using Bayes' theorem (again assuming a uniform prior),

```math
P[I_i | PL = pl, PW = pw] = \frac{ P[ PL = pl, PW = pw | I_i ] }{ \sum_{i=1}^3 P[ PL = pl, PW = pw | I_i ] } \\: .
```

Here too do we need to tread carefully as we venture into regions of small probability, since the normalization factor may yield numerically zero.

The resulting posterior is now a function that both depends on the petal length and petal width. As such, it is best displayed as a heatmap as show in Fig. 9. Both setosa and versicolor occupy a particular region in state-space. Interestingly enough, virginica appears to be used as a sort of "default option" everywhere else. One can also see some strips in the region with high petal widths and low petal lengths. Note that these regions have no associated data and as such very low likelihood, meaning that we can interpret those as simply numerical artifacts.

</p>


<figure>
  <p align="center">
  <img src="/Images/06PosteriorPLPWHeatmap.png" width="500"/>
  </p>
  <figcaption>
    <p align="center">
    Fig. 9: Heatmap of the Posterior for the Petal Length and Petal Width. Regions of high probability are marked by brighter colours.
    </p>
  </figcaption>
</figure>

<p align="justify"> 

In a previous section, we ran into the problem that there was an ambiguity of whether one has found a versicolor or a virginica if one has measured a petal width of 1.6 cm or 1.7 cm. To see whether we have improved our situation, we can look at a "slice" of the heatmap, shown in Fig. 10 and Fig. 11. To better see if the odds have indeed been improved, the old posterior of the petal width is shown as a dashed line.

- For a petal width of 1.6 cm, we appear to have overall improved our ability to distinguish between versicolor and virginica. However, between a petal length of ~3.5cm - 4cm and ~5cm - 5.5 cm, we have introduced even more uncertainty into our system. Unfortunately, those regions have a very high likelihood to appear in our measurements, meaning that outside of the slice between 4cm - 5cm, measuring the petal length has done us little favour.

- For a petal width of 1.7 cm, the situation looks even more grim. Here, our ability to identify the species has decreased within a range of roughly ~4.2 cm - 5.2 cm, which again correspond to regions of high likelihood. While our model defaults to virginica for very small and large petal lengths, seemingly increasing our ability to reliable identify the iris, one should note that these regions have a virtually zero chance of actually being measured.

In conclusion, we can say that measuring the petal length in addition to the petal width does not really help in distinguishing versicolor and virginica.

</p>

<figure>
  <p align="center">
  <img src="/Images/07PosteriorPLPW16.png" width="500"/>
  </p>
  <figcaption>
    <p align="center">
    Fig. 10: Posterior for the Petal Length and a Petal Width of 1.6 cm. The dashed lines represent the old posterior probability for a petal width of 1.6 cm without considering the petal length.
    </p>
  </figcaption>
</figure>


<figure>
  <p align="center">
  <img src="/Images/08PosteriorPLPW17.png" width="500"/>
  </p>
  <figcaption>
    <p align="center">
    Fig. 11: Posterior for the Petal Length and a Petal Width of 1.7 cm. The dashed lines represent the old posterior probability for a petal width of 1.7 cm without considering the petal length.
    </p>
  </figcaption>
</figure>


## Conclusion

<p align="justify"> 

By employing Bayes' theorem, we have shown that the species of an iris flower can in most cases be determined by measuring its petal width. For petal widths between 1.6 cm and 1.7 cm, a confusion between versicolor and virginica may occur. Measuring additional features provided by the dataset, such as the petal length, do not help to remedy this situation, as all provided features are strongly correlated with each other. To better help distinguishing between the different iris species, an additional less correlated feature, such as the colour and shade of the flower, would be needed.

</p>
