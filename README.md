# FM skills prediction

**Predicting player Football Manager skills using real statistics**

## Applications
Soccer statistics is a lot of fun, but sometimes may be overwhelming. For somebody like myself, a person who spent way too much time on Football Manager in childhood (and adulthood), it is much easier to assess those amazing tables with numbers in 1-20 range. Moreover, these numbers could be conveniently transformed into radar graphs. Oh, these radar graphs. I had them in my dreams, both nightmares and some, well, more pleasant ones. It would also be a lot of fun to see if the numbers can be transformed into atrificial ones!

## Data sources:
- **FM data:** https://www.kaggle.com/datasets/platinum22/foot-ball-manager-2023-dataset
- **Real soccer data:** https://fbref.com (and they get it from Opta, apparently)

## Steps

1. Preprocessing
    - per-team normalization of player statistics
2. Dimentionality reduction
    - application of PCA in order to reduce complexity of feeatures and multicollinearity
3. Team features generation
    - clustering / PCA
4. Similarity identification
    - teams
    - players
5. Modelling
6. Visualization