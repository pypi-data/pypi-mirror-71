# Introduction
This library provides a pure Python interface for a Generalized Recommendation system.

## Recommender Systems
Recommender Systems are algorithms aimed at suggesting relevant items to users (items being products to buy, movies to watch, text to read or anything else depending on industries). There exist two major categories of methods 
1. Content based methods
2. Collaborative filtering methods

#### Content Based Recommendation
Content based approaches use additional information about users and/or items. The major idea of content based methods is to try to build a model, based on the available “features”, that explain the observed user-item interactions.

#### Collaborative Filtering Methods
Collaborative methods for recommender systems are methods that are based solely on the past interactions recorded between users and items in order to produce new recommendations. 

# Installing

> pip install py-recommendation

# Usage

## Module Import

```python
import py_recommendation as prc
```

## Fetch the Input Data
Generate input data object which can be used for various types of recommendations available

```python
inputInitialise = prc.InputData()

ItemData = inputInitialise.getData_file(
    filePath = 'path to the data file',
    itemName_col = 'column name carrying the item name/id',
    itemTag_col = 'column name carrying the item features',
    fileType = 'type of file (xlsx/csv)'
    )
```
## Recommeder based on Similar Items
This is used to find other items similar to the given item based on the features.

```python
similarItemInit = prc.SimilarItem(ItemData)
recommendation = similarItemInit.similarItem('Item name/id')
```
*recommendation* carries a list with each recommended items and their recommendation score on 100



